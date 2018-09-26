#!/usr/bin/python
 
# Import required python libraries
import glob 
import os
import time
import datetime
import pipes
import subprocess 
# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.
 
#DB_HOST = 'localhost' 
#DB_USER = 'root'
#DB_PASSWORD = '_mysql_user_password_'
#DB_NAME = '/backup/dbnameslist.txt'
#DB_NAME = 'db_name_to_backup'
#BACKUP_PATH = '/backup/dbbackup'

#DB_HOST = 'mysql'
#DB_USER = 'root'
#DB_PASSWORD = 'root'
#DB_NAME = 'vipparcel'
#BACKUP_PATH = '/backup' 


DB_HOST = os.environ.get("DB_HOST", None)
DB_USER = os.environ.get("DB_USER", None)
DB_PASSWORD = os.environ.get("DB_PASSWORD", None)
DB_NAME = os.environ.get("DB_NAME", None)
BACKUP_PATH = os.environ.get("BACKUP_PATH", None)

print DB_HOST
print DB_USER
print DB_PASSWORD
print DB_NAME
print BACKUP_PATH

# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = time.strftime('%Y%m%d-%H%M%S')

#Remove previous backups/direcotry
if os.path.exists(BACKUP_PATH):
	files = glob.glob(BACKUP_PATH + "/" + "*")
	for f in files:
		os.remove(f)
# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(BACKUP_PATH)
except:
    os.mkdir(BACKUP_PATH)
 
# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
print ("checking for databases names file.")
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print ("Databases file found...")
    print ("Starting backup of all dbs listed in file " + DB_NAME)
else:
    print ("Databases file not found...")
    print ("Starting backup of database " + DB_NAME)
    multi = 0
 
# Starting actual database backup process.
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")
 
   while p <= flength:
       db = dbfile.readline()   # reading database name from file
       db = db[:-1]         # deletes extra line
       dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_PASSWORD + " " + db + " > " + pipes.quote(BACKUP_PATH) + "/" + db + DATETIME + ".sql"
       os.system(dumpcmd)
       gzipcmd = "gzip " + pipes.quote(BACKUP_PATH) + "/" + db + DATETIME + ".sql"
       os.system(gzipcmd)
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_PASSWORD + " " + db + " > " + pipes.quote(BACKUP_PATH) + "/" + db + DATETIME + ".sql"
   os.system(dumpcmd)
   gzipcmd = "gzip " + pipes.quote(BACKUP_PATH) + "/" + db + DATETIME + ".sql"
   os.system(gzipcmd)

subprocess.Popen("s3cmd put " + pipes.quote(BACKUP_PATH) + "/" + db + DATETIME + ".sql" 's3://dbbackups-8h382hf722fjf2012n3yfh84t83ridjugfugii4g99/vipparcel_db/' ) 

print ("")
print ("Backup script completed")
print ("Your backups have been created in '" + BACKUP_PATH + "' directory")
