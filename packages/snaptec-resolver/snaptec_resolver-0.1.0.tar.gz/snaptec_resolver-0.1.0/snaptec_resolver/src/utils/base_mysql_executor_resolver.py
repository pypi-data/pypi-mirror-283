from constants import constants

from src.utils.base_sql_executor_resolver import BaseSQLExecutorResolver
from src.databases.sql_reader import SQLReader
from src.databases.mysql_handler import MySQLHandler
from src.utils.merge_graphql_schemas import GraphQLSchemaMerger

class BaseMySQLExecutorResolver(BaseSQLExecutorResolver):
    def __init__(self, event = {}, merge_schema = constants.merge_schema, **kwargs) -> None:
        self._event = event
        self._args = self._event.get('args') or {}
        self._kwargs = kwargs
        self._sql_reader = None
        self._mysql_handler: MySQLHandler = None
        self._sql_name = None
        self._sql_params = None
        self._formatted_result = None
        self._sql_script_file_path = "" # define at sub class
        # self._merge_schema = GraphQLSchemaMerger("../../appsync/schema.graphql")
        self._merge_schema = merge_schema
        self._post_init()
    
    #override
    def _before_init(self):
        self._merge_schema.add_schema_file()
        self._merge_schema.write_merged_schema()

    def set_sql_script_file_path(self, sql_script_file_path):
        self._sql_script_file_path = sql_script_file_path
        self._sql_reader.set_sql_file_path(sql_script_file_path)

    def set_sql_handler(self, sql_handler):
        self._mysql_handler = sql_handler
        
    def set_sql_reader(self, sql_reader):
        self._sql_reader = sql_reader

    def _get_default_sql_params(self):
        return {}

    def _get_sql_params(self, **kwargs):
        default_sql_params = self._get_default_sql_params()
        sql_params = default_sql_params.copy()
        sql_params.update(self._args)
        sql_params = self._update_sql_params_user_token(sql_params)
        return sql_params
    
    def _get_sql_param_names(self, sql_params):
        lst_sql_param_names = []
        for key, _ in sql_params.items():
            lst_sql_param_names.append(key)
        return lst_sql_param_names

    def _get_sql_name(self, **kwargs):
        name = 'DEFAULT NAME'
        return name
    
    def _get_complete_sql_script(self, sql_name, sql_params):
        return self._sql_reader.get_query_by_name(sql_name, params=sql_params)
    
    def init(self):
        # OLD VERSION
        pass
    
    # override
    def _init(self):
       self._init_sql_reader()
       self._sql_params = self._get_sql_params()
       self._sql_name = self._get_sql_name()
       self._query = self._get_complete_sql_script(self._sql_name, self._sql_params)

    def _init_sql_reader(self):
         self._sql_reader = SQLReader()
         self._sql_reader.set_sql_file_path(self._sql_script_file_path)

    # override
    def _connect_to_database(self):
        self._mysql_handler.connect()

    # override 
    def _get_data(self): 
        self._result = self._mysql_handler.execute_query(self._query, output_format='list_dict')

    # override
    def _format_result(self):
        self._formatted_result = self._result
    
    # override
    def _after_format_result(self):
        self._mysql_handler.close_connection()

    def get_result(self):
        self.template_method()
        return self._formatted_result
    
    def _update_sql_params_list_filters(self, sql_params):
        sql_params_copy = sql_params.copy()
        list_valid_filters = []
        for filter, value in sql_params_copy.items():
            if value is None:
                continue
            if isinstance(value, list) and len(value) == 0:
                continue
            list_valid_filters.append(filter)
        sql_params_copy["list_filter_names"] = list_valid_filters
        return sql_params_copy
    
    def _update_sql_params_user_token(self, sql_params):
        sql_params_copy = sql_params.copy()
        request_info = self._event.get('request') or {}
        request_headers = request_info.get('headers') or {}
        token = request_headers.get('authorization') or ''
        sql_params_copy['token'] = token
        return sql_params_copy
