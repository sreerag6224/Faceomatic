
import serial
from  DBConnection import  Db
serialPort = serial.Serial(port="COM14")
import pyttsx3
engine = pyttsx3.init()
serialString = ""                           # Used to hold data coming over UART
mm=""
counter=0
studentlogid=""
while(True):
        serialString = serialPort.read().decode('utf-8')
        mm=mm+serialString
        if len(mm)==12:
            print(mm)
            db = Db()
            qry = "select * from rfid where key='" + mm + "'"
            res = db.selectOne(qry)
            if res is not None:
                # engine.say("Hi "+ res['student_name'])
                # engine.runAndWait()
                counter = counter + 1
                studentlogid = res['rfid_id']
                qry1=db.selectOne("select * from late where rfid_id='"+str(studentlogid)+"' and e_date=curdate()")
                if qry1 is None:
                    qry2=db.insert("insert into late(rfid_id,e_date,e_time) values('"+str(studentlogid)+"',curdate(),curtime())")
                else:
                    exTime=qry1['exit_time']
                    if exTime is None:
                        qry3=db.update("update late set exit_time=curtime() where late_id='"+str(qry1['late_id'])+"'")
            else:
                pass
            mm=""

