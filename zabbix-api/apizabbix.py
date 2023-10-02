from pyzabbix import ZabbixAPI
from dotenv import load_dotenv
import os
import logging
import warnings

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

load_dotenv()


def connect():
    try:
        zabbix_url = os.getenv("ZABBIX_URL")
        zabbix_user = os.getenv("ZABBIX_USER")
        zabbix_pass = os.getenv("ZABBIX_PASS")

        zapi = ZabbixAPI(zabbix_url)
        zapi.session.verify = False
        zapi.login(zabbix_user, zabbix_pass)

        return zapi
    except Exception as e:
        logger.exception("connect() Exception")
