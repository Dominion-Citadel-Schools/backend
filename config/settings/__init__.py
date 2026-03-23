import pymysql
import os, socket
pymysql.install_as_MySQLdb()




hostname = socket.gethostname()

if hostname == "DESKTOP-2TCQM12":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
elif "staging" in hostname:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.staging")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
