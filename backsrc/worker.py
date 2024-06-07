from kamailio.models import Acc,Subscriber,ApiUsage
import time
import threading
from django.db import connection

class Worker():
    def __init__(self):
        self.mainLock = threading.Lock()
        self.customerLock = threading.Lock()
        self.working =[]
        self.logStart = Acc.objects.filter(call__isnull=True,method="INVITE")
        print(self.logStart.count())
        #time.sleep(25)
        self.initAll()
        return

    def fetchLog(self):
        self.mainLock.acquire()
        try:
            newLog = self.logStart[0]
            self.logStart= self.logStart[1:]
            for working in self.working:
                if working==newLog.callid:
                    self.mainLock.release()
                    return False
            self.working.append(newLog.callid)
            self.mainLock.release()
            return newLog
        except Exception as e:
            print("no hay aparentemente")
            print(e)
            try:
                self.logStart = Acc.objects.filter(call__isnull=True,method="INVITE")
                print("new count")
                print(self.logStart.count())
                self.mainLock.release()
            except:
                print("errorcito")
                self.mainLock.release()
                return False
                
        

    def fetchEndLog(self,myId):
        # print("my Id") 
        # print(myId)
        #logEnd = Acc.objects.get(callid=myId,method="BYE")
        try:
            logEnd = Acc.objects.get(call__isnull=True,callid=myId,method="BYE",sip_code='200')
        except Exception as e:
            print("y qloq")
            print(e)
        return logEnd
    def newBalance(self,username,cost):
        self.customerLock.acquire()
        try:
            consumer = Subscriber.objects.get(username=username).customer
            print("found")
            consumer.balance=float(consumer.balance)-cost
            consumer.save()
            self.customerLock.release()
            return consumer
        except:
            print("not found subscriber")
            return
            self.customerLock.release()
    # def recordDataReverse(self):
    #     try:
    #         self.mainLock.acquire()
    #         newLog = self.logEnd[0]
    #         self.logEnd= self.logEnd[1:]
    #         self.mainLock.release()
    #     except Exception as e:
    #         print("no hay aparentemente")
    #         print(e)
    #         return
    #     try:
    #         logStart = self.objects.get(callid=myId,method="INVITE")
    #         time.sleep(1)
    #         startDate=logStart.time
    #         endDate=newLog.time
    #         diff = (endDate-startDate).seconds/60
    #         destination = newLog.dst_user
    #         rate=0.010
    #         try:
    #             consumer = self.newBalance(newLog.src_user,rate*diff)
    #             newLog.consumer=consumer
    #             newLog.save()
    #             logStart.consumer=consumer
    #             logStart.save()
    #         except Exception as e:
    #             print("errorcito sumando")
                
    #             print(e)

    #     except Exception as e:
    #         print("errorcito fetching")
    #         print(e)
    #         print(newLog.id)
    #     connection.close()
    #     return

    def recordData(self):
        while True:
            newLog = self.fetchLog()
            if not newLog:
                time.sleep(1)
                continue
            try:
                logEnd = self.fetchEndLog(newLog.callid)
                time.sleep(1)
                startDate=newLog.time
                endDate=logEnd.time
                diff = (endDate-startDate).seconds/60
                print("difffff")
                print(diff*60)
                destination = newLog.dst_user
                rate=0.010
                try:
                    newCall = ApiUsage.objects.get(callid=logEnd.callid)
                    print("already exists")
                    consumer = self.newBalance(newLog.src_user,rate*diff)
                    newLog.consumer=consumer
                    newLog.call = newCall
                    newLog.save()
                    logEnd.consumer=consumer
                    logEnd.call = newCall
                    logEnd.save()
                    print("updated tho")
                except Exception as e:
                    print("Not created,creating")
                    try:
                        consumer = self.newBalance(newLog.src_user,rate*diff)
                        print("updated balance")
                        newCall = ApiUsage.objects.create(src_user=newLog.src_user,dst_user=destination,duration=diff*60,serviceProvided="USCALL",startTime=startDate,endTime=endDate,callid=logEnd.callid,consumer=consumer)
                        print("this one is done")
                        newLog.consumer=consumer
                        newLog.call = newCall
                        newLog.save()
                        logEnd.consumer=consumer
                        logEnd.call = newCall
                        logEnd.save()
                        print("this one is safed")
                    except Exception as e:
                        print("errorcito sumando")
                        
                        print(e)

            except Exception as e:
                print("errorcito fetching")
                print(e)
                print(newLog.id)
            print("this one finished")
            if newLog.callid in self.working: self.working.remove(newLog.callid)
            continue
    def initAll(self):
        while(True):
            # self.recordData()
            for y in range(15):
                threads = []
                t = threading.Thread(target=self.recordData)
                t.start()
                threads.append(t)
                
            for thread in threads:
                t.join()
                pass
        
            # else:
                # for y in range(20):
                #     threads = []
                #     t = threading.Thread(target=self.recordData)
                #     t.start()
                #     threads.append(t)
                    
                # for thread in threads:
                #     t.join()
                #     pass
                # self.logEnd = Acc.objects.filter(consumer__isnull=True,method="BYE")
                # for y in range(20):
                #     threads = []
                #     t = threading.Thread(target=self.recordDataReverse)
                #     t.start()
                #     threads.append(t)
                    
                # for thread in threads:
                #     t.join()
                #     pass 
        return

worker = Worker()