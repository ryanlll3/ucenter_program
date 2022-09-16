#!/usr/bin/python
# _*_ coding:utf-8 _*_


import subprocess
import yaml
import time
from core.Logger import *

config_file = open('main_config/config.yml', 'r', encoding='utf-8')
config_variables = config_file.read()
conf = yaml.load(config_variables, Loader=yaml.FullLoader)

Reloading_Interval = conf.get('RELOADING_INTERVAL').get('SECONDS')

@setup_log
def UCenter_API_Process():
    try:
        Active_Alarms_Count = subprocess.call(['python', 'alarms/Active_Alarms_Count.py'])
        if Active_Alarms_Count == 0:
            logging.info("Active_Alarms_Count executed successfully.")
        else:
            logging.error("Active_Alarms_Count executed failed.")
    except Exception as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Exit Operation by Human.")
        exit(0)

    try:
        CI_List = subprocess.call(['python', 'cmdb/CI_List.py'])
        if CI_List == 0:
            logging.info("CI_List executed successfully.")
        else:
            logging.error("CI_List executed failed.")
    except Exception as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Exit Operation by Human.")
        exit(0)

    try:
        CI_Type = subprocess.call(['python', 'cmdb/CI_Type.py'])
        if CI_Type == 0:
            logging.info("CI_Type executed successfully.")
        else:
            logging.error("CI_Type executed failed.")
    except Exception as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Exit Operation by Human.")
        exit(0)

    try:
        RE_Type = subprocess.call(['python', 'cmdb/RE_Type.py'])
        if RE_Type == 0:
            logging.info("RE_Type executed successfully.")
        else:
            logging.error("RE_Type executed failed.")
    except Exception as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Exit Operation by Human.")
        exit(0)

    try:
        IOM_Dev_List = subprocess.call(['python', 'iom/IOM_Dev_List.py'])
        if IOM_Dev_List == 0:
            logging.info("IOM_Dev_List executed successfully.")
        else:
            logging.error("IOM_Dev_List executed failed.")
    except Exception as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Exit Operation by Human.")
        exit(0)

    try:
        IOM_Linux_OS_List = subprocess.call(['python', 'iom/IOM_Linux_OS_List.py'])
        if IOM_Linux_OS_List == 0:
            logging.info("IOM_Linux_OS_List executed successfully.")
        else:
            logging.error("IOM_Linux_OS_List executed failed.")
    except Exception as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Exit Operation by Human.")
        exit(0)

    try:
        IOM_Linux_OS_RealTime = subprocess.call(['python', 'iom/IOM_Linux_OS_RealTime.py'])
        if IOM_Linux_OS_RealTime == 0:
            logging.info("IOM_Linux_OS_RealTime executed successfully.")
            logging.info("\nData Reloading Completed.\n")
        else:
            logging.error("IOM_Linux_OS_RealTime executed failed.")
    except Exception as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Exit Operation by Human.")
        exit(0)


if __name__ == '__main__':
    while True:
        try:
            UCenter_API_Process()
            time.sleep(Reloading_Interval)
        except KeyboardInterrupt:
            logging.info("Exit Operation by Human.")
            exit(0)
