import threading
import random
import cv2
import json
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import gzip

# Create your views here.
from mainapp import yolo

from mainapp import models
from .models import Word
global pastFrame
def main(request):
    return render(request, 'index.html')

def learning(request):

    return render(request, 'learning.html')

def delete(request, id):
  w = Word.objects.get(id=id)
  w.delete()
  return render(request,'delete.html')

def ajax(request):
    words = yolo.labels
    context = {'words': words}
    response = json.dumps(context)

    words = yolo.labels
    for idx, val in enumerate(yolo.images):
        print(r"static"+"\\images\\" + words[idx] + ".png")
        cv2.imwrite(r"static"+"\\images\\" + words[idx] + ".png", val)
        physics = models.Word(word=yolo.labels[idx], images=r"static"+"\\images\\" + words[idx] + ".png")
        physics.save()

    #print(response)
    return HttpResponse(response)
    # return HttpResponse(json.dumps(data), content_type='application/json')

def game(request):
    wordList = models.Word.objects.all()
    wordList2 = Word.objects.order_by('?')[:5]
    outerStr = "["
    wList = [" ", " ", " "]
    nList = [" ", " ", " "]
    print(len(wordList))
    print(len(wordList2))
    for item in wordList2:
        tmpN = random.randint(0,10)
        wList[0] = wordList[random.randint(0, len(wordList)-1)].word
        wList[1] = wordList[random.randint(0, len(wordList)-1)].word
        wList[2] = item.word

        nList[(tmpN + 0) % 3] = wList[0]
        nList[(tmpN + 1) % 3] = wList[1]
        nList[(tmpN + 2) % 3] = wList[2]

        str = "{\n"
        str += "\"question\": \"" + item.word + "\",\n"
        str += "\"a\": \"" + nList[0] + "\",\n"
        str += "\"b\": \"" + nList[1] + "\",\n"
        str += "\"c\": \"" + nList[2] + "\",\n"
        str += "\"correct\": \""+chr(97+((tmpN + 2) % 3)) +"\"\n"
        str += "},\n"
        print(str)

        outerStr += str

    outerStr = outerStr[:-2]
    outerStr += "]"
    print("outer")
    print(outerStr)
    jTmp = json.loads(outerStr)
    print(jTmp)
    #words = jTmp
    context = {"words": jTmp}
    #print(context)

    return render(request, 'game.html', context)

def portfolio(request):
    return render(request, 'portfolio.html')

def portfolio_details(request):
    return render(request, 'portfolio-details.html')

def wordlist(request):
    context = {
        "words": models.Word.objects.all()
    }
    return render(request, 'wordlist.html', context)

def services(request):
    return render(request, 'services.html')

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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

