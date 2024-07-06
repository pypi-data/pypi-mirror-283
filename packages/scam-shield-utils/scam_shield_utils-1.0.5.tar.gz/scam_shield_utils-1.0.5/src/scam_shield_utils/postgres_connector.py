import psycopg
from psycopg.rows import dict_row
from io import StringIO
from logger_log import log_message

class postgressUtility:
    #class with postgres database utility.
    #Self explanatory parameters...
    def __init__(self, db_name = "", user_name = "", password = "", host = "", port=5432) -> None:
        self.db_name = db_name
        self.user_name = user_name
        self.pwd = password
        self.conn = None
        self.cursor = None
        self.host = host
        self.port = port

    def connect(self):
        #this function will connect to the postgres instance and also initiates cursor object
        conn_string = f"dbname={self.db_name} user={self.user_name} password={self.pwd} host={self.host} port={self.port}"
        try:
            self.conn = psycopg.connect(conn_string)
            if self.conn:
                self.cursor = self.conn.cursor(row_factory=dict_row)
                return True
            else:
                log_message('error', "Failed to establish a database connection.")
                return False
        except Exception as ex:
            msg = f"Unable to connect to Postgres Server. Error : {str(ex)}"
            log_message('error', msg)
            self.conn = None
            self.cursor = None
            return False
        
    def execute_void_query(self, sql):
        #this function is for executing ad-hoc query, which does not return rows.
        try:
            self.cursor.execute(sql)
            #self.conn.commit()
            return True
        except Exception as ex:
            msg = f"Unable to Execute Query. Error : {str(ex)}"
            log_message('error', msg)
            return False

    def execute_select_query(self, sql):
        #executes select query and return rows if existing.
        results = []
        try:
            if sql=="": raise Exception('invalid sql')
            results = self.cursor.execute(sql).fetchall()
            return results
        except Exception as ex:
            msg =f"Unable to Execute Select Query. Error : {str(ex)}"
            log_message('error', msg)
            return results


    def execute_insert_query(self, sql, data=[]):
        #executes insert query with data sent seperately.
        results = []
        try:
            if len(sql)==0: raise Exception ("invalid SQL")
            if len(data)>0:
                results = self.cursor.execute(sql,data)
            else:
                results = self.cursor.execute(sql)
            return results

        except Exception as ex:
            msg = f"Unable to Execute insert Query. Error : {str(ex)}"
            log_message('error', msg)
            return results

    
    def execute_using_copy_bulk(self,tablename,data_list, columns,convert = True):
        #this function uses copy command to insert bulk data into tables..
        #Convert the list to values of tupple.
        try:
            tup_list = [tuple (d.values()) for d in data_list]
            if convert:
                fields = ""
                for col in columns:
                    fields = fields + "," if len(fields)>0 else ""
                    fields = fields + col
            else:
                fields = columns
            con_str = f"COPY {tablename}({fields}) FROM STDIN"
            with self.cursor.copy(con_str) as copy:
                for rec in tup_list:
                    try:
                        copy.write_row(rec)
                    except Exception as ex:
                        msg = f"Errors while copying record : {str(ex)}"
                        log_message('error', msg)
                        continue
            self.conn.commit()
            return True
        except Exception as ex:
            self.conn.rollback()
            msg = f"Something went wrong. Error : {str(ex)}"
            log_message('error', msg)
            return False
        
        

