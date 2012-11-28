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
import sys
import time
from thread import *

HOST = ''
PORT = 8888
	
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def setUpSocketServer():

	lastInfo = ''
	lastFrameID = ''

	global fingerInfo
	global palmRayInfo
	global palmAngles
	global palmRadius
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
		fingerInfo = ''
		palmRayInfo = ''
		palmAngles = ''
		palmRadius = ''
		frameID = ''
		lastFrameID = ''
		allData = ''
		
		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientthread ,(conn,))
		
		listener = SampleListener()
  		controller = Leap.Controller(listener)

  		
  		while 1:
  		
  				if (frameID != lastFrameID and lastInfo != allData):
  					telemetryInfo = allData
  				
  					print allData
  				
  					conn.sendall(telemetryInfo)
  					
				lastInfo = telemetryInfo
				lastFrameID = frameID
				time.sleep(0.05)

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


class SampleListener(Leap.Listener):

	def onInit(self, controller):
		print "LEAP Initialized"

	def onConnect(self, controller):
		print "LEAP Connected"

	def onDisconnect(self, controller):
		print "LEAP Disconnected"

	def onFrame(self, controller):
		global fingerInfo
		global palmRayInfo
		global palmAngles
		global palmRadius
		global frameID
		global allData
	
		# Get the most recent frame and report some basic information
		frame = controller.frame()
		hands = frame.hands()
		numHands = len(hands)
		#print "Frame id: %d, timestamp: %d, hands: %d" % (frame.id(), frame.timestamp(), numHands)
		frameID=frame.id()
	
		if numHands >= 1:
		  # Get the first hand
		  hand = hands[0]
	
		  # Check if the hand has any fingers
		  fingers = hand.fingers()
		  numFingers = len(fingers)
		  if numFingers >= 1:
			# Calculate the hand's average finger tip position
			pos = Leap.Vector(0, 0, 0)
			dir = Leap.Vector(0, 0, 0)
			fingerInfo = str(numFingers)
			for finger in fingers:
			  tip = finger.tip()
			  id = finger.id()
			  #dir.x = 
			  pos.x = tip.position.x
			  pos.y = tip.position.y
			  pos.z = tip.position.z
			  fingerInfo += "#"+str(pos.x)+","+str(pos.y)+","+str(pos.z)  
			#pos = Leap.Vector(pos.x/numFingers, pos.y/numFingers, pos.z/numFingers)
			#print "Hand has %d fingers with average tip position (%f, %f, %f)" % (numFingers, pos.x, pos.y, pos.z)
		  else:
		   	fingerInfo = "0"
		   	
	
		  # Check if the hand has a palm
		  palmRay = hand.palm()
		  if palmRay is not None:
			# Get the palm position and wrist direction
			palm = palmRay.position
			wrist = palmRay.direction
			#print "Palm position (%f, %f, %f)" % (palm.x, palm.y, palm.z)
			palmRayInfo = "#^"+str(palm.x)+","+str(palm.y)+","+str(palm.z)	
	
			# Check if the hand has a normal vector
			normal = hand.normal()
			if normal is not None:
			  # Calculate the hand's pitch, roll, and yaw angles
			  pitchAngle = -math.atan2(normal.z, normal.y) * 180/math.pi + 180
			  rollAngle = -math.atan2(normal.x, normal.y) * 180/math.pi + 180
			  yawAngle = math.atan2(wrist.z, wrist.x) * 180/math.pi - 90
			  # Ensure the angles are between -180 and +180 degrees
			  if pitchAngle > 180: pitchAngle -= 360
			  if rollAngle > 180: rollAngle -= 360
			  if yawAngle > 180: yawAngle -= 360
			  #print "Pitch: %f degrees,  roll: %f degrees,  yaw: %f degrees" % (pitchAngle, rollAngle, yawAngle);
					
			  palmAngles = "^"+str(pitchAngle)+","+str(rollAngle)+","+str(yawAngle)	
		  else:
		  	palmRayInfo = '^'
		  	palmAngles = '^'
		  	
		  # Check if the hand has a ball
		  ball = hand.ball();
		  if ball is not None:
			#print "Hand curvature radius: %f mm" % ball.radius
			palmRadius = "^"+str(ball.radius)
		  else:
		  	palmRadius = '^'
		
		  allData = fingerInfo+palmRayInfo+palmAngles+palmRadius
		
		else:
			fingerInfo = ''
			palmRayInfo = ''
		  	palmAngles = ''
			palmRadius = ''
			allData = ''
			allData = fingerInfo+palmRayInfo+palmAngles+palmRadius
			
def main():

  # Create a sample listener and assign it to a controller to receive events
  #listener = SampleListener()
  #controller = Leap.Controller(listener)
  
  setUpSocketServer()

  # Keep this process running until Enter is pressed
  print "Press Enter to quit..."
  sys.stdin.readline()

  # The controller must be disposed of before the listener
  controller = None


if __name__ == "__main__":
  main()