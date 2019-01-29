import RPi.GPIO as GPIO
from pygame import mixer
import time
import random


#set I/O to appropriate pin numbers
# TODO change all buttons to correct pi numbers
playBtn=22
backBtn=18
fowardBtn=16
playlistNum=1
led=32
lastSong = ""
currentSong = "/home/pi/Music/slowChill/lofiMix.mp3"

#set all playlists to appropriate file paths
slowChill = ["/home/pi/Music/slowChill/blueLines.mp3", 
            "/home/pi/Music/slowChill/heligoland.mp3",
			"/home/pi/Music/slowChill/lofiMix.mp3",
			"/home/pi/Music/slowChill/mezzanine.mp3",
			"/home/pi/Music/slowChill/protection.mp3"]
			
upbeatChill = ["/home/pi/Music/upbeatChill/40oz.mp3",
              "/home/pi/Music/upbeatChill/currents.mp3",
			  "/home/pi/Music/upbeatChill/reggaeMix.mp3",
			  "/home/pi/Music/upbeatChill/am.mp3",
			  "/home/pi/Music/upbeatChill/sublime.mp3"]
			  
metal = ["/home/pi/Music/metal/andJusticeForAll.mp3",
		"/home/pi/Music/metal/farBeyondDriven.mp3",
		"/home/pi/Music/metal/iowa.mp3",
		"/home/pi/Music/metal/load.mp3",
        "/home/pi/Music/metal/masterOfPuppets.mp3",
		"/home/pi/Music/metal/metallica.mp3",
		"/home/pi/Music/metal/reignInBlood.mp3",
		"/home/pi/Music/metal/selvesWeCannotForgive.mp3",
		"/home/pi/Music/metal/slipknot.mp3",
		"/home/pi/Music/metal/subliminalVerses.mp3"]
		
progRock = ["/home/pi/Music/progRock/10000days.mp3",
           "/home/pi/Music/progRock/aenima.mp3",
		   "/home/pi/Music/progRock/deloused.mp3",
		   "/home/pi/Music/progRock/lateralus.mp3",
		   "/home/pi/Music/progRock/theWall.mp3",
		   "/home/pi/Music/progRock/wishYouWereHere.mp3",
		   "/home/pi/Music/progRock/undertow.mp3"]

def selectPlaylist(playlistNum):
	lastSong = currentSong
	while true:
		if playlistNum == 1:
			currentSong = random.choice(slowChill)
		
		elif playlistNum == 2:
			currentSong = random.choice(upbeatChill)
		
		elif playlistNum == 3:
			currentSong = random.choice(metal)
		
		elif playlistNum == 4:
			currentSong = random.choice(progRock)
			
		if currentSong != lastSong:
			break
			
	mixer.music.load(currentSong)
		
	mixer.music.play(-1)
	mixer.music.pause()
    print("song is at " + currentSong)
	return

#initializes pygame mixer
mixer.init()
selectPlaylist(playlistNum)

#GPIO SETUP
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(playBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(backBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(forwardBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Turns button LED off
GPIO.output(led, 0)

while True:
    playBtnPressed = not GPIO.input(playBtn)
    backBtnPressed = not GPIO.input(backBtn)
	forwardBtnPressed = not GPIO.input(forwardBtn)


    #If main button is pressed
    if playBtnPressed and not mixer.music.get_busy():
        print('Song playing')
        songPlaying=True
        GPIO.output(led, 1)
        mixer.music.unpause()
        time.sleep(1)

    elif playBtnPressed and mixer.music.get_busy():
        print('Song stopped')
        songPlaying=False
        GPIO.output(led, 0)
        mixer.music.pause()
        time.sleep(1)
				
				
    #If switch pressed
    if forwardBtnPressed:
            
        if playlistNum >= 4:
            playlistNum = 1
		else:
			playlistNum += 1
				
        time.sleep(.4)
		selectPlaylist(playlistNum)
				
	if backBtnPressed:
	    if playlistNum <= 1:
			playlistNum = 4
		else:
			playlistNum -= 1
        time.sleep(.4)
		selectPlaylist(playlistNum)
		

