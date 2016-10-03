#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-


from task import signin_task, tender_task
from Queue import Queue
from Queue import Empty
import logging,utils,signal,time
DEBUG = True
AUTO_TENDER = True
SIGNIN = True
reserved_amount = 50

logger = logging.getLogger("app")
mainQueue = Queue()

def handler(signum, frame):
    t1.stop()
    t2.stop()
    global running
    running = False
    
    print "receive a signal %d, is_exit = %d"%(signum, True)

def main():
    #初始化
    utils.initSys()

    #signal handler
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    #签到
    if SIGNIN:
        t1.daemon = True
        t1.start()
    
    #自动投资
    if AUTO_TENDER:
        t2.daemon = True
        t2.start()
    
    mainloop()
      
def mainloop():
    while running:
        try:
            data = mainQueue.get(timeout=2)
        except Empty:
            continue
              
        if data['type'] == 'encrypt':
            responseQueue = data['queue']
            collaborative_id = data['collaborative_id']
            resp = {
                    "status": "OK",
                    "collaborative_id":collaborative_id,
                    "data": "date"
                    }
            responseQueue.put(resp)
            pass
        elif data['type'] == 'encrypt2':
            d = data["data"]
            tradepassword = d["pwd"]
            uniqkey = d["key"]
            pwd = utils.encryptTradePassword(tradepassword, uniqkey)
            responseQueue = data['queue']
            collaborative_id = data['collaborative_id']
            resp = {
                    "status": "OK",
                    "collaborative_id":collaborative_id,
                    "data": pwd
                    }
            responseQueue.put(resp)
            pass
        else:
            pass
    
if __name__ == '__main__':
    t1 = signin_task(mainQueue)
    t2 = tender_task(mainQueue)
    running = True
    try:
        main()
        while 1:   
            alive=True  
            if t1.is_stop() and t2.is_stop():   
                alive=False  
            if not alive:   
                break  
    except KeyboardInterrupt, e: 
        print e
    
