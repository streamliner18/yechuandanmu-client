# -*- coding: utf-8 -*-
import time
from random import randint, shuffle
import requests
from pools import pools


def sendDanmaku(list_id, message):
        print "From list %d, message: %s" % (list_id, message)
        requests.post(
            "http://cldds-danmu.herokuapp.com/post",
            data={"message": message, "master": 1}
            )


def spawn(list_id):
    def sleep(duration=1.0):
        sTime = time.time()
        cTime = time.time()
        while not cTime >= sTime+duration:
                cTime = time.time()

    def randNext(i, len):
        return randint(0, len-1)

    def seqNext(i, len):
        if i >= len-1:
            return 0
        else:
            return i + 1
    rate = 1.2
    content = pools[list_id]["content"]
    length = len(content)
    curPos = 0
    if pools[list_id]["sequential"]:
        inc_func = seqNext
    else:
        inc_func = randNext
    while True:
        sendDanmaku(list_id, content[curPos])
        curPos = inc_func(curPos, length)
