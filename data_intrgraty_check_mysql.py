#!/usr/bin/python -tt


"""A tiny Python program to make mysql can write data into db with current time
   Before using this tool, you need to intall mysql server, and configured db_user and db_pwd. 
   Also you need to inall mysql.connector, which is a python package to handle mysql.
"""

import sys
import mysql.connector
from mysql.connector import errorcode
import time
import datetime

#Connect to mysql server without indicating database name
def db_connect():
  config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    #'database': 'test',
    'raise_on_warnings': True,
  }

  try: cnx = mysql.connector.connect(**config)
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    else:
      print(err)
      exit(1)
  return cnx

#Create Database with indicated database name
def db_create(db_cursor,db_name):
    try:
      db_cursor.execute(
        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
      print("Failed creating database: {}".format(err))
      exit(1)

#Remove Databse with indicated database name
def db_remove(db_cursor,db_name):
    try:
      db_cursor.execute(
        "DROP DATABASE IF EXISTS {}".format(db_name))
    except mysql.connector.Error as err:
      print("Failed removing database: {}".format(err))
      exit(1)

#Create db tables with indicated table definition
def db_create_tables(cursor,tables):
  for name, ddl in tables.iteritems():
    try:
      cursor.execute(ddl)
    except mysql.connector.Error as err:
      if err.errno != errorcode.ER_TABLE_EXISTS_ERROR:
        print(err.msg)
        exit(1)

#Insert one record with current timestamp
def insert_one_record (cursor):
  now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
  add_record = ("INSERT INTO video_records"
               "(rec_time) "
               "VALUES ('" + now + "')")
  #print add_record
  cursor.execute(add_record,'') 

#check all timestamp whether there are some neiborhood timestamp are more than indicated value
def check_all_records(cursor, interval):
  query = ("SELECT rec_no, rec_time FROM test.video_records ")
  cursor.execute(query,'')
  first_flag = 0
  result_flag = 'true'
  #Check whether there are some neighbor records are with the interval more than indicated values
  for (rec_no, rec_time) in cursor:
    if first_flag == 0:
       #record the first record for later comparison
       (rec_no_before,rec_time_before) = (rec_no,rec_time)
       first_flag = 1 
       continue
    time_delta =rec_time - rec_time_before
    if time_delta.total_seconds()/ (rec_no - rec_no_before ) > interval :
       result_flag = 'false'
       print "Some timestamp is lost in rec_no:",rec_no,"Time interval is",time_delta,"Time stampe is ",rec_time
    #update it for the compasison target for future comparason
    (rec_no_before, rec_time_before) = (rec_no, rec_time)
  if result_flag == 'true' :
    print 'All records are OK.'
  else :
    print 'There are some data needs to be confirmed.'

#Usage print function
def print_help():
  print "Usage simple data intergrity check tool."
  print "--help \t print this information"
  print "--startWrite [interval] \t write a timestamp for the excution time into databse continously per [interval] seconds"
  print "--stopWrite \t stop writing a timestamp into database table. "
  print "--reset \t Database, table and the data will be removed forcely"
  print "--checkData [interval] \t Read the data from dabase to check how many data in neibourhood are with larger interval than the indicidated value. "

#update write flag
def update_write_flag (filename,flag):
    write_flag = ['write',flag]
    f= open (filename,'w')
    f.write(':'.join(write_flag))
    f.close() 

#check write flag to jusitify whethere database wrting should continue or not
def check_write_flag (filename) :
  f = open(filename,'r')
  write_flag = f.read()
  f.close()
  return write_flag.split(':')[1]

#Main function
def main():
  DB_NAME = 'test'
  TABLES = {}
  TABLES['video_records'] = (
    "CREATE TABLE `video_records` ("
    "  `rec_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `rec_time` timestamp NOT NULL,"
    "  PRIMARY KEY (`rec_no`)"
    ") ENGINE=InnoDB")
  #conf file to record write flag to control database wrting continue/stop
  write_flag_conf_file = sys.argv[0]+'.conf' 

  #get command option to decide which command need to be excuted 
  if len(sys.argv) >= 2:
    cmd = sys.argv[1]
  else:
    cmd = '--help'

  if cmd == '--help' : # print help information
    print_help()
    exit(0)
  
  #Stop the database writing.. 
  if cmd == '--stopWrite':
    update_write_flag(write_flag_conf_file,'false')
    exit(0)  

  #Connect to mydql without indicating database name
  db_cnx = db_connect()
  db_cursor= db_cnx.cursor()

  #Remove databse to reset test enviroment
  if cmd =='--reset' :
    update_write_flag(write_flag_conf_file,'false')
    time.sleep(0.5)
    db_remove(db_cursor,'test')
    exit(0)

  #Create test database if it does not exist
  try:
    db_cnx.database = DB_NAME
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        db_create(db_cursor,DB_NAME)
        db_cnx.database = DB_NAME
    else:
        print(err)
        exit(1)
 
  #create tables if they do not exist
  db_create_tables(db_cursor, TABLES)
  
  #Start write data into database continously until it is stoped by --stopWrite
  if cmd == '--startWrite' :
    if len(sys.argv)>2 and int(sys.argv[2]) >0 :
      update_write_flag(write_flag_conf_file,'true')
      print ('writing data....')
      while check_write_flag(write_flag_conf_file) == 'true' :
        #insert one record with current timestamp continously untill write_flag is set to false by --stopWrite per [interval] seconds
        insert_one_record(db_cursor)
        # Make sure data is committed to the database
        db_cnx.commit()
        time.sleep(int(sys.argv[2]))
      print('writing data is stopped.')
    else : #[inerval] is missed in the command line
      print('Usage --startWrite [interval]')
     
  #check record with indicated value
  if cmd == '--checkData' :
    if len(sys.argv)>2 and int(sys.argv[2]) >0 :
      check_all_records(db_cursor,int(sys.argv[2])) 
    else : #[interval] is missed in the command line
      print('Usage --checkData [interval]')
  
  #close handling
  db_cursor.close()
  db_cnx.close()  

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
