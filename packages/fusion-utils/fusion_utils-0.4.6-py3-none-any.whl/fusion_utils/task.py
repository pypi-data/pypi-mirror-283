import uuid
import pandas as pd  # Ensure pandas is imported to use pd.isna

class Task:
    current_stage = 1

    def __init__(self, name, query=None, query_definition=None, table_alias=None, optional=False, stage=None, **kwargs):
        self.name = name
        self.optional = optional
        self.kwargs = kwargs
        self.query_definition = query_definition
        self.query = query
        self.table_alias = uuid.uuid4().hex if not table_alias else table_alias
        if stage is None or pd.isna(stage):
            self.stage = Task.current_stage
            Task.current_stage += 1
        else:
            self.stage = int(stage) if isinstance(stage, (int, float)) else Task.current_stage
            Task.current_stage = max(Task.current_stage, self.stage + 1)

    def define_query(self, query_definition):
        self.query_definition = query_definition

    def define_table_alias(self, table_alias):
        self.table_alias = table_alias

    def define_optional(self, optional):
        self.optional = optional


