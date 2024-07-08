from constants import constants
class GraphQLSchemaMerger:
    def __init__(self, output_file):
        self.output_file = output_file
        self.merged_schema = ""
        self.schema_files = constants.schema_files

    def _read_schema_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            # print(f"Error: File {file_path} not found.")
            return ""
        except IOError as e:
            # print(f"Error reading file {file_path}: {e}")
            return ""

    def add_schema_file(self, type_schema_v1_file=constants.type_schema_v1_file, query_file=constants.query_file):
        for schema_file in self.schema_files:
            schema_content = self._read_schema_file(schema_file)
            if schema_content:
                self.merged_schema += schema_content + "\n\n"
        # Read and append the type version 1 file
        # type_schema_v1_file = "../../appsync/type_schema/type_schema_versions/type_schema_v1.graphql"
        type_schema_v1_content = self._read_schema_file(type_schema_v1_file)
        if type_schema_v1_content:
            self.merged_schema += type_schema_v1_content + "\n\n"

        # Read and append the query schema file
        # query_file = "../../appsync/query_schema/query.graphql"
        query_content = self._read_schema_file(query_file)
        if query_content:
            self.merged_schema += query_content

    def write_merged_schema(self):
        try:
            with open(self.output_file, 'w') as outfile:
                outfile.write(self.merged_schema)
            print(f"Merged GraphQL schemas into: {self.output_file}")
        except IOError as e:
            pass
            # print(f"Error writing to file {self.output_file}: {e}")