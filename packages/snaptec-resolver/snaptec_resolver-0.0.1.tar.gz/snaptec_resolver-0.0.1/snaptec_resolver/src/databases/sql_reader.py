import re
import jinja2

class SQLReader:
    def __init__(self, sql_file_path = None, **kwargs):
        self.__sql_file_path = sql_file_path
        self.__kwargs = kwargs
        self.__all_queries = None

    def set_sql_file_path(self, sql_file_path):
        self.__sql_file_path = sql_file_path

    def read_sql_file(self):
        with open(self.__sql_file_path, 'r') as f:
            self.__all_queries = f.read()
    
    def get_query_by_name(self, query_name, params = {}):
        RE_GET_SQL = '(?<=-{{40}}BEGIN SQL QUERY-{{40}}\n-{{20}}NAME: {query_name}-{{20}}\n)(?:(?!-{{40}}END SQL QUERY-{{40}})[\s\S])*(?=-{{40}}END SQL QUERY-{{40}})'
        re_pattern = RE_GET_SQL.format(query_name=query_name)
        if self.__all_queries is None:
            self.read_sql_file()
        match = re.search(re_pattern, self.__all_queries)
        try:
            query_template = match.group()
            print('Query template matched:')
            print(query_template)
        except:
            query_template = "No query template"
            print("No query template matched")
        jinja_template = jinja2.Template(query_template)
        query = jinja_template.render(params)
        formatted_query = self.__format_query(query)
        print('Query after render:')
        print(formatted_query)
        return formatted_query

    def __format_query(self, query):
        formatted_query = self.__trim_blank_lines(query)
        return formatted_query

    def __trim_blank_lines(self, query):
        new_query = re.sub(r'(\n\t*\s*){2,}', '\n', query)
        return new_query