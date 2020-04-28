import logging
import pymqi

# https://stackoverflow.com/questions/36805172/how-to-write-pcf-command-to-get-channel-status-with-a-condition/36900937#36900937

logging.basicConfig(level=logging.INFO)

queue_manager = 'QMU1'
channel = 'SYSTEM.ADMIN.SVRCONN'
host = '127.0.0.1'
port = '1414'
conn_info = '%s(%s)' % (host, port)

args = {pymqi.CMQCFC.MQCACH_CHANNEL_NAME: "*",
        pymqi.CMQCFC.MQIACH_CHANNEL_INSTANCE_TYPE: pymqi.CMQC.MQOT_CURRENT_CHANNEL}
  
qmgr = pymqi.connect(queue_manager, channel, conn_info, 'mqm', '131333')
pcf = pymqi.PCFExecute(qmgr)

CHSTATUS = ( 
            "MQCHS_INACTIVE", "MQCHS_BINDING", "MQCHS_STARTING", "MQCHS_RUNNING", 
                "MQCHS_STOPPING", "MQCHS_RETRYING", "MQCHS_STOPPED", 
                "MQCHS_REQUESTING", "MQCHS_PAUSED", 
                "", "", "", "", "MQCHS_INITIALIZING" 
        ); 
dict(
    MQCHS_INACTIVE = 0
    MQCHS_BINDING = 1
    MQCHS_STARTING = 2
    MQCHS_RUNNING = 3
    MQCHS_STOPPING = 4
    MQCHS_RETRYING = 5
    MQCHS_STOPPED = 6
    MQCHS_REQUESTING = 7
    MQCHS_PAUSED = 8
    MQCHS_INITIALIZING = 13
)

try:
    response = pcf.MQCMD_INQUIRE_CHANNEL_STATUS(args) 
except pymqi.MQMIError as e:
    if e.comp == pymqi.CMQC.MQCC_FAILED and e.reason == pymqi.CMQC.MQRC_UNKNOWN_OBJECT_NAME:
        logging.info('No queues matched given arguments.')
    else:
        raise
else:
    for queue_info in response:
        logging.info(f"CHANNEL NAME: {queue_info[pymqi.CMQCFC.MQCACH_CHANNEL_NAME]},
                               STATUS: {CHSTATUS[queue_info[pymqi.CMQCFC.MQIACH_CHANNEL_STATUS]]}") 


qmgr.disconnect()