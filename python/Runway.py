####################################################################################
#	The MIT License																   #
#																				   # 
#	Copyright (C) 2012 Robert M. Hall, II, Inc. dba Feasible Impossibilities       #
#	http://www.impossibilities.com/												   #
#	 																			   #
#	Permission is hereby granted, free of charge, to any person obtaining a copy   #
#	of this software and associated documentation files (the "Software"), to deal  #
#	in the Software without restriction, including without limitation the rights   #
#	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      #
#	copies of the Software, and to permit persons to whom the Software is          #
#	furnished to do so, subject to the following conditions:					   #
#	 																			   #
#	The above copyright notice and this permission notice shall be included in     #
#	all copies or substantial portions of the Software.							   #
#	 																			   #
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     #
#	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       #
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    #
#	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         #
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  #
#	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN      #
#	THE SOFTWARE.																   #
####################################################################################

####################################################################################
#  NOTICE: Software contains references to and uses the Leap Motion SDK/API:       #
#  Copyright (C) 2012 Leap Motion, Inc. All rights reserved.                       #
#  NOTICE: This developer release of Leap Motion, Inc. software is confidential    #
#  and intended for very limited distribution. Parties using this software must    #
#  accept the SDK Agreement prior to obtaining this software and related tools.    #
#  This software is subject to copyright.                                          #
####################################################################################

####################################################################################
# Runway Version 0.1a - 11/29/2012                                                 #
####################################################################################

import Leap, sys, math
import socket
import time
from thread import *

class bcolors:
	STRANGE = '\033[90m'
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	def disable(self):
		self.STRANGE = ''
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

def setUpSocketServer():

	# Create a Leap listener and assign it to a controller to receive events
	listener = LeapListener()
  	controller = Leap.Controller(listener)

	lastInfo = ''
	lastFrameID = ''

	global frameID
	global jsonStore
	global flashSocketState
	flashSocketState = False
	
	HOST = ''
	PORT = 8888
	
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
	print bcolors.OKBLUE + 'Socket Created...'+ bcolors.ENDC
	
	try:
		s.bind((HOST, PORT))
	except socket.error , msg:
		print 'Bind Failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	
	print bcolors.OKBLUE + 'Socket BIND Complete...'+ bcolors.ENDC
	
	s.listen(10)
	print bcolors.OKBLUE + 'Socket Now Listening...'+ bcolors.ENDC
		
		#now keep talking with the client
	while 1:
		#wait to accept a connection - blocking call
		conn, addr = s.accept()
				
		print 'Connected with client at: ' + addr[0] + ':' + str(addr[1])
		
		telemetryInfo = ''
		frameID = ''
		lastFrameID = ''
		jsonStore = ''
		
		print 'Beginning broadcast...'
		
		start_new_thread(clientThread ,(conn,))

		#Before we start pushing out info wait a bit to avoid any potential issues
  		time.sleep(1);
  		
  		
  		while 1:
  				
  				telemetryInfo=''
				if (frameID != lastFrameID and lastInfo != jsonStore and flashSocketState == True):
					telemetryInfo = jsonStore
  				
					if(telemetryInfo != "" and telemetryInfo is not None):
						try:
							conn.sendall(telemetryInfo+"\n")
  						except socket.error , msg:
							print  bcolors.FAIL + 'Socket Error - Code: ' + str(msg[0]) + ' Message ' + msg[1]+ bcolors.ENDC
							conn, addr = s.accept()
							print 'Connected with client at: ' + addr[0] + ':' + str(addr[1])
							print 'Restarting broadcast...'
							start_new_thread(clientThread ,(conn,))
						
				lastInfo = telemetryInfo
				lastFrameID = frameID
				#This sleep can be adjusted up or down- future iterations of the Leap SDK
				#Have indicated more control over Frame update rate, etc.
				time.sleep(0.02)


	s.close()
	
#Handle incoming connection data on a thread for control commands since we primarily are pushing out data
def clientThread(conn):

    global flashSocketState
    #Sending message to connected client
    print 'Connected!'
    conn.send('CONNECTED')
    flashSocketState = True
     
    #Infinite loop so that function does not terminate and thread does not end.
    #Not totally neccessary, but may add some control functions in here from client
    while True:
        time.sleep(0.1)
        #Receiving from client
        data = conn.recv(1024)
        reply = data;
                
        print 'RECEIVED COMMAND: '+reply
        
        if not data:
            break
            
        if (reply=="ACTIVATING" or reply=="DEACTIVATING"):
			reply = 'OK'
			conn.sendall(reply)	
			if(reply=="ACTIVATING"):
				flashSocketState=True
			if(reply=="DEACTIVATING"):
				flashSocketState=False	
				
          
    #came out of loop
    conn.close()

class LeapListener(Leap.Listener):

	def onInit(self, controller):
		print bcolors.STRANGE + "LEAP Initialized"+ bcolors.ENDC

	def onConnect(self, controller):
		print bcolors.OKGREEN + "LEAP Connected"+ bcolors.ENDC
		print bcolors.WARNING + 'CTRL-C TO STOP'+ bcolors.ENDC

	def onDisconnect(self, controller):
		print bcolors.FAIL + "LEAP Disconnected"+ bcolors.ENDC

	def onFrame(self, controller):
		global frameID
		global jsonStore

		jsonStore = ''	
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
			# Get the hands - need to loop over all hands 
			# Currently just the 1st hand - REVISIT!
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
		   
			jsonStore = jsonData
		
		else:
			jsonData += '"hands": null }, "state":"frame" }'
			jsonStore = jsonData
	
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

	try:
		setUpSocketServer()
	except KeyboardInterrupt:
		print bcolors.FAIL + "\nCaught CTRL-C Interrupt, terminating..."+ bcolors.ENDC

if __name__ == "__main__":
  main()