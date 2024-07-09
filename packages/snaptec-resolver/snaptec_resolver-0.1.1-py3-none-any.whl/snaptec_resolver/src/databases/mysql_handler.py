import pymysql
from sshtunnel import SSHTunnelForwarder
import paramiko
import json
from io import StringIO
import time
import boto3
import os
from src.utilities import singleton

class MySQLHandler(metaclass=singleton.Singleton):
    def __init__(self, database_host = None, 
                 database_port = 3306, 
                 database_user = None, 
                 database_password = None, 
                 database_name = None, 
                 ssh_host = None, 
                 ssh_port = 22, 
                 ssh_username = None,
                 ssh_password = None, 
                 ssh_private_key_file_path = None):
        self.__database_host = database_host
        self.__database_port = database_port
        self.__database_user = database_user
        self.__database_password = database_password
        self.__database_name = database_name
        self.__require_ssh_connection = False
        self.__require_iam_authentication = False
        self.__ssh_host = ssh_host
        self.__ssh_port = ssh_port
        self.__ssh_username = ssh_username
        self.__ssh_password = ssh_password
        self.__ssh_private_key_file_path = ssh_private_key_file_path
        self.__conn = None
    
    def set_database_host(self, database_host):
        self.__database_host = database_host
        return self
    
    def set_database_port(self, database_port):
        self.__database_port = database_port
        return self
    
    def set_database_user(self, database_user):
        self.__database_user = database_user
        return self
    
    def set_database_password(self, database_password):
        self.__database_password = database_password
        return self
    
    def set_database_name(self, database_name):
        self.__database_name = database_name
        return self
    
    def is_ssh_connection_required(self, is_required=False):
        self.__require_ssh_connection = is_required
        return self
    
    def is_iam_authentication_required(self, is_required=False):
        self.__require_iam_authentication = is_required
        return self
    
    def set_ssh_host(self, ssh_host):
        self.__ssh_host = ssh_host
        return self
    
    def set_ssh_port(self, ssh_port):
        self.__ssh_port = ssh_port
        return self

    def set_ssh_username(self, ssh_username):
        self.__ssh_username = ssh_username
        return self
    
    def set_ssh_private_key_file_path(self, ssh_private_key_file_path, ssh_password=None):
        self.__ssh_private_key_file_path = ssh_private_key_file_path
        self.__ssh_password = ssh_password
        self.__get_ssh_private_key_from_file_path()
        return self
    
    def set_ssh_private_key(self, ssh_private_key):
        # NOTE: RUN THE CODE BELOW BEFORE PASS TO THIS FUNCTION:
        # f = open('/path/to/key.pem','r')
        # s = f.read()
        # import io 
        # keyfile = io.StringIO(s)
        # mykey = paramiko.RSAKey.from_private_key(keyfile)
        self.__ssh_private_key = ssh_private_key


    def set_ssh_password(self, ssh_password):
        self.__ssh_password = ssh_password
        

    def __get_ssh_private_key_from_file_path(self):
        print('Getting SSH private key')
        with open(self.__ssh_private_key_file_path, 'r') as f:
            s = f.read()
            keyfile = StringIO(s)
            ssh_pkey = paramiko.RSAKey.from_private_key(keyfile, password=self.__ssh_password)
            self.__ssh_private_key = ssh_pkey

    def connect(self):
        t0 = time.time()
        if self.__require_ssh_connection:
            self.__connect_with_ssh()
        elif self.__require_iam_authentication:
            self.__connect_with_iam_authentication()
        elif not self.__require_ssh_connection:
            self.__normal_connect()
        t1 = time.time()
        print(f'MySQL connect time {t1-t0} seconds')

    def __connect_with_ssh(self):
        self.__ssh_tunnel = SSHTunnelForwarder(
                (self.__ssh_host, self.__ssh_port),
                ssh_username=self.__ssh_username,
                ssh_pkey=self.__ssh_private_key,
                remote_bind_address=(self.__database_host, self.__database_port))
        self.__ssh_tunnel.start()
        self.__conn = pymysql.connect(host='127.0.0.1',
                                        user=self.__database_user,
                                        passwd=self.__database_password,
                                        db=self.__database_name,
                                        port=self.__ssh_tunnel.local_bind_port)
        
    def __connect_with_iam_authentication(self):
        client = boto3.client('rds')
        token = client.generate_db_auth_token(
            DBHostname=self.__database_host,
            Port=self.__database_port,
            DBUsername=self.__database_user,
            Region=os.environ.get('AWS_REGION')
        )
        try:
            # create a connection object
            self.__conn = pymysql.connect(
                host=self.__database_host,
                user=self.__database_user,
                password=token,
                db=self.__database_name,
                ssl={ "rejectUnauthorized": False}
            )
        except Exception as e:
            print("ERROR: Unable to connect with  MySQL instance: {}".format(e))

    def __normal_connect(self):
        self.__conn = pymysql.connect(host=self.__database_host, 
                            user=self.__database_user,
                            passwd=self.__database_password, 
                            db=self.__database_name,
                            port=self.__database_port)

    def execute_query(self, query, output_format='default'):
        if self.__conn is None or not self.__conn.open:
            self.connect()
        cursor = self.__conn.cursor()
        print(f'Preparing execute query: {query}')
        t0 = time.time()
        cursor.execute(query)
        t1 = time.time()
        delta_time = t1 - t0
        print(f'Execute query completed. Query execution time {delta_time} seconds')
        if cursor.description is not None:
            rows = cursor.fetchall()
            results = rows
            if output_format == 'list_dict':
                results_dict = self.__get_output_as_list_dict(cursor, rows)
                results = results_dict
            elif output_format == 'one_dict':
                results_dict = self.__get_output_as_list_dict(cursor, rows)
                results = results_dict[0]
            # self.close_connection()
            return results
        # self.close_connection()
        return []
    
    def __get_output_as_list_dict_old(self, cursor, rows): # OLD VERSION
        headers = [x[0] for x in cursor.description]
        json_data = []
        for row in rows:
            json_data.append(dict(zip(headers,row)))
        result_json_str = json.dumps(json_data, default=str)
        result_dict = json.loads(result_json_str)
        return result_dict
    
    def __get_output_as_list_dict(self, cursor, rows): # CURRENT VERSION
        headers = [x[0] for x in cursor.description]
        json_header_indexes = [idx for idx, x in enumerate(cursor.description) if x[1] == 245] # 245 is JSON type. Link: https://www.mikusa.com/python-mysql-docs/docs/MySQLdb.constants.FIELD_TYPE.html and https://stackoverflow.com/questions/45455189/unknown-type-245-in-column
        json_data = []
        for row in rows:
            row = list(row)
            for idx in json_header_indexes:
                row[idx] = json.loads(row[idx] or '{}')
            json_data.append(dict(zip(headers,row)))
        result_json_str = json.dumps(json_data, default=str)
        result_dict = json.loads(result_json_str)
        return result_dict
        
    def close_connection(self):
        if self.__conn:
            if self.__conn.open:
                self.__conn.close()
        if self.__require_ssh_connection:
            self.__ssh_tunnel.close()