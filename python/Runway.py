################################################################################
# Copyright (C) 2012 Leap Motion, Inc. All rights reserved.                    #
# NOTICE: This developer release of Leap Motion, Inc. software is confidential #
# and intended for very limited distribution. Parties using this software must #
# accept the SDK Agreement prior to obtaining this software and related tools. #
# This software is subject to copyright.                                       #
################################################################################

################################################################################
# Modified to add Socket Server and output functions by: Robert M. Hall, II    #
# 11/27/2012 - http://www.impossibilities.com/ - Version 00.1a				   #
################################################################################

import Leap, sys, math
import socket
import time
from thread import *

HOST = ''
PORT = 8888
	
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def setUpSocketServer():

	lastInfo = ''
	lastFrameID = ''

	global frameID
	global allData
	
	print  'Socket Created'
	
	try:
		s.bind((HOST, PORT))
	except socket.error , msg:
		print 'Bind Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	
	print 'Socket BIND Complete'
	
	s.listen(10)
	print 'Socket Now Listening'
		
		#now keep talking with the client
	while 1:
		#wait to accept a connection - blocking call
		conn, addr = s.accept()
				
		# Create a sample listener and assign it to a controller to receive events
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		
		telemetryInfo = ''
		frameID = ''
		lastFrameID = ''
		allData = ''
		
		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientthread ,(conn,))
		
		listener = LeapListener()
  		controller = Leap.Controller(listener)

  		time.sleep(1);
  		while 1:
  				
  				telemetryInfo=''
				if (frameID != lastFrameID and lastInfo != allData):
					telemetryInfo = allData
  				
					if(allData != ""):
						conn.sendall(telemetryInfo+"\n")
  					
				lastInfo = telemetryInfo
				lastFrameID = frameID
				time.sleep(0.02)

	s.close()
	
#Function for handling connections. This will be used to create threads
def clientthread(conn):

    #Sending message to connected client
    conn.send('CONNECTED') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        time.sleep(0.1)
        #Receiving from client
        data = conn.recv(1024)
        reply = data; #.strip();
                
        print '"'+reply+'"'
        
        if not data:
            break
            
        if (reply == 'INFO'):
			reply = 'OK'		
     
        conn.sendall(reply)
     
    #came out of loop
    conn.close()

class LeapListener(Leap.Listener):

	def onInit(self, controller):
		print "LEAP Initialized"

	def onConnect(self, controller):
		print "LEAP Connected"

	def onDisconnect(self, controller):
		print "LEAP Disconnected"

	def onFrame(self, controller):
		global frameID
		global allData

		allData = ''	
		frame = controller.frame()
		hands = frame.hands()
		numHands = len(hands)
		handCnt = 0
		frameID = frame.id()
		
		#BEGIN jsonData
		jsonData = ''
		jsonData =  '{ "frame":{ '
		jsonData += '"id":'+str(frame.id())+','
		jsonData += '"timestamp":'+str(frame.timestamp())+','
		
		#BEGIN HANDS
		if numHands >= 1:
		 
			jsonData += '"hands": '
			# Get the hands!
			#for hand in hands:
			handCnt+=1
			hand = hands[0]
			normal = hand.normal()		  
	  
			jsonData += '{"id":'+str(hand.id())+','
			jsonData += '"normal":{'
			if normal is not None:
				jsonData += '"x":'+str(normal.x)+','
				jsonData += '"y":'+str(normal.y)+','
				jsonData += '"z":'+str(normal.z)
			jsonData += '},'
	  
			#BEGIN FINGERS
			jsonData += generateFingerData(hand, handCnt, numHands)
			#END FINGERS
			
			#BEGIN PALM
			jsonData += generatePalmData(hand, handCnt, numHands)
			#END PALM	
		 
			jsonData += '}}, "state":"frame" }'
		   
			allData = jsonData
		
		else:
			jsonData += '"hands": null }, "state":"frame" }'
			allData = jsonData
	
def generateFingerData(hand, handCnt, numHands):
	
	fingers = hand.fingers()
	numFingers = len(fingers)
	fingerCnt = 0

	if numFingers >= 1:
		fingerData = '"fingers":[ '
		pos = Leap.Vector(0, 0, 0)
		dir = Leap.Vector(0, 0, 0)
		
		for finger in fingers:
			tip = finger.tip()
			id = finger.id()
			width = finger.width()
			pos.x = tip.position.x
			pos.y = tip.position.y
			pos.z = tip.position.z
			velocity = finger.velocity()
        	  
			fingerData += '{ "id":'+str(id)+','
			fingerData += '"isTool": "'+str(finger.isTool())+'",'
			fingerData += '"length":'+str(finger.length())+','
			fingerData += '"tip": {'
			fingerData += '"direction":{'
			fingerData += '"x":'+str(tip.direction.x)+','
			fingerData += '"y":'+str(tip.direction.y)+','
			fingerData += '"z":'+str(tip.direction.z)
			fingerData += '}, "position":{'
			fingerData += '"x":'+str(tip.position.x)+','
			fingerData += '"y":'+str(tip.position.y)+','
			fingerData += '"z":'+str(tip.position.z)+'} '
			fingerData += '}, "velocity":{'
			fingerData += '"x":'+str(velocity.x)+','
			fingerData += '"y":'+str(velocity.y)+','
			fingerData += '"z":'+str(velocity.z)+'},'
			fingerData += '"width":'+str(width)+'}'
			  
			fingerCnt+=1
			if (fingerCnt != numFingers):
				fingerData +=','
		fingerData  += '],' 	
			 
	else:
		fingerData  = '"fingers": null,'
	
	 	
	return fingerData

def generatePalmData(hand, handCnt, numHands):
		
	palmRay = hand.palm()
	velocity = hand.velocity()
	ball = hand.ball();
	  
	if palmRay is not None:
		# Get the palm position and wrist direction
		palm = palmRay.position
		wrist = palmRay.direction
		
		if ball is not None:
			palmData = '"ball":{'
			palmData += '"position":{'
			palmData += '"x":'+str(ball.position.x)+','
			palmData += '"y":'+str(ball.position.y)+','
			palmData += '"z":'+str(ball.position.z)+'}, '
			palmData += '"radius": '+str(ball.radius)+'},'	
		else:
			palmData = '"ball": null,'
			
		palmData += '"palm":{'
		palmData += '"direction":{'
		palmData += '"x":'+str(wrist.x)+','
		palmData += '"y":'+str(wrist.y)+','
		palmData += '"z":'+str(wrist.z)
		palmData += '}, "position":{'
		palmData += '"x":'+str(palm.x)+','
		palmData += '"y":'+str(palm.y)+','
		palmData += '"z":'+str(palm.z)+'} '	
		palmData += '},"velocity":{'
		palmData += '"x":'+str(velocity.x)+','
		palmData += '"y":'+str(velocity.y)+','
		palmData += '"z":'+str(velocity.z)+'}'
		
	else:
		palmData = '"ball": null,'
		palmData += '"palm": null,'
		palmData += '"velocity": null'
		
	#if(handCnt<numHands and numHands>1):
	#	 palmData +=','	
	  
	return palmData	
			
def main():

  setUpSocketServer()

  # Keep this process running until Enter is pressed
  print "Press Enter to quit..."
  sys.stdin.readline()

  # The controller must be disposed of before the listener
  controller = None


if __name__ == "__main__":
  main()