#coding:utf-8

import socket
import base64
import time
import MySQLdb

class Queue():
    
    def __init__(self,maxsize=10):
        self.cache = [] #使用列表来实现FIFO的队列
        self.head = 'NXWJ'
        self.size = 0
        self.semaphore = 0
        self.maxsize = maxsize

    def get(self):
        if not self.empty():
            self.semaphore-=1
            return self.cache.pop()
        else:
            print "Queue is empty"

    def put(self,data):
        #print data
        if self.size <= self.maxsize:
            if data.startswith(self.head):
                data = base64.b64decode(data[4:])
                self.cache.insert(0,data)
                self.size+=1
                self.semaphore+=1
            else:
                print "The message head is wrong"
        else:
            print "The queue is full"
    def empty(self):
        if self.cache:
            return False
        else:
            return True
    
    def full(self):
        if self.size < self.maxsize:
            return False
        else:
            return True

if __name__=='__main__':
    Q = Queue()
    host = ''
    port = 23333
    i=0
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((host,port))
    sock.listen(5)
    try:
        db = MySQLdb.connect("localhost","root","123","test" )
        cu = db.cursor()
        sql = "truncate table socket"
        cu.execute(sql)
        db.commit()
        db.close()
    except Exception,e:
        print e
        db.rollback()
    while True:
        connection,address = sock.accept()
        try:
            buf = connection.recv(100)
            if not Q.full():
                Q.put(buf)
            else:
                print "Waiting for consume"
        except Exception,e:
            socket.timeout
            print "Time out\n"
            print e
        if Q.semaphore:
            #数据库操作开始
            try:
                content = Q.get()
                if content =='q':
                    connection.close()
                db = MySQLdb.connect("localhost","root","123","test" )
                cu = db.cursor()
                sql = "Insert into socket (id,content,time) values ('%d','%s','%s')"%(i,content,time.asctime(time.localtime(time.time())))
                cu.execute(sql)
                db.commit()

            except Exception,e:
                print e
                db.rollback()
            i+=1
            print "插入数据库成功('%d','%s','%s')"%(i,content,time.asctime(time.localtime(time.time())))
            #f. write(time.asctime(time.localtime(time.time()))+"----"+Q.get()+"\n")
    db.close()
    connection.close()