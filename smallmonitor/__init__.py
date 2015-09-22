import pymysql

try:
    pymysql.install_as_MySQLdb()
except:
    pass
