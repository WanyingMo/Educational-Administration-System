import socket
import sys
import os
from threading import Thread
import time
import sqlite3


db = sqlite3.connect('teach.db')
#create student inforamtion table
db.execute ('''CREATE TABLE IF NOT EXISTS Student(
   ID             INTEGER    PRIMARY KEY   AUTOINCREMENT,
   NAME           TEXT      NOT NULL,
   Password       TEXT       NOT NULL,
   Gender         TEXT      NOT NULL,
   Age            TEXT       NOT NULL,
   Class          TEXT       MOT NULL,
   Phone          TEXT       NOT NULL,
   Address        TEXT      NOT NULL);''')

#create teacher inforamtion table
db.execute ('''CREATE TABLE IF NOT EXISTS Teacher(
   ID             INTEGER    PRIMARY KEY   AUTOINCREMENT,
   NAME           TEXT      NOT NULL,
   Password       TEXT       NOT NULL,
   Gender         TEXT      NOT NULL,
   Age            TEXT       NOT NULL,
   Class          TEXT       MOT NULL,
   Phone          TEXT       NOT NULL,
   Address        TEXT      NOT NULL);''')

#create administrator inforamtion table
db.execute ('''CREATE TABLE IF NOT EXISTS Administrators(
   ID             INTEGER    PRIMARY KEY   AUTOINCREMENT,
   NAME           TEXT      NOT NULL,
   Password       TEXT       NOT NULL,
   Age            TEXT       NOT NULL,
   Phone          TEXT       NOT NULL,
   Address        TEXT      NOT NULL);''')

#create class information table
db.execute ('''CREATE TABLE IF NOT EXISTS Course(
   ID             INTEGER       PRIMARY KEY   AUTOINCREMENT,
   Name           TEXT          NOT NULL,
   Credit         TEXT           NOT NULL,
   Teacherid      INT           NOT NULL,
   Cost           TEXT           NOT NULL,
   Upper_limit    INT     NOT NULL,
   Number         INT     NOT NULL);''')


#create class selection table
db.execute ('''CREATE TABLE IF NOT EXISTS Course_selection(
   Studentid         INTEGER PRIMARY KEY   AUTOINCREMENT,
   CourseId          INT         NOT NULL,
   Teacherid         INT         NOT NULL,
   Record            INT         NOT NULL);''')


def dataMerge(inpath,attachpath):
    conn = sqlite3.connect(inpath)
    conn.text_factory = str
    cur = conn.cursor()
    attach = 'attach database "'+attachpath+'" as w;'
    sql1 = 'insert into map select * from w.map;'
    sql2 = 'insert into images select * from w.images;'
    cur.execute(attach)
    cur.execute(sql1)
    cur.execute(sql2)


address = ('127.0.0.1',8888)
filedir1 = 'C:\\Users\\rommel\\Desktop\\python\\teach_system\\server\\'
filedir2='C:\\Users\\rommel\\Desktop\\python\\teach_system\\client\\'
def doRequest(client):
    #set up a object, every server has its own object to process events
    serverobj = ftpserver(client)
    #Receive the requirement of server
    while True:
        message = client.recv(1024).decode()
        msglist = message.split(' ')
        if msglist[0] == 'G':
            serverobj.doget(msglist[-1])
        if msglist[0] == 'P':
            serverobj.doput(msglist[-1])    

class ftpserver(object):
    def __init__(self,client):
        self.client = client

    def dolist(self):
        
        filelist = os.listdir(filedir)
        if not filelist:
            self.client.send('Noting in the filelist'.encode())
            
            time.sleep(0.1)
        else:
            self.client.send(b'OK')
            #send the name of the file to server
            for file in filelist:
                #If it is a normal file
                if os.path.isfile(filedir+file) and file[0] != '.':
                    self.client.send(file.encode())
                    time.sleep(0.1)

            self.client.send(b'##')
            time.sleep(0.1)

    def doget(self,filename):
        try:
            f = open(filedir+filename,'rb')
        except:
            self.client.send('File is not exist'.encode())
            return
        
        #File is opened
        self.client.send(b'OK')
        time.sleep(0.1)
        #The content of the file sent
        while True:
            data = f.read(1024)
            if not data:
                self.client.send(b'##')
                time.sleep(0.1)
                break
            self.client.send(data)
            #After sending the contend, close the file
            f.close()

    def doput(self,filename):
        try:
            f = open(filedir1+filename,'wb')
        except:
            self.client.send('上传失败'.encode())
            return
        self.client.send(b'OK')
        while True:
            data = self.client.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()

    def doexit(self):
        sys.exit(0)

def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind(address)
    server.listen(10)
    print('Waiting for connecting server......')

    while True:
        try:
            client,addr = server.accept()
            print('The server is connected：',addr)
        except KeyboardInterrupt:
            sys.exit("The server is disconnected！")
        except Exception as e:
            print(e)
            continue
        t = Thread(target=doRequest,args=(client,))
        t.setDaemon(True)
        t.start()
        
if __name__ == "__main__" :
    main()
