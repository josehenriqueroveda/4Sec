from pyzabbix import ZabbixAPI
import os
import configparser
import logging
import warnings
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def connect():
    config = configparser.ConfigParser()
    config.read("config.ini")

    user = config.get('zabbix', 'user')
    password = config.get('zabbix', 'password')
    server = config.get('zabbix', 'server')

    zabbix_url = os.getenv('ZBXURL', str(server))
    zabbix_user = os.getenv('ZBXUSER', str(user))
    zabbix_pass = os.getenv('ZBXPASS', str(password))

    zapi = ZabbixAPI(zabbix_url)
    zapi.session.verify = False
    zapi.login(zabbix_user, zabbix_pass)

    return zapi
