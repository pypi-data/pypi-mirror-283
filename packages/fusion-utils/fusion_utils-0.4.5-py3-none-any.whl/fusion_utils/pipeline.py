import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.cloud import bigquery
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional
from .task import Task
from .errors import *
import time
import sys
import threading
import pandas as pd
import numpy as np
import re

class Pipeline:
    def __init__(self, name, QA_flag=None):
        if QA_flag is None:
            print("NO QA_FLAG PASSED. DEFAULTING TO TRUE.")
            self.QA = True
        elif isinstance(QA_flag, str):
            self.QA = QA_flag.lower() == 'true'
        else:
            self.QA = QA_flag

        self.name = name
        self.stages = []
        self.errors = []  # To collect errors during execution
        self.halt_execution = False  # Flag to halt execution if a non-optional task fails
        self.qa_queries = []  # Initialize QA queries as an empty list
        self.tasks = []
        self.client = bigquery.Client(project='aic-production-core')
        self.temp_tables = {}
        self.status = {}
        self.set_table_map()
        self.initialize_datasets()
        self.set_smtp_ip()


    def add_qa_query(self, query, condition):
        """Update the QA queries."""
        self.qa_queries.append({'query': query, 'condition': condition})
        
    def print_elapsed_time(self, start_time, stop_event):
        while not stop_event.is_set():
            elapsed_time = time.time() - start_time
            sys.stdout.write(f"\rElapsed time: {elapsed_time:.2f} seconds")
            sys.stdout.flush()
            time.sleep(0.1)  # Adjust the sleep time as needed to print intermittently

    def set_table_map(self, dataset='3349c7ea_09a2_461d_87f5_312a5401c51a', table='LKP_QA_TABLE_MAPPING'):
        table_map = f'`{dataset}.{table}`'
        self.table_map_df = self.client.query(f'SELECT * FROM {table_map}').to_dataframe()
        self.dataset_map = dict(zip(self.table_map_df['alias'], self.table_map_df['qa_dataset' if self.QA else 'prod_dataset']))

    def set_email_recipients(self, recipients):
        if isinstance(recipients, str):
            self.recipients = [recipients]
        else:
            self.recipients = recipients

    def set_smtp_ip(self, dataset='3349c7ea_09a2_461d_87f5_312a5401c51a', table='LKP_SMTP_IP'):
        """Set the SMTP IP address from a BigQuery table."""
        if '_' not in dataset:
            dataset_id = self.translate_dataset(dataset)
            smtp_map = f'`{dataset_id}.{table}`'
        else:
            smtp_map = f'`{dataset}.{table}`'
        try:
            query = f"SELECT ip FROM {smtp_map} LIMIT 1"
            results = self.client.query(query).result()
            for row in results:
                self.smtp_ip = row['ip']
                break
            if not isinstance(self.smtp_ip, str):
                raise ValueError("Retrieved SMTP IP is not a string.")
        except Exception as e:
            raise ValueError('Cannot retrieve SMTP server IP.') from e

    def translate_dataset(self, alias):
        return getattr(self, alias)

    def initialize_datasets(self):
        for _, row in self.table_map_df.iterrows():
            alias = row['alias']
            dataset = row['qa_dataset'] if self.QA else row['prod_dataset']
            setattr(self, alias, dataset)

    def translate_tables(self, query):
        """Translate any tables with $ to the respective dataset_id from the table map."""
        for alias, dataset_id in self.dataset_map.items():
            query = query.replace(f'${alias}:', f'{dataset_id}.')
        return query

    def translate_query(self, query):
        """Translate query placeholders using pipeline temp tables and dataset mappings."""
        # Translate dataset alias
        query = self.translate_tables(query)
        # Translate task table alias
        for alias, table_name in self.temp_tables.items():
            query = query.replace(f'${{{alias}}}', table_name)
        return query

    def send_email(self, subject, body, recipients=None):
        """
        Send an email using SMTP to multiple recipients.
        """
        if not hasattr(self, 'smtp_ip'):
            raise SMTPConfigurationError("SMTP server IP is not configured.")

        if not recipients:
            if hasattr(self, 'recipients'):
                recipients = self.recipients
            else:
                raise SMTPConfigurationError('No recipient passed or defined within pipeline attributes.')

        if isinstance(recipients, str):
            recipients = [recipients]

        sender = 'pinapps@jdpa.com'
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = ", ".join(recipients)
        message['Subject'] = subject
        css = '<style>.pass { color: #008000; } .fail { color: #FF0000; }</style>'
        body_html = f"<html><head>{css}</head><body>{body}</body></html>"
        message.attach(MIMEText(body_html, 'html'))

        try:
            server = smtplib.SMTP(self.smtp_ip, 25)
            server.ehlo()  # Necessary for some SMTP servers
            server.sendmail(sender, recipients, message.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print("Failed to send email:", str(e))


    def send_completion_email(self):
        """Send an email notification upon pipeline completion."""
        status_summary = []
        pass_flag = True

        for task_name, updates in self.status.items():
            latest_update = updates[-1]  # Get the latest update for each task
            status_summary.append(f"<span class='{ 'pass' if latest_update.get('success', False) else 'fail' }'>Task '{task_name}': {latest_update['status']} at {latest_update['timestamp']}</span>")
            if not latest_update.get('success', False):
                pass_flag = False

        summary = "<br>".join(status_summary)
        flag_text = "PASS" if pass_flag else "FAIL"
        subject = f"Pipeline {self.name} Execution {flag_text}"
        body = f"Pipeline {self.name} has completed with the following status:<br><br>{summary}"

        try:
            self.send_email(subject, body)
        except Exception as e:
            print(f"Failed to send completion email: {e}")

    def execute_query(self, query, temp_table_name=None):
        query = self.translate_query(query)
        try:
            start_time = time.time()
            stop_event = threading.Event()
            elapsed_time_thread = threading.Thread(target=self.print_elapsed_time, args=(start_time, stop_event))
            elapsed_time_thread.start()

            ddl_patterns = [
                r"create\s+table", r"replace\s+table", r"insert\s+into", r"drop\s+table",
                r"alter\s+table", r"truncate\s+table", r"\bupdate\b", r"delete\s+from"
            ]

            # Check if the query contains actual DDL statements using regular expressions
            is_ddl = any(re.search(pattern, query.lower()) for pattern in ddl_patterns)

            # No destination if statement contains DDL
            if temp_table_name and not is_ddl:
                job_config = bigquery.QueryJobConfig(
                    destination=temp_table_name,
                    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
                )
                query_job = self.client.query(query, job_config=job_config)
            else:
                query_job = self.client.query(query)

            query_job.result()

            stop_event.set()
            elapsed_time_thread.join()

            end_time = time.time()
            total_elapsed_time = end_time - start_time
            print(f"\nQuery executed in {total_elapsed_time:.2f} seconds.")

            # Only create and update temp table if it's not a DDL statement
            if not is_ddl:
                self.create_temp_table(query_job, temp_table_name)
                self.update_temp_table_list(query, temp_table_name)

            return query_job, total_elapsed_time

        except Exception as e:
            stop_event.set()
            elapsed_time_thread.join()
            error_message = str(e).split('\n\n')[0].strip()
            raise TaskError(f"Failed to execute query: {error_message}")


    def create_temp_table(self, query_job, temp_table_name):
        """Set an expiration time for the temporary table created with the query job."""
        try:
            destination = query_job.destination
            if destination is None:
                print(f"No destination table created for job: {query_job.job_id}")
                return None

            table = self.client.get_table(destination)
            if table.table_type != 'TEMPORARY':
                table.expires = datetime.datetime.now() + datetime.timedelta(hours=1)
                self.client.update_table(table, ["expires"])  # API request
                print(f"Temporary table {temp_table_name} created.")
            else:
                print(f"Skipping expiration update for anonymous table {destination}")
            return temp_table_name
        except Exception as e:
            error_message = str(e).split('\n\n')[0].strip()  # Removing additional info
            raise TaskError(f"Failed to create temporary table {temp_table_name}: {error_message}")


    def log_task_execution(self, task_name, data_size, elapsed_time):
        """Log the task execution details to the Silver.LKP_TASK_LOG table."""
        try:
            if "test" in task_name.lower():
                print(f"Skipping logging for test task: {task_name}")
                return

            log_query = f"""
            INSERT INTO `{self.translate_dataset('Silver')}.LKP_TASK_LOG` (task_name, data_size, date_run, elapsed_time)
            VALUES ('{task_name}', {data_size}, '{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}', {elapsed_time})
            """
            # print(log_query)                  
            self.client.query(log_query).result()
            print(f"Logged task execution for task: {task_name}")
        except Exception as e:
            print(f"Failed to log task execution for task: {task_name}. Error: {str(e)}")


    def add_task(self, task):
        self.tasks.append(task)
        temp_table = f"{self.client.project}.AIC_BRANCH_JOB.{task.table_alias}"
        task.temp_table = temp_table

    def execute_stage(self, stage_tasks):
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.execute_task, task): task for task in stage_tasks}
            for future in as_completed(futures):
                task = futures[future]
                try:
                    future.result()
                except Exception as e:
                    error_message = f"Task '{task.name}' in stage {task.stage} failed with exception: {e}"
                    self.errors.append(error_message)
                    print(error_message)
                    if not task.optional:
                        self.halt_execution = True  # Halt further execution if a non-optional task fails
                        return

    def execute_all(self):
        """Execute all tasks in the pipeline stage by stage."""
        try:
            max_stage = max(task.stage for task in self.tasks)
            for stage in range(1, max_stage + 1):
                if self.halt_execution:
                    break  # Stop executing further stages if halt_execution flag is set
                stage_tasks = [task for task in self.tasks if task.stage == stage]
                if stage_tasks:
                    print(f"Executing stage {stage} with {len(stage_tasks)} task(s).")
                    self.execute_stage(stage_tasks)
            print("Pipeline execution completed.")
            
            # Run QA checks after all tasks are executed
            self.run_qa_checks()
        except Exception as e:
            error_message = f"Pipeline Failure: {e}"
            self.errors.append(error_message)
            print(error_message)
        finally:
            if self.errors:
                print("Errors encountered during pipeline execution:")
                for error in self.errors:
                    print(error)


            self.send_completion_email()  # Send email notification upon completion
         

    def run_qa_checks(self):
        """Run QA checks on the pipeline and collect results."""
        print("Running QA checks...")
        for qa in self.qa_queries:
            query = qa['query']
            condition = qa['condition']
            try:
                query_job = self.client.query(query)
                result = query_job.result().to_dataframe()
                if not condition(result):
                    self.errors.append(f"QA check failed for query: {query}")
                else:
                    print(f"QA check passed for query: {query}")
            except Exception as e:
                error_message = f"Failed to execute QA query: {query} with exception: {e}"
                self.errors.append(error_message)
                print(error_message)
                

    def execute_task(self, task):
        """Run a query and write the results to a temporary table in BigQuery."""
        try:
            if task not in self.tasks:
                raise TaskError(f"Task '{task.name}' has not been added to the pipeline. Use Pipeline.add_task() to execute.")

            if not task.query_definition:
                if not task.optional:
                    raise TaskError(f'{task.name} does not have a defined query')
                else:
                    print(f'WARNING: {task.name} does not have a defined query. Skipping optional task...')
                    self.update_status(task, 'Failed: No query defined')
                    return

            self.update_status(task, 'Started')

            # Generate the actual query using the pipeline's temp tables and dataset mappings
            try:
                task.query = self.translate_query(task.query_definition)
            except KeyError as e:
                raise TaskError(f"Failed to translate query for task '{task.name}': Missing key {str(e)} in temp tables")

            # Estimate data size using dry run
            estimated_data_size = self.estimate_data_size(task.query)
            print(f"Estimated data size for task '{task.name}': {estimated_data_size/1000000000:.2f} Gb")

            # Estimate run time using historical data
            estimated_run_time = self.estimate_run_time(estimated_data_size, task.name)
            if estimated_run_time:
                print(f"Estimated run time for task '{task.name}': {estimated_run_time:.2f} seconds")
            else:
                print(f"No historical data available to estimate run time for task '{task.name}'")

            try:
                temp_table_name = f"{self.client.project}.AIC_BRANCH_JOB.{task.table_alias}"
                query_job, elapsed_time = self.execute_query(task.query, temp_table_name)
                # create_temp_table is already called within execute_query
                self.update_temp_table_list(task.name, temp_table_name)

                # Log task execution details
                self.log_task_execution(task.name, estimated_data_size, elapsed_time)

                self.update_status(task, 'Completed')
                print(f"{task.name} Completed.")
            except Exception as e:
                self.update_status(task, f'Failed: {str(e)}')
                if not task.optional:
                    raise e

        except Exception as e:
            error_message = f"Task '{task.name}' in stage {task.stage} failed with exception: {e}"
            self.errors.append(error_message)
            print(error_message)
            self.update_status(task, f"Failed with exception: {str(e)}")
            if not task.optional:
                self.halt_execution = True


    def execute_task_by_name(self, task_name):
        """Find a task by name and execute it."""
        task = next((t for t in self.tasks if t.name == task_name), None)
        if task is None:
            raise TaskError(f"No task found with name '{task_name}'")
        self.execute_task(task)

    def execute_stage_by_number(self, stage_number):
        """Execute all tasks in a given stage number."""
        stage_tasks = [task for task in self.tasks if task.stage == stage_number]
        if not stage_tasks:
            error_message = f"No tasks found for stage {stage_number}"
            self.errors.append(error_message)
            print(error_message)
        else:
            self.execute_stage(stage_tasks)

    def update_temp_table_list(self, task_name, table):
        self.temp_tables[task_name] = f'{table}'
        # print(f"Temp table for task '{task_name}' updated to: {self.temp_tables[task_name]}")  # Debug statement

    def update_status(self, task, status):
        update = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': status
        }

        if status == 'Completed':
            update['success'] = True
        elif status.startswith('Failed'):
            update['success'] = False

        if task.name not in self.status:
            self.status[task.name] = []
        self.status[task.name].append(update)
        
    def estimate_data_size(self, query):
        """Estimate the data size of a query using a dry run."""
        job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
        query_job = self.client.query(query, job_config=job_config)
        return query_job.total_bytes_processed

    def get_historical_data(self):
        """Fetch historical task execution data from the log table."""
        query = f"""
        SELECT task_name, data_size, elapsed_time
        FROM `{self.translate_dataset('Silver')}.LKP_TASK_LOG`
        """
        df = self.client.query(query).to_dataframe()
        return df

    def estimate_run_time(self, estimated_data_size, task_name):
        """Estimate the run time of a task based on historical data."""
        df = self.get_historical_data()

        # Filter historical data for the same task
        df_task = df[df['task_name'] == task_name]

        if df_task.empty:
            print(f"No historical data available to estimate run time for task '{task_name}'")
            return None  # No historical data available for this task

        # Perform linear interpolation
        x = df_task['data_size'].values
        y = df_task['elapsed_time'].values

        # Use numpy to perform linear interpolation
        estimated_time = np.interp(estimated_data_size, x, y)
        return estimated_time

