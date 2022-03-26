from django.http.response import StreamingHttpResponse
from django.shortcuts import render
import cv2
import numpy as np
import threading 

cameraInputs = []

class Form():
    def __init__(self,ip,username,password,port,ishttp,link) -> None:
        self.Ip = ip
        self.Username = username
        self.Password = password
        self.Port = port
        self.Ishttp = ishttp
        self.Link = link

def home(request):
    return render(request,"index.html",{"Cam":str(len(cameraInputs))})
 
def stream1(request):
    if(len(cameraInputs)>0):
        cam = Capture(cameraInputs[0].Ip,cameraInputs[0].Username,cameraInputs[0].Password,cameraInputs[0].Port,cameraInputs[0].Ishttp,cameraInputs[0].Link)
        return StreamingHttpResponse(gen(cam),'multipart/x-mixed-replace;boundary=frame')

def stream2(request):
    if(len(cameraInputs)>1):
        cam = Capture(cameraInputs[1].Ip,cameraInputs[1].Username,cameraInputs[1].Password,cameraInputs[1].Port,cameraInputs[1].Ishttp,cameraInputs[1].Link)
        return StreamingHttpResponse(gen(cam),'multipart/x-mixed-replace;boundary=frame')

def stream3(request):
    if(len(cameraInputs)>2):
        cam = Capture(cameraInputs[2].Ip,cameraInputs[2].Username,cameraInputs[2].Password,cameraInputs[2].Port,cameraInputs[2].Ishttp,cameraInputs[2].Link)
        return StreamingHttpResponse(gen(cam),'multipart/x-mixed-replace;boundary=frame')

def stream4(request):
    if len(cameraInputs)>3:
        cam = Capture(cameraInputs[3].Ip,cameraInputs[3].Username,cameraInputs[3].Password,cameraInputs[3].Port,cameraInputs[3].Ishttp,cameraInputs[3].Link)
        return StreamingHttpResponse(gen(cam),'multipart/x-mixed-replace;boundary=frame')

def input(request):
    ip = request.POST['ip']
    username = request.POST['username']
    password = request.POST['password']
    port = request.POST['port']
    link = request.POST['link']
    print(request.POST['protocol'])
    ishttp = False
    if str(request.POST['protocol'])=="http_radio":
       ishttp = True    

    cam_no = request.POST['cams']
    if(len(cameraInputs)>int(cam_no[-1])):
        cameraInputs[int(cam_no[-1])] = Form(ip,username,password,port,ishttp,link)
    elif int(cam_no[-1])<5:
        cameraInputs.append(Form(ip,username,password,port,ishttp,link))
    return home(request)

class Capture():

    def __init__(self,ip,username,password,port,ishttp,link):

        url = ""
        print(str(ishttp)+" ishttp")
        if ishttp:
            url += "http://"
        else:
            url+="rtsp://"

        if(len(username)==0 or len(password)==0):
            print('username is zero')
            pass
        else:
            url+=username+":"+password+'@'

        url+=ip+':'+port+'/video'

        # change videocapture(0) to videocapture(url) if correct ip address is added
        self.cam = cv2.VideoCapture(url)

        (self.success,self.frame) = self.cam.read()
        if self.success ==True:
            threading.Thread(target=self.update,args=()).start()
        elif len(link)>10:
            self.cam = cv2.VideoCapture(link)
            (self.success,self.frame) = self.cam.read()
            if self.success ==True:
                threading.Thread(target=self.update,args=()).start()


    def __del__(self):
        self.cam.release()

    def get_frame(self):
        image = self.frame
        _,jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

    def update(self):    
        while True:
            (self.success,self.frame) = self.cam.read()

# this function generates the views and send this frames using yield to stream functions
def gen(camera):
    while True:
        frame = camera.get_frame()
        if(frame!=None):
            yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame+ b'\r\n\r\n')
