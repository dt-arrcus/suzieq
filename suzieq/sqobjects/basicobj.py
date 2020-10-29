import typing
import pandas as pd

from suzieq.utils import load_sq_config, Schema, SchemaForTable
from suzieq.engines import get_sqengine


class SqContext(object):

    def __init__(self, engine, config_file=None):
        self.cfg = load_sq_config(validate=False, config_file=config_file)

        self.schemas = Schema(self.cfg['schema-directory'])

        self.namespace = ''
        self.hostname = ''
        self.start_time = ''
        self.end_time = ''
        self.exec_time = ''
        self.engine = 'pandas'
        self.sort_fields = []
        self.engine = get_sqengine(self.engine)
        if not self.engine:
            # We really should define our own error
            raise ValueError


class SqObject(object):

    def __init__(self, engine_name: str = '', hostname: typing.List[str] = [],
                 start_time: str = '', end_time: str = '',
                 view: str = 'latest', namespace: typing.List[str] = [],
                 columns: typing.List[str] = ['default'],
                 context=None, table: str = '', config_file=None) -> None:

        if context is None:
            self.ctxt = SqContext(engine_name, config_file)
        else:
            self.ctxt = context
            if not self.ctxt:
                self.ctxt = SqContext(engine_name)

        self._cfg = self.ctxt.cfg
        self._schema = SchemaForTable(table, self.ctxt.schemas)
        self._table = table
        self._sort_fields = self._schema.key_fields()

        if not namespace and self.ctxt.namespace:
            self.namespace = self.ctxt.namespace
        else:
            self.namespace = namespace
        if not hostname and self.ctxt.hostname:
            self.hostname = self.ctxt.hostname
        else:
            self.hostname = hostname

        if not start_time and self.ctxt.start_time:
            self.start_time = self.ctxt.start_time
        else:
            self.start_time = start_time

        if not end_time and self.ctxt.end_time:
            self.end_time = self.ctxt.end_time
        else:
            self.end_time = end_time

        if not view and self.ctxt.view:
            self.view = self.ctxt.view
        else:
            self.view = view
        self.columns = columns

        if engine_name and engine_name != '':
            self.engine = get_sqengine(engine_name)
        else:
            self.engine = self.ctxt.engine

        if self._table:
            self.engine_obj = self.engine.get_object(self._table, self)
        else:
            self.engine_obj = None

        self._addnl_filter = None
        self._addnl_fields = []

    @property
    def all_schemas(self):
        return self.ctxt.schemas

    @property
    def schema(self):
        return self._schema

    @property
    def cfg(self):
        return self._cfg

    @property
    def table(self):
        return self._table

    def validate_input(self, **kwargs):
        """Dummy validate input"""
        return

    def get(self, **kwargs) -> pd.DataFrame:
        if not self._table:
            raise NotImplementedError

        if not self.ctxt.engine:
            raise AttributeError('No analysis engine specified')

        if self._addnl_filter:
            kwargs['add_filter'] = self._addnl_filter

        # This raises exceptions if it fails
        try:
            self.validate_input(**kwargs)
        except Exception as error:
            df = pd.DataFrame({'error': [f'{error}']})
            return df

        return self.engine_obj.get(**kwargs)

    def summarize(self, namespace='') -> pd.DataFrame:
        if not self._table:
            raise NotImplementedError

        if not self.ctxt.engine:
            raise AttributeError('No analysis engine specified')

        return self.engine_obj.summarize(namespace=namespace)

    def unique(self, **kwargs) -> pd.DataFrame:
        if not self._table:
            raise NotImplementedError

        if not self.ctxt.engine:
            raise AttributeError('No analysis engine specified')

        return self.engine_obj.unique(**kwargs)

    def analyze(self, **kwargs):
        raise NotImplementedError

    def aver(self, **kwargs):
        raise NotImplementedError

    def top(self, what='', n=5, reverse=False,
            **kwargs) -> pd.DataFrame:
        """Get the list of top/bottom entries of "what" field"""

        if "columns" in kwargs:
            columns = kwargs["columns"]
            del kwargs["columns"]
        else:
            columns = ["default"]

        table_schema = SchemaForTable(self._table, self.all_schemas)
        columns = table_schema.get_display_fields(columns)

        if what not in columns:
            self._addnl_fields.append(what)

        return self.engine_obj.top(what=what, n=n, reverse=reverse, **kwargs)
