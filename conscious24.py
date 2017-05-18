# -*- coding: utf-8 -*-
""" conscious manager
Функционал программы
1 Осознание
Пауза для засыпания
Проверка на движение глаз
Subtopic
Пробуждение сознания
2 Напоминание
Регулярное напоминание/проверка
3 Связь
Режим ввода команд
Запуск приложений
  Выполнение заданий
	Пункты задания
Управление из сна
  Ответы на запросы
  Ввод текста
  Управление условиями
Программируемые действия по случаю
4 Лог сна
Вывод текстов
Запись движения глаз
Запись отданных команд
Регистрация случаев
Лог действий
5 Тестирование маски
Логика программы
Переменные
Время задержки начала работы в секундах time_wait_run=5
Таймер времени замера повторного движения глазами в секундах timer_rem=30
Счетчик движений глаз counter_eye_movement=0
Значение счетчика движений глазами для срабатывания функции пробуждения сознания counter_eye_limit=5
Run
Задержка начала работы программы в секундах wai time_wait_ru secs
Установить сптайт в положение мышки go to x:mousex y:mouse y
Выполнять всегда
Установить счетчик движений глазами в 0
Если есть движение мышки, то есть спрайт не в положении мышки if not mousex=x position or not mouse y = y position
  Да
	Сбросить таймер
	Повторять пока работает таймер значение счетчика движения глазами будет равно значению установленного предела. repeat until timer<timer_rem
	  Да, таймер работает, предел значения движения глазами не достигнут
		Если есть движение мышки
		  ДА
			Установить спрайт в положение мышки
			Добавить +1 к значению счетчика движений глазами
		Ждать 1 секунду
	  Нет
		Таймер выполнил круг и значение замера повторного движения глаз не достигло предела. Переход в начало программы
	Если значение счетчика движения глаз достигло значения лимита
  Нет
	Следить за мышкой
Interface программы
Мeню
Файл
Открыть
Вид
Настройки
Помощь
# Программа
imports """
import Tkinter
from Tkinter import *
import tkMessageBox
import tkFileDialog
import thread
import time
import random
import RPi.GPIO as GPIO
# import sqlite3
import autopy
# variables
# gpio
outPins = [ 11, 12, 13]
buttonsPins = [ 33, 40, 18]
# leds
greenled = 11
blueled = 12
redled = 13
# vibration motor
vibromotor = 29
# external buttons
buttonGpio = 18
buttonGpio1 = 33
buttonGpio2 = 40
# status external buttons
oncePressedB0=0
# timer variables
timerOn=0
timerEvent=0
timerStop=0
# script flags
mainStart=0
run=0
firstRun=0
# variables for tracking eyes
noRemEyeMoves=7 # moving mouse pointer in pixels
limitCounterEyeMovement=5
counterEyeMovement=0
timeCheckRepeatEyeMovement=1
trackTimeEyeMoves=20
eyeMovesOn=0
# lucid
intoLucidEvent=0
lucid=0
awakingLucid=10
lucidTimerON=0
lucidTimerStop=0
lucidTimerEvent=0
lucidAnswerOn=0
#lastLed=0
# blinks
awakingBlinksOn=0
countAwakingBlinks=21
stepAwakingBlinks=0
lastCycleBlinks=2
# answer variables
doneMoveAnswerEvent=3
answerYesGo=0
# answer yes
yAnswerEvent=0
yMoveAnswerEvent=0
yAnswerOn=0
yMoveAnswerEvent=0
yAnswerOn=0
yMoveAnswerEvent=0
yesMoveLimit=5
# answer no
xAnswerEvent=0
xMoveAnswerEvent=0
xAnswerOn=0
xMoveAnswerEvent=0
xAnswerOn=0
xMoveAnswerEvent=0
# check answerYes
timeCheckAnswerYes=10
checkAnswerYesOn=0
lucidAnswerAwakingBlinks=0
# mouse tracking variables
centerPosX=300
centerPosY=300
yposition=centerPosY
mouseY=centerPosY
xposition=centerPosX
mouseX=centerPosX
counterMouseCenterSet=0
mouseCenterSetOn=0
# run triggers
timeBetweenDreams=600
# set time until runin seconds
timeUntilRun = 100
# bug checking
awBl=0
blwhile=0
# functions
# gpio
def gpioOuts():
  # led pins gpio setup
  global outPins
  global buttonsPins
  GPIO.setmode(GPIO.BOARD)
  for a in outPins:
    GPIO.setup(a, GPIO.OUT) # set led pins to out
    GPIO.output (a, 0) # set leds off
  # buttons
  for b in buttonsPins:
    GPIO.setup(buttonsPins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def gpioButtons():
  GPIO.setmode(GPIO.BOARD)
  for b in buttonsPins:
    GPIO.setup(buttonsPins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# blinks
def slowblink(led, freq, blinks, power):
  p = GPIO.PWM (led, freq)
  p.start(0)
  for k in range (blinks):
    for i in range (power):
      p.ChangeDutyCycle(i)
      time.sleep(0.02)
    for i in range (power):
      p.ChangeDutyCycle(power-i)
      time.sleep(0.02)
  p.stop()
def ledblink (led,blinktimes,freq,cdc,ontime,offtime):
  #led=11
  if led==11:
    freq=100
    cdc=100
  p = GPIO.PWM (led, freq)
  #ontimes=int (round(ontime/0.02))
  #print "ontimes = ", ontimes
  p.start(0)
  for c in range (blinktimes):
    p.ChangeDutyCycle(cdc)
    time.sleep (ontime)
  p.ChangeDutyCycle(0)
  time.sleep (offtime)
  p.stop()
def startLedBlinks():
  global outPins
  global mainStart
  mainStart=mainStart+1
  print "start new main cycle", mainStart
  for a in outPins:
    ledblink(a,1,100,1,0.5,0)
def lucidLedBlinks(lblinktimes,lfreq,lcdc,lontime,lofftime):
  #ledblink (led,blinktimes,freq,cdc,ontime,offtime)
  global run
  global lucid
  global outPins
  #global lastLed
  lled=11
  #lled=random.choice(outPins)
  #while lastLed==lled:
    #lled=random.choice(outPins)
  #lastLed=lled  
  ledblink (lled,lblinktimes,lfreq,lcdc,lontime,lofftime)
def awakingBlinks():
  global run
  global lucidAnswerOn
  global lucid
  global timerOn
  global awakingBlinksOn
  global lucid
  global countAwakingBlinks
  global stepAwakingBlinks
  global awBl
  global blwhile
  global lastCycleBlinks
  awakingBlinksOn=1
  awBl=awBl+1
  countLastCycleBlinks=0
  print "awaking blinks inside start =", awBl
  print "lucid =", lucid
  print "run =", run
  print "stepAwakingBlinks =", stepAwakingBlinks
  stepAwakingBlinks=0
  a=int(round(countAwakingBlinks/3))
  b=int(round(countAwakingBlinks/4*3))
  #lucidLedBlinks(lblinktimes,lfreq,lcdc,lontime,lofftime)
  while run==1 and lucid==0 and awakingBlinksOn==1:
    blwhile=blwhile+1
    time.sleep(2)
    print "awakingBlinks inside while", blwhile
    for i in range (stepAwakingBlinks, countAwakingBlinks):
      stepAwakingBlinks=stepAwakingBlinks+1
      print "awaking blinks", stepAwakingBlinks
      time.sleep(1)
      if awakingBlinksOn==0 or lucid==1 or run!=1:
	print "awakingBlinks before in to return awakingBlinksOn=", awakingBlinksOn
	print "awakingBlinks before in to return lucid=", lucid
	print "awakingBlinks before in to return run=", run
	i=0
	stepAwakingBlinks=0
	return

      if stepAwakingBlinks<=a:
	print "stepAwakingBlinks<a", stepAwakingBlinks
	lucidLedBlinks(1,200,1,1,3)
      if stepAwakingBlinks>a and stepAwakingBlinks<b:
	print "stepAwakingBlinks>a <b", stepAwakingBlinks
	lucidLedBlinks(1,100,5,1,2)
      if stepAwakingBlinks>=b and stepAwakingBlinks<=countAwakingBlinks:
	print "stepAwakingBlinks==b", stepAwakingBlinks
	lucidLedBlinks(1,100,10,0.5,1)
      if stepAwakingBlinks>=countAwakingBlinks:
	print "awaking blinks cycle done"
	stepAwakingBlinks=b
	countLastCycleBlinks=countLastCycleBlinks+1
	#awakingBlinksOn=0
      if countLastCycleBlinks==lastCycleBlinks:
	return
	
def awakingBlinks2():
  global run
  global lucidAnswerOn
  global lucid
  global timerOn
  global awakingBlinksOn
  global lucid
  global countAwakingBlinks
  global stepAwakingBlinks
  global awBl
  global blwhile
  global lastCycleBlinks
  awakingBlinksOn=1
  awBl=awBl+1
  countLastCycleBlinks=0
  print "awaking blinks inside start =", awBl
  print "lucid =", lucid
  print "run =", run
  print "stepAwakingBlinks =", stepAwakingBlinks
  stepAwakingBlinks=0
  a=int(round(countAwakingBlinks/3))
  b=int(round(countAwakingBlinks/4*3))
  # lucidLedBlinks(lblinktimes,lfreq,lcdc,lontime,lofftime)
  while run==1 and lucid==0 and awakingBlinksOn==1:
    blwhile=blwhile+1
    time.sleep(1)
    print "awakingBlinks inside while", blwhile
    if awakingBlinksOn==0 or lucid==1 or run!=1:
      i=0
      stepAwakingBlinks=0
      awBl=0
      print "awakingBlinksOn==0 return event"
      return
    #startLedBlinks()
# mouse positions
def mouseCenterSet():
  global run
  global mouseX
  global mouseY
  global xposition
  global ypostion
  global counterMouseCenterSet
  global mouseCenterSetOn
  xposition=mouseX
  yposition=mouseY
  while run==1 and mouseCenterSetOn==1:
    #print "mouseX=", mouseX
    #print "mouseY=", mouseY
    if mouseCenterSetOn==0:
      print "mouseCenterSetOn return event mouseCenterSet=",mouseCenterSetOn
      return
    if mouseX > 600 or mouseX < 100 or mouseY > 600 or mouseY < 100:
      print "mouse center set xposition before if =", xposition
      print "mouse center set yposition before if =", yposition
      autopy.mouse.move(300,300)
      yposition=mouseY
      xposition=mouseX
      print "mouse center set xposition if =", xposition
      print "mouse center set yposition if =", yposition
      #ledblink(redled,1,100,1,1,0.5)
      time.sleep (10)
      counterMouseCenterSet=counterMouseCenterSet+1
      print "counterMouseCenterSet =", counterMouseCenterSet
    else:
      time.sleep (1)
  mouseCenterSetOn=0
def setInMousePosition(setM=0):
  global yposition
  global mouseY
  global xposition
  global mouseX
  if setM!=0:
    autopy.mouse.smooth_move(300,300)
  xposition=mouseX
  yposition=mouseY
# check true move eyes
def checkMove (check1position,check2position,limitMove):
  checkMove=check1position-check2position
  print "eyeMove 1 checkMove=", checkMove
  cM=cmp(checkMove,0)
  print "eyeMove cM=", cM
  if cM==-1:
    checkMove=-checkMove
  print "eyeMove 2 checkMove=", checkMove
  if checkMove>limitMove:
    print "checkMove return 1"
    return 1
  else:
    print "checkMove return 0"
    return 0
#проверка движений глазами
def eyeMoves():
  global run
  global yposition
  global mouseY
  global xposition
  global mouseX
  global timerEvent
  global trackTimeEyeMoves
  global counterEyeMovement
  global limitCounterEyeMovement
  global timeCheckRepeatEyeMovement
  global intoLucidEvent
  global timerOn
  global timerStop
  global oncePressedB0
  intoLucidEvent=0
  setInMousePosition(1,)
  setInMousePosition()
  counterEyeMovement=0
  #ledblink (greenled,1,100,5,0.5,0.5)
  while run==1 and intoLucidEvent==0 and counterEyeMovement!=limitCounterEyeMovement:
    if xposition==mouseX or yposition==mouseY:
      time.sleep(timeCheckRepeatEyeMovement)
    else:
      #checkMove(check1position,check2position,limitMove)
      xCheck=checkMove(xposition,mouseX,noRemEyeMoves)
      yCheck=checkMove(yposition,mouseY,noRemEyeMoves)
      if xCheck==1 or yCheck==1:
	counterEyeMovement=counterEyeMovement+1
	print "first counterEyeMovement", counterEyeMovement
	#mouseCenterSet()
	setInMousePosition()
	time.sleep(1)
	print "timerEvent =", timerEvent
	print "intoLucidEvent", intoLucidEvent
	if timerOn==0 and counterEyeMovement>=1:
	  print "start eye movement timer"
	  thread.start_new_thread(timer, (trackTimeEyeMoves,))
      else:
	setInMousePosition()
	time.sleep(1)
    if counterEyeMovement==limitCounterEyeMovement:
      print "start intoLucid start event = 1"
      intoLucidEvent=1
      thread.start_new_thread(intoLucid,())
      timerStop=1
      counterEyeMovement=0
      timerOn=0
    if timerEvent==1 and counterEyeMovement!=limitCounterEyeMovement:
      counterEyeMovement=0
      print "final counterEyeMovement =", counterEyeMovement
      print "timerEvent = 1, set timerEvent = 0"
      print "timerOn = ", timerOn
      timerEvent=0
  counterEyeMovement=0
# осознание
def intoLucid():
  global run
  global lucid
  global timerEvent
  global yAnswerOn
  global lucidAnswerOn
  global intoLucidEvent
  lucidAnswerOn=0
  timerOn=0
  awakingBlinksOn=0
  lucid=0
  answer=0
  print "intoLucid inside start"
  lucidAnswer()
def lucidAnswer():
  global lucidAnswerOn
  global run
  global lucidTimerON
  global yAnswerOn
  global lucid
  global yAnswerEvent
  global yMoveAnswerEvent
  global awakingBlinksOn
  global countAwakingBlinks
  global yAnswerEvent
  global timeBetweenDreams
  global stepAwakingBlinks
  global lucidAnswerAwakingBlinks
  global checkAnswerYesOn
  lucidAnswerOn=1
  o=0
  l=0
  t=0
  lucidAnswerAwakingBlinks=0
  print "lucidAnswer start"
  if awakingBlinksOn==0 and yAnswerEvent==0 and lucid==0 and lucidAnswerAwakingBlinks==0:
    lucidAnswerAwakingBlinks=lucidAnswerAwakingBlinks+1
    t=t+1
    print "lucidAnswer awakingBlinks start = ", t
    thread.start_new_thread(awakingBlinks,())
  if checkAnswerYesOn==0:
    checkAnswerYesOn=1
    o=o+1
    print "start checkAnswerYes =",o
    thread.start_new_thread(checkAnswerYes,())
  if yAnswerOn==0 and yAnswerEvent==0:
    yAnswerOn=1
    l=l+1
    print "start answerYes =", l
    thread.start_new_thread(answerYes,())
  time.sleep(3)
  onceYAnswerEvent=0
  while run==1 and lucid==0:
    if  yAnswerEvent!=0:
      onceYAnswerEvent=onceYAnswerEvent+1
      print "lucid dream in action"
      #ledblink (led,blinktimes,freq,cdc,ontime,offtime)
      lucid=1
      awakingBlinksOn=0
      stepAwakingBlinks=0
      stopAll()
      time.sleep (2)
      #ledblink (greenled,3,100,5,1,0.5)
      timer(timeBetweenDreams)
      lucidAnswerOn=0
      stepAwakingBlinks=0
      yAnswerOn=0
      yAnswerEvent=0
      lucidAnswerAwakingBlinks=0
      GPIO.cleanup()
      gpioOuts()
      mainThreadRuns()
      """elif onceYAnswerEvent>1:
	print "onceYAnswerEvent=",onceYAnswerEvent"""
# answers
def checkAnswerYes():
  global awakingBlinksOn
  global yMoveAnswerEvent
  global yAnswerEvent
  global yAnswerOn
  global timeCheckAnswerYes
  global checkAnswerYesOn
  global awakingBlinksOn
  global lucid
  global answerYesGo
  checkAnswerYesOn=1
  print "checkAnswerYes init def checkAnswerYesOn", checkAnswerYesOn
  print "checkAnswerYes init def yAnswerEvent", yAnswerEvent
  e=0
  g=0
  while run==1 and checkAnswerYesOn==1 and yAnswerEvent==0:
    print "checkAnswerYes while awakingBlinksOn", awakingBlinksOn
    print "checkAnswerYes while yAnswerEvent", yAnswerEvent
    print "checkAnswerYes while answerYesGo=", answerYesGo
    if answerYesGo==1 and awakingBlinksOn==1:
      e=e+1
      print "checkAnswerYes start",e
      u=0
      awakingBlinksOn=0
      for u in range (0, timeCheckAnswerYes):
	if checkAnswerYesOn==0 or run!=1 or yAnswerEvent==1:
	  return
	print "timeCheckAnswerYes=",timeCheckAnswerYes-u
	time.sleep(1)
      answerYesGo=0
      print "yAnswerOn 2 checkAnswerYes=", yAnswerOn
      print "yAnswerEvent 2 checkAnswerYes=", yAnswerEvent
      print "awakingBlinksOn 2 checkAnswerYes=", awakingBlinksOn
      if yAnswerOn==1 and yAnswerEvent==0 and awakingBlinksOn==0 and lucid==0:
	awakingBlinksOn=1
	g=g+1
	print "checkAnswerYes continue awakingBlinks",g
	thread.start_new_thread(awakingBlinks,())
    else:
      print "check answer Yes else"
      time.sleep(1)      
  checkAnswerYesOn=0
  print "checkAnswerYes exit yAnswerEvent", yAnswerEvent
def answerYes():
  global run
  global yposition
  global mouseY
  global xposition
  global mouseX
  global yAnswerEvent
  global yMoveAnswerEvent
  global doneMoveAnswerEvent
  global yAnswerOn
  global lucid
  global answerYesGo
  global yesMoveLimit
  #global awakingBlinksOn
  yMoveAnswerEvent=0
  yAnswerOn=1
  yAnswerEvent=0
  while run ==1 and yAnswerEvent==0 and yAnswerOn==1:
    if yposition==mouseY:
      time.sleep(0.5)
    elif yposition>mouseY:
      yesCheck=checkMove(yposition,mouseY,yesMoveLimit)
      if yesCheck==1:
	answerYesGo=1
	print "answerYesGo answerYes=", answerYesGo
	yMoveAnswerEvent=yMoveAnswerEvent+1
	setInMousePosition()
	ledblink (greenled,1,100,20,0.5,0.5)
	print "yMoveAnswerEvent 1=", yMoveAnswerEvent
	time.sleep(0.5)
      else:
	setInMousePosition()
	time.sleep(0.5)
    else:
      setInMousePosition()
      #ledblink (blueled,1,100,1,0.5,0.5)
      time.sleep(0.5)
      print "yposition!=mouseY else"
    while yMoveAnswerEvent==1:
      if yposition<mouseY:
	yesCheck=checkMove(yposition,mouseY,yesMoveLimit)
	if yesCheck==1:
	  yMoveAnswerEvent=yMoveAnswerEvent+1
	  setInMousePosition()
	  ledblink (greenled,1,100,20,0.5,0.5)
	  print "yMoveAnswerEvent 2 =", yMoveAnswerEvent
	  time.sleep(0.5)
	else:
	  setInMousePosition()
	  yMoveAnswerEvent=0
	  #ledblink (redled,1,100,2,0.5,0.5)
	  time.sleep(0.5)
      else:
	setInMousePosition()
	#ledblink (redled,1,100,2,0.5,0.5)
	yMoveAnswerEvent=0
	time.sleep(0.5)
	print "while yMoveAnswerEvent==1 else"
    while yMoveAnswerEvent==2:
      if yposition>mouseY:
	yesCheck=checkMove(yposition,mouseY,yesMoveLimit)
	if yesCheck==1:
	  answerYesGo=1
	  yMoveAnswerEvent=yMoveAnswerEvent+1
	  setInMousePosition()
	  ledblink (greenled,1,100,20,0.5,0.5)
	  print "yMoveAnswerEvent 3 =", yMoveAnswerEvent
	  time.sleep(0.5)
	else:
	  setInMousePosition()
	  yMoveAnswerEvent=0
	  #ledblink (redled,1,100,2,0.5,0.5)
	  time.sleep(0.5)
      else:
	setInMousePosition()
	#ledblink (redled,1,100,2,0.5,0.5)
	yMoveAnswerEvent=0
	time.sleep(0.5)
	print "while yMoveAnswerEvent==2 else"
      if yMoveAnswerEvent>=3:
	print "last yMoveAnswerEvent=", yMoveAnswerEvent
	yAnswerEvent=1
  yAnswerOn=0
  yMoveAnswerEvent=0
  answerYesGo=0

# mouse moves
def mouseXmoves():
  global run
  global xposition
  global mouseX
  xposition=mouseX
  while run==1:
    if xposition==mouseX:
      time.sleep(0.05)
      #print "mouseX dont move"
      #print('x= {},y= {}'.format(mouseX, mouseY ))
      #print "xposition", xposition
      #print "yposition", yposition
    if xposition>mouseX:
      ledblink(greenled,1,100,10,1,0.5)
      time.sleep(0.05)
      #print "xposition>mouseX"
      #print('x= {},y= {}'.format(mouseX, mouseY ))
      #print "xposition", xposition
      #print "yposition", yposition
      xposition=mouseX
    if xposition<mouseX:
      ledblink(greenled,1,100,10,1,0.5)
      time.sleep(0.05)
      #print "xposition<mouseX"
      #print('x= {},y= {}'.format(mouseX, mouseY ))
      #print "xposition", xposition
      #print "yposition", yposition
      xposition=mouseX
    #mouseCenterSet()
def mouseYmoves():
  global run
  global yposition
  global mouseY
  yposition=mouseY
  while run==1:
    if yposition==mouseY:
      time.sleep(0.05)
      #print "mouseY dont move"
      #print('x= {},y= {}'.format(mouseX, mouseY ))
      #print "yposition", yposition
    if yposition>mouseY:
      # ledblink (led,blinktimes,freq,cdc,ontime,offtime)
      #ledblink(blueled,1,100,1,1,0.5)
      time.sleep(0.05)
      #print "yposition>mouseY"
      #print('x= {},y= {}'.format(mouseX, mouseY ))
      #print "yposition", yposition
      yposition=mouseY
    if yposition<mouseY:
      #ledblink(blueled,1,100,1,1,0.5)
      time.sleep(0.05)
      #print "yposition<mouseY"
      #print('x= {},y= {}'.format(mouseX, mouseY ))
      #print "yposition", yposition
      yposition=mouseY
    #mouseCenterSet()
# timer functions
def timer (timerTime,hideTimer=0):
  global run
  global timerOn
  global timerStop
  global timerEvent
  timerStop=0
  timerOn=1
  print "timerOn init timer = ", timerOn
  timerEvent=0
  #while run==1 and timerStop==0:
  for i in range (0, timerTime):
    if timerStop==1 or run!=1:
      timerStop=0
      timerOn=0
      print "return event timer"
      return
    if hideTimer==0:
      print "timer is ",timerTime-i
    time.sleep(1) 
  timerEvent=1
  timerStop=0
  timerOn=0
  print "timerOn = ", timerOn# lucidtimer function
def lucidTimer (lucidTimerTime):
  global run
  global lucidTimerON
  global lucidTimerStop
  global lucidTimerEvent
  global lucid
  lucidTimerEvent=0
  lucidTimerStop=0
  lucidTimerON=1
  print "lucidTimerOn = 1"
  while run==1 and lucidTimerStop==0:
    for i in range (0, lucidTimerTime):
      if lucidTimerStop==1 or run!=1 or lucid==1:
	return
      print "lucid timer",lucidTimerTime-i
      time.sleep(1)
    lucidTimerON=0
    lucidTimerStop=1
    lucidTimerEvent=1
    print "lucidTimerOn = 0"
# buttons functions
def check_button():
  global oncePressedB0
  if (GPIO.input(buttonGpio) == GPIO.LOW):
    if oncePressedB0==0:
      oncePressedB0=1
      mainThreadRuns()
  root.after(10,check_button)
  # global oncePressedB0==1
def check_button1():
  global oncePressedB0
  global timerStop
  global timerOn
  if (GPIO.input(buttonGpio1) == GPIO.LOW):
    oncePressedB0=0
    timerStop=1
    timerOn=0
    stopAll()
  root.after(11,check_button1)
def check_button2():
  if (GPIO.input(buttonGpio2) == GPIO.LOW):
    #startLedBlinks()
    doNothing()
  root.after(12,check_button2)
# запуск первых mултизадач
def mainThreadRuns():
  global timeUntilRun # 0=10
  global lucid # 0=0
  global run # 0=0
  global mouseCenterSetOn #0=0
  global firstRun #0=0
  global eyeMovesOn
  #autopy.mouse.move(300,300)
  lucid =0
  run=1
  gpioOuts()
  #startLedBlinks()
  if mouseCenterSetOn==0:
    mouseCenterSetOn=1
    thread.start_new_thread(mouseCenterSet,())
    time.sleep(1)
  if firstRun==0:
    timer(timeUntilRun,1)
  firstRun=firstRun+1
  print "firstRun =", firstRun  
  if eyeMovesOn==0:
    thread.start_new_thread(eyeMoves,())
  #thread.start_new_thread(timer, (120,))
# функция  остановки и сброса
def stopAll():
  global run
  global intoLucidEvent
  global lucidAnswerOn
  global yAnswerEvent
  global awakingBlinksOn
  global lucid
  if run==1:
    run=0
    intoLucidEvent=0
    lucid=0
    lucidAnswerOn=0
    yAnswerEvent=0
    awakingBlinksOn=0
    print 'stop all threadings'
    #ledblink (redled,3,100,1,1,0.5)
    #GPIO.cleanup()
    #check_button()
# функция определения местоположения курсора мыши
def mousetrack(event):
  global mouseX
  global mouseY
  mouseX, mouseY  = event.x, event.y
  #print('x= {},y= {}'.format(mouseX, mouseY ))
# функция по нажатию любой клавиши
def onKeyPress(event):
  global run
  run=0
  check_button()
  print "treads stoped by pressing key"
  print 'you pressed %s\n' % (event.char)
# quit function
def mQuit():
  mExit = tkMessageBox.askokcancel(title="Quit", message="Are you sure?")
  if mExit > 0:
    GPIO.cleanup()
    root.destroy()
    return
# функция ничего
def doNothing():
  print("doNothing")
# main execution
gpioOuts()
#ledblink(blueled,1,100,1,3,1)
# часть Tkinter
root = Tkinter.Tk()
root.title("Conscious")
root.geometry('800x700+0+0')
#menu
menu = Menu(root)
root.config(menu=menu)
#Main menu items
fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
viewMenu = Menu(menu)
menu.add_cascade(label="View", menu=viewMenu)
recordsMenu = Menu(menu)
menu.add_cascade(label="Records", menu=recordsMenu)
settingsMenu = Menu(menu)
menu.add_cascade(label="Settings", menu=settingsMenu)
helpMenu = Menu(menu)
# menu file items
fileMenu.add_command(label="Open", command=doNothing)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=mQuit)
# menu view items
viewMenu.add_command(label="Status bar", command=doNothing)
# menu records items
recordsMenu.add_command(label="Calendar", command=doNothing)
recordsMenu.add_command(label="Logs", command=doNothing)
# menu settings items
settingsMenu.add_command(label="Options", command=doNothing)
settingsMenu.add_command(label="Load", command=doNothing)
settingsMenu.add_command(label="Save", command=doNothing)
# menu help items
helpMenu.add_command(label="About", command=doNothing)
menu.add_cascade(label="Help", menu=helpMenu)
root.bind('<KeyPress>', onKeyPress)
root.bind('<Motion>', mousetrack)
root.after(10,check_button)
root.after(11,check_button1)
root.after(12,check_button2)
root.mainloop()
""" # Legend
глобальные переменные
определение переменных 
#комментарии
параллельные задачи
function with action
function with return
операция while
операция if 
операция elif
операция else
return
библиотечные функции
внутренние функции
blink функции
interactiva функции
тело внутренней функции
print
tkinter
"""
