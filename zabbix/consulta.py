import apizabbix
from pprint import pprint
from datetime import datetime
import time
import json
import logging
import warnings
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

api = apizabbix.connect()


def _set_time_filter():
    st_date = time.strftime("%d/%m/%Y")
    time_filter = time.mktime(datetime.strptime(st_date, "%d/%m/%Y").timetuple())
    return time_filter


def _get_hosts(time_filter):
    try:
        hosts = api.host.get(time_from=time_filter)
        # Serializing json
        json_object = json.dumps(hosts, indent=4)
        # Writing to sample.json
        with open("files/hosts.json", "w") as f:
            f.write(json_object)
        return 1
    except Exception as e:
        logger.exception('_get_hosts() Exception')
        # creating/opening a file
        f = open("logs/logs.txt", "a")
        # writing in the file
        f.write(f'{str(datetime.now())} {str(e)}\n')
        # closing the file
        f.close()


def _ha_nodes():
    try:
        hanodes = api.hanode.get()
        # Serializing json
        json_object = json.dumps(hanodes, indent=4)
        # Writing to sample.json
        with open("files/hanodes.json", "w") as f:
            f.write(json_object)
        return 1
    except Exception as e:
        logger.exception('_ha_nodes() Exception')
        # creating/opening a file
        f = open("logs/logs.txt", "a")
        # writing in the file
        f.write(f'{str(datetime.now())} {str(e)}\n')
        # closing the file
        f.close()



def _get_problems(time_filter):
    try:
        problems = api.problem.get(severities=[4,5], time_from=time_filter)
        # Serializing json
        json_object = json.dumps(problems, indent=4)
        # Writing to sample.json
        with open("files/problems.json", "w") as f:
            f.write(json_object)
        return 1
    except Exception as e:
        logger.exception('_get_problems() Exception')
        # creating/opening a file
        f = open("logs/logs.txt", "a")
        # writing in the file
        f.write(f'{str(datetime.now())} {str(e)}\n')
        # closing the file
        f.close()


if __name__ == '__main__':
    time_filter = _set_time_filter()
    #_get_problems(time_filter)
    _ha_nodes()
