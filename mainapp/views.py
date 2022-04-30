from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

# Create your views here.
from mainapp import yolo

global pastFrame
def main(request):
    return render(request, 'index.html')

def learning(request):
    words = yolo.labels
    return render(request, 'learning.html',{'words': words})

def contact(request):
    return render(request, 'contact.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def portfolio_details(request):
    return render(request, 'portfolio-details.html')

def resume(request):
    return render(request, 'resume.html')

def services(request):
    return render(request, 'services.html')

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(1)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        image = yolo.detection(image)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_frame2(self):
        image = self.frame
        image = yolo.detection2(image)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gen2(camera):
    global pastFrame
    flag = True
    while True:
        if flag:
            frame = camera.get_frame()
            pastFrame = frame
            flag = False
        else:
            frame = pastFrame

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def detectme(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass
def detectme2(request):
    try:
        cam = VideoCamera()
        #return gen2(cam)
        return StreamingHttpResponse(gen2(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass

