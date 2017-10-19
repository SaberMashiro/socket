#coding:utf-8
import socket
import time
import base64
import wx
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def Transfer(evt):
    host = '127.0.0.1'
    port = 23333
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))
    #time.sleep(1)
    a = unicode(Transfer_content.GetValue())
    message = base64.b64encode(a)
    sock.send("NXWJ"+message)
    time.sleep(1)
    #text_contents.SetValue(sock.recv(1024))
    sock.close()

def Load(evt):
    content = ''
    db = MySQLdb.connect("localhost","root","123","test" )
    cu = db.cursor()
    cu.execute("select * from socket")
    for i in cu.fetchall():
        content +=str(i)+"\n"
    text_contents.SetValue(content)
  
if __name__=='__main__':
    app = wx.App()
    win = wx.Frame(None,title='Transfer',size=(440,320))
    panel = wx.Panel(win)
    bt_open = wx.Button(panel,label='Transfer')
    bt_open . Bind(wx.EVT_BUTTON,Transfer)
    bt_save = wx.Button(panel,label='Load')
    bt_save.Bind(wx.EVT_BUTTON,Load)
    Transfer_content = wx.TextCtrl(panel)
    text_contents = wx.TextCtrl(panel,style=wx.TE_MULTILINE|wx.HSCROLL)
    bsizer_top = wx.BoxSizer()
    bsizer_top.Add(Transfer_content,proportion=1,flag=wx.EXPAND,border=5)
    bsizer_top.Add(bt_open,proportion=0,flag=wx.LEFT,border=5)
    bsizer_top.Add(bt_save,proportion=0,flag=wx.LEFT,border=5)

    bsizer_all = wx.BoxSizer(wx.VERTICAL)
    bsizer_all.Add(bsizer_top,proportion=0,flag=wx.EXPAND|wx.LEFT,border=5)
    bsizer_all.Add(text_contents,proportion=1,flag=wx.EXPAND|wx.ALL,border=5)

    panel.SetSizer(bsizer_all)

    win.Show()
    app.MainLoop()