from decouple import config
import os
from time import strftime

BACKUPPATH="/home/massndb/supernovadb/backup/dbbackup/"+ strftime("%y%m%d-%H%M%S") + ".sql.gz"

dumpscrip="mysqldump -u" + config('DB_USER') + " -p" + config('DB_PWD') + " -h " + config('DB_HOST') + " '" + config('DB_NAME') + "' | gzip -9 >"  + BACKUPPATH

os.system(dumpscrip)

#http://webcheatsheet.com/sql/mysql_backup_restore.php
#mysql -u [uname] -p[pass] [db_to_restore] < [backupfile.sql]