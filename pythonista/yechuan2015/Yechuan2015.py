#coding: utf-8
import ui
import time
from random import randint, shuffle
import requests
actv = ui.ActivityIndicator()





def sendDanmaku(list_id, message, manual=False):
		if not manual:
			flashPool(list_id)
		mainScroll['lblCurrent'].text=message
		requests.post("http://cldds-danmu.herokuapp.com/post", data={"message": message,'master':1})


def indicateSpawn(view):
        def restoreColor():
                view.background_color=(1,1,1,1)
                view.alpha=1.0
        view.background_color=(1,0,0,1)
        view.alpha=0.2
        ui.animate(restoreColor, duration=0.5)


def flashPool(poll_id):
        indicateSpawn(mainScroll['lblPool'+str(poll_id+1)])


@ui.in_background
def sendAction(sender):
	v=sender.superview
	sendDanmaku(0, v['editMessage'].text, True)


@ui.in_background
def poolAction(sender):
        poolnum = int(sender.name[-1])-1
        if sender.value:
        	spawn(poolnum, sender)

@ui.in_background
def autospawn_click(sender):
        v=sender.superview
        if sender.value:
                actv.start()
                timeline=initSpawn()
                playTimeline(timeline, respawn, sendDanmaku, sender)
        else:
                actv.stop()


@ui.in_background
def spawnSlide(sender):
        sender.superview['lblSpawnRate'].text=str(round(sender.value*100)/10)+'s'


@ui.in_background
def loadSlide(sender):
        sender.superview['lblLoadRate'].text=str(round(sender.value*200)/10)+'s'


def spawn(list_id, list_control):
    def sleep(control, duration=1.0):
    	print duration
        sTime=time.time()
        cTime=time.time()
        while not cTime>=sTime+duration:
                cTime=time.time()
                if not control.value:
                	return False
        return True

    def randNext(i, len):
        return randint(0, len-1)

    def seqNext(i, len):
        if i>=len-1:
            return 0
        else:
            return i + 1

    v = list_control.superview
    rate = v["slSpawnRate"].value
    content = pools[list_id]["content"]
    length = len(content)
    if pools[list_id]['sequential']:
    	curPos=0
        inc_func = seqNext
    else:
    	curPos=randint(0, length-1)
        inc_func = randNext
    while list_control.value:
        sendDanmaku(list_id, content[curPos])
        curPos = inc_func(curPos, length)
        if not sleep(list_control, round(list_control.superview['slSpawnRate'].value*100)/10):
        	return


mainView=ui.load_view('Yechuan2015')
mainView.add_subview(actv)
mainScroll=mainView['scroll1']
mainScroll.add_subview(actv)
actv.y=mainScroll['lblAutospawn'].y+5
actv.x=mainScroll['lblAutospawn'].x+90

loadSlide(mainScroll['slLoadRate'])
spawnSlide(mainScroll['slSpawnRate'])
mainView.present()
