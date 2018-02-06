# coding: utf-8
import cx_Oracle 

def OperationToString(operation): 
    operations = [] 
    if operation & cx_Oracle.OPCODE_INSERT: 
        operations.append("insert") 
    if operation & cx_Oracle.OPCODE_DELETE: 
        operations.append("delete") 
    if operation & cx_Oracle.OPCODE_UPDATE: 
        operations.append("update") 
    if operation & cx_Oracle.OPCODE_ALTER: 
        operations.append("alter") 
    if operation & cx_Oracle.OPCODE_DROP: 
        operations.append("drop") 
    if operation & cx_Oracle.OPCODE_ALLOPS: 
        operations.append("all operations") 
    return ", ".join(operations) 

def OnChanges(message): 
    print "Message received" 
    print "    Database Name:", message.dbname 
    print "    Tables:" 
    for table in message.tables: 
        print "        Name:", table.name, 
        print "        Operations:",
        print OperationToString(table.operation) 
        if table.rows is None \
                or table.operation & cx_Oracle.OPCODE_ALLROWS: 
            print "        Rows: all rows" 
        else: 
            print "        Rows:" 
            for row in table.rows: 
                print "            Rowid:", row.rowid 
                print "            Operation:", 
                print OperationToString(row.operation) 
dsn=cx_Oracle.makedsn("10.70.61.97","1521","XE")

connection=cx_Oracle.connect('sys','oracle',dsn,mode =cx_Oracle.SYSDBA)
# connection = cx_Oracle.Connection("cx_Oracle/dev@t11g",
#         events = True) 
sql = "select instance_name from v$instance"
subscriptionAll = connection.subscribe(callback = OnChanges) 
subscriptionAll.registerquery(sql) 
subscriptionInsertUpdate = \
        connection.subscribe(callback = OnChanges, 
        operations = cx_Oracle.OPCODE_INSERT | \
        cx_Oracle.OPCODE_UPDATE, rowids = True) 
subscriptionInsertUpdate.registerquery(sql) 

raw_input("Hit enter to terminate...\n") 
