import socket
import threading
import re
import xml.etree.ElementTree as ET

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "Disconnect"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def parse_create_table(sql_statement):
    create_table_pattern = r"CREATE TABLE ([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)"
    # column_pattern = r"([a-zA-Z_][a-zA-Z0-9_]*) ([a-zA-Z_][a-zA-Z0-9_]*)\((\d*)\)?"
    primary_key_pattern = r"PRIMARY KEY\s*\(([^)]*)\)"
    foreign_key_pattern = r"FOREIGN KEY\s*\(([^)]+)\)\s*REFERENCES\s([^)]+)\s*\(([^)]+)\)"

    # Extract table name
    match = re.match(create_table_pattern, sql_statement)
    if match:
        # Extract primary key information
        primary_key_match = re.search(primary_key_pattern, sql_statement)
        if primary_key_match:
            primary_keys = primary_key_match.group(1).split(',')
        else:
            primary_keys = []

        #Eliminate the primary key part from sql statement
        sql_statement = re.sub(r",\s*"+primary_key_pattern,'',sql_statement)

        # Extract foreign key information
        foreign_keys = []
        foreign_key_match = re.search(foreign_key_pattern, sql_statement)
        while foreign_key_match:
            foreign_key = foreign_key_match.group(1)
            reference_table = foreign_key_match.group(2)
            reference_pk = foreign_key_match.group(3)
            fk = foreign_key,reference_table,reference_pk
            foreign_keys.append(fk)
            #Eliminate foreign key part from sql statement
            sql_statement = re.sub(r",\s*"+foreign_key_pattern,'',sql_statement,count=1)
            foreign_key_match = re.search(foreign_key_pattern, sql_statement)

        #Extract column information
        table_name = match.group(1)
        match = re.match(create_table_pattern, sql_statement)
        column_definitions = match.group(2)
        column_definitions_split = column_definitions.split(',')
        columns = []
        for col_def in column_definitions_split:
            if col_def[0] == ' ':
                col_def = col_def[1:]
            names_and_types = col_def.split(' ')
            column_name = names_and_types[0]
            data_type = names_and_types[1]
            if len(names_and_types) > 2 and names_and_types[2] == 'NOT' and names_and_types[3] == 'NULL':
                is_null = '0'
            else:
                is_null = '1'
            col = column_name, data_type, is_null
            columns.append(col)

        return {
            'table_name': table_name,
            'columns': columns, #one column is a tuple of column_name, data_type, is_null
            'primary_key_attributes': primary_keys,
            'foreign_keys': foreign_keys #one foreign key is a tuple of foreign_key,reference_table,reference_pk
        }

def parse_create_index(sql):
    # Regular expression to parse the CREATE INDEX statement with the UNIQUE keyword
    pattern = r"CREATE\s+(UNIQUE\s+)?INDEX\s+(\w+)\s+ON\s+(\w+)\s+\(([^)]+)\)"

    # Match the regular expression to the input string
    match = re.match(pattern, sql)

    if match:
        # Check if the UNIQUE keyword is present
        unique = match.group(1) is not None

        # Extract the components from the matched groups
        index_name = match.group(2)
        table_name = match.group(3)
        columns = match.group(4).split(', ')

        return index_name, unique, table_name, columns

        # print("Unique:", unique)
        # print("Index Name:", index_name)
        # print("Table Name:", table_name)
        # print("Columns:", columns)
    else:
        print("Failed to parse the CREATE INDEX statement.")

def create_index(db_name, index_name,unique, table_name, columns):
    tree = ET.parse('DataBases.xml')
    root = tree.getroot()

    databases = root.findall("DataBase")
    for database in databases:
        if database.attrib['dataBaseName'] == db_name:
            tables = database.find('Tables')
            for table in tables:
                if table.attrib['tableName'] == table_name:
                    is_unique =  '1' if unique else '0'
                    index_files = table.find('IndexFiles')
                    if index_files is not None:
                        for ind in index_files:
                            if ind.attrib['indexName'] == index_name + '.ind':
                                return f"Index with name {index_name} already exists!"
                    else:
                        index_files = ET.SubElement(table, 'IndexFiles')
                    index_file = ET.SubElement(index_files, 'IndexFile', indexName=index_name + '.ind',isUnique = is_unique)
                    index_attributes = ET.SubElement(index_file, 'IndexAttributes')
                    structure = table.find("Structure")
                    table_attributes = structure.findall("Attribute")
                    index_attributes_added = False
                    for col in columns:
                        for attrib in table_attributes:
                            if attrib.attrib['attributeName'] == col:
                                iattribute = ET.SubElement(index_attributes,'IAttribute')
                                iattribute.text = col
                                index_attributes_added = True
                    if not index_attributes_added:
                        return f"Column {col} not found"          
                    tree.write("DataBases.xml")
                    return "Query executed successfully"
            return "Table not found"
        
def find_database(db_name):
    tree = ET.parse('DataBases.xml')
    root = tree.getroot()

    databases = root.findall("DataBase")
    for database in databases:
        if database.attrib['dataBaseName'] == db_name:
            return database
    return None

def find_table(table_name):
    tree = ET.parse('DataBases.xml')
    root = tree.getroot()

    databases = root.findall("DataBase")
    for database in databases:
        tables = database.find('Tables')
        for table in tables.findall('Table'):
            if table.attrib['tableName'] == table_name:
                return table
    return None

def find_attribute_in_table(table_name, attribute_name):
    table = find_table(table_name)
    structure = table.find('Structure')
    if table is not None and structure is not None:
        for attribute in structure.findall('Attribute'):
            if attribute.attrib['attributeName'] == attribute_name:
                return attribute
        return None

def create_database(db_name):
    tree = ET.parse('DataBases.xml')
    root = tree.getroot()

    if find_database(db_name) is not None:
        return "Database already exists!"
    
    db = ET.SubElement(root, 'DataBase', dataBaseName=db_name)
    tables = ET.SubElement(db, 'Tables')
    tree.write("DataBases.xml")
    return "Query executed successfully"
 
def drop_database(db_name):
    tree = ET.parse('DataBases.xml')
    root = tree.getroot()

    databases = root.findall("DataBase")
    for database in databases:
        if database.attrib['dataBaseName'] == db_name:
            root.remove(database)
            tree.write("DataBases.xml")
            return "Query executed successfully"
    return "Database not found!"
 
def create_table(db_name, table_info):
    tree = ET.parse('DataBases.xml')
    root = tree.getroot()

    if table_info:
        table_name=table_info['table_name']
        databases = root.findall("DataBase")
        if len(databases):
            for database in databases:
                if database.attrib['dataBaseName'] == db_name:
                    tables = database.find("Tables")
                    for table in tables.findall("Table"):
                        if table.attrib['tableName'] == table_name:
                            return "Table already exists!"
                    tbl = ET.SubElement(tables, 'Table', tableName=table_name)
                    structure = ET.SubElement(tbl,'Structure')
                    for column, data_type, is_null in table_info['columns']:
                        attr = ET.SubElement(structure, 'Attribute', attributeName=column, type=data_type, isnull=is_null)
                    if len(table_info['primary_key_attributes']) >= 1:                       
                        pk = ET.SubElement(tbl, "primaryKey")
                        for pk_column in table_info['primary_key_attributes']:
                            pk_attr = ET.SubElement(pk,"pkAttribute")
                            pk_attr.text = pk_column
                    if len(table_info['foreign_keys']) >= 1:
                        foreign_keys_element = ET.SubElement(tbl,'foreignKeys')
                        for fk in table_info['foreign_keys']:
                            fk_attribute, reference_table, reference_pk = fk
                            #Check if reference table and reference attribute exist
                            if find_table(reference_table) is None:
                                return "Reference table not found!"
                            elif find_attribute_in_table(reference_table, reference_pk) is None:
                                return "Reference attribute not found!"
                            else:
                                foreign_key_element = ET.SubElement(foreign_keys_element,'foreignKey')
                                fkAttribute = ET.SubElement(foreign_key_element,'fkAttribute')
                                fkAttribute.text = fk_attribute
                                references = ET.SubElement(foreign_key_element,'references')
                                refTable = ET.SubElement(references,'refTable')
                                refTable.text = reference_table
                                refAttribute = ET.SubElement(references,'refAttribute')
                                refAttribute.text = reference_pk
                    tree.write("DataBases.xml") 
                    return "Query executed successfully"
        
def drop_table(db_name, table_name):
    tree = ET.parse('DataBases.xml')
    root = tree.getroot()

    databases = root.findall("DataBase")
    for database in databases:
        if database.attrib['dataBaseName'] == db_name:          
            tables = database.find("Tables")
            for table in tables.findall("Table"):
                if table.attrib['tableName'] == table_name:
                    tables.remove(table)
                    tree.write("DataBases.xml")
                    return "Query executed successfully"
            return "Table not found!"
            
    return "Database not found!"

def send_feedback_to_client(feedback_message, conn):
    feedback_message = feedback_message.encode(FORMAT)
    feedback_msg_length = len(feedback_message)
    send_length = str(feedback_msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(feedback_message)

def parse_insert(sql):
    table_pattern = r'INSERT INTO (\w+)'
    columns_pattern = r'\((.*?)\)'
    values_pattern = r'VALUES \((.*?)\)'

    # Extract table name, column names, and values
    table_match = re.search(table_pattern, sql)
    columns_match = re.search(columns_pattern, sql)
    values_match = re.search(values_pattern, sql)

    if table_match and columns_match and values_match:
        table_name = table_match.group(1)
        column_names = [column.strip() for column in columns_match.group(1).split(',')]
        values = [value.strip() for value in values_match.group(1).split(',')]

        insert_info = {
            'table_name': table_name,
            'column_names': column_names,
            'values': values
        }
        return insert_info
    else:
        return None


def handle_client(conn, addr):
    print(f"New connection: {addr} connected")
    connected= True
    current_database = ""
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
             
            print(f"{addr}: {msg}")

            #check if the message is a valid sql query
            pattern = re.compile(r"(USE\s[\w]+)|(CREATE\sDATABASE\s[\w]+)|(DROP\sDATABASE\s[\w]+)|(DROP\sTABLE\s[\w]+)|(CREATE\s+(UNIQUE\s+)?INDEX\s+(\w+)\s+ON\s+(\w+)\s+\(([^)]+)\))|CREATE TABLE ([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)|INSERT INTO (\w+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\);?")
            if re.fullmatch(pattern, msg):
                query_words = msg.split(" ")
                if query_words[0] == 'USE':
                    if find_database(query_words[1]) is not None:
                        current_database = query_words[1]
                        send_feedback_to_client("Database selected", conn)
                    else:
                        send_feedback_to_client("Database does not exist!", conn)
                elif query_words[0] == 'CREATE':
                    db_name = query_words[2]
                    if query_words[1] == 'DATABASE':
                        query_execution_result = create_database(db_name)
                        send_feedback_to_client(query_execution_result, conn)
                    elif query_words[1] == 'TABLE':
                        if current_database == '':
                            send_feedback_to_client("No database specified", conn)
                        else:
                            table_info = parse_create_table(msg)
                            query_execution_result = create_table(current_database, table_info)
                            send_feedback_to_client(query_execution_result,conn)
                    elif 'INDEX' in query_words:
                        index_info = parse_create_index(msg)
                        query_execution_result = create_index(current_database, index_info[0],index_info[1],index_info[2],index_info[3])
                        send_feedback_to_client(query_execution_result, conn)
                elif query_words[0] == 'DROP':
                    if query_words[1] == 'DATABASE':
                        db_name = query_words[2]
                        query_execution_result = drop_database(db_name)
                        send_feedback_to_client(query_execution_result,conn)
                    elif query_words[1] == 'TABLE':
                        if current_database == '':
                            send_feedback_to_client("No database specified", conn)
                        else:
                            table_name = query_words[2]
                            query_execution_result = drop_table(current_database, table_name)
                            send_feedback_to_client(query_execution_result, conn)
                elif query_words[0] == 'INSERT':
                    print(parse_insert(msg))
            elif msg == DISCONNECT_MESSAGE:   
                connected = False
                send_feedback_to_client("Disconnected successfully", conn)                   
            else:
                send_feedback_to_client("Invalid SQL query", conn)         
    conn.close()

def start():
    server.listen()
    print(f"Listening. Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active connections: {threading.active_count()-1}")

print("Server starting...")
start()