#     def apply_transformations_dynamically(self, table, transform_map_tbl):
#         for index, row in transform_map_tbl.iterrows():
#             transformation_cmd = row['TRANSFORMATION_CMD']
#             conditions = []
#             updates = {}

#             # Construct conditions based on the transformation command
#             if 'Rename Model' in transformation_cmd:
#                 conditions.append((table['model'] == row['model']) & (row['ACTIVE_IND'] == 'Y'))
#                 updates['model'] = row['NEW_NAME']

#             if 'Rename Series' in transformation_cmd:
#                 conditions.append((table['series'] == row['series']) & (row['ACTIVE_IND'] == 'Y'))
#                 updates['series'] = row['NEW_NAME']

#             if 'Move OEM' in transformation_cmd:
#                 conditions.append((table['oem'] == row['OEM']) & (row['ACTIVE_IND'] == 'Y'))
#                 updates['oem'] = row['NEW_NAME']

#             if 'Move Nameplate' in transformation_cmd:
#                 conditions.append((table['nameplate'] == row['nameplate']) & (row['ACTIVE_IND'] == 'Y'))
#                 updates['nameplate'] = row['NEW_NAME']

#             # Apply additional conditions based on specific transformation commands
#             if 'specific MY and effective period' in transformation_cmd:
#                 conditions.append(table['modelyear'] == row['modelyear'])
#                 conditions.append(table['monthofs'].between(row['EFFECTIVE_PERIOD_START'], row['EFFECTIVE_PERIOD_END']))

#             if 'specific model' in transformation_cmd:
#                 if pd.isna(row['nameplate']) and pd.isna(row['series']):
#                     conditions.append(pd.isna(table['nameplate']) & pd.isna(table['series']))
#                 elif not pd.isna(row['series']):
#                     conditions.append(table['series'] == row['series'])
#                 elif not pd.isna(row['nameplate']):
#                     conditions.append(table['nameplate'] == row['nameplate'])

#             # Combine all conditions using logical AND
#             combined_condition = conditions[0]
#             for condition in conditions[1:]:
#                 combined_condition &= condition

#             # Apply updates
#             for column, new_value in updates.items():
#                 table.loc[combined_condition, column] = new_value

#         return table
