/*
	The MIT License
	 
	Copyright (c) 2012 Robert M. Hall, II, Inc. dba Feasible Impossibilities
	http://www.impossibilities.com/
	 
	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:
	 
	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.
	 
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
	THE SOFTWARE.
	
	
	NOTICE:
	
	This software also contains references and uses additional third party libraries (classes).
	Please see the individual libraries for their license terms.
	
	Dependencies:
	
	LeapMotion 0.7.1 SDK
	
	WebSocket Classes:
	https://github.com/Worlize/AS3WebSocket
		
		WebSocket has dependencies on:
		as3corelib:
		https://github.com/mikechambers/as3corelib/
		and
		Adobe's Flex SDK (tested with 4.6.0 and 4.6.1)
		http://www.adobe.com/devnet/flex/flex-sdk-download.html
	
*/

package com.impossibilities.leap{

	import com.worlize.websocket.WebSocket;
	import com.worlize.websocket.WebSocketErrorEvent;
	import com.worlize.websocket.WebSocketEvent;
	import com.worlize.websocket.WebSocketMessage;

	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.events.SecurityErrorEvent;
	import flash.events.IOErrorEvent;
	import flash.display.Sprite;

	dynamic public class Runway extends MovieClip {;

	// websocket is how we communciate with the Leap on port 6437 - Leap app must be running
	var websocket:WebSocket;
	var posZ:Number = 0;
	var posX:Number = 0;
	var posY:Number = 0;

	// Set up plenty of "pointables" to use as a pool for rendering to avoid costs of multiple dynamic instantiations of movieclips
	// actually create a couple extra pointables to account for two hands, some pointers and Polydactyl users ;)
	var pointerTip_0:fingerTip = new fingerTip();
	var pointerTip_1:fingerTip = new fingerTip();
	var pointerTip_2:fingerTip = new fingerTip();
	var pointerTip_3:fingerTip = new fingerTip();
	var pointerTip_4:fingerTip = new fingerTip();
	var pointerTip_5:fingerTip = new fingerTip();
	var pointerTip_6:fingerTip = new fingerTip();
	var pointerTip_7:fingerTip = new fingerTip();
	var pointerTip_8:fingerTip = new fingerTip();
	var pointerTip_9:fingerTip = new fingerTip();
	var pointerTip_10:fingerTip = new fingerTip();
	var pointerTip_11:fingerTip = new fingerTip();
	var pointerTip_12:fingerTip = new fingerTip();
	var pointerTip_13:fingerTip = new fingerTip();
	var pointerTip_14:fingerTip = new fingerTip();
	var pointerTip_15:fingerTip = new fingerTip();
	var pointerTip_16:fingerTip = new fingerTip();
	var pointerTip_17:fingerTip = new fingerTip();
	var pointerTip_18:fingerTip = new fingerTip();
	var pointerTip_19:fingerTip = new fingerTip();
	var pointerTip_20:fingerTip = new fingerTip();

	var activeItems_arr:Array = [];
	var activeIDs_arr:Array = [];

	var connectButton:connectButt = new connectButt();
	var disconnectButton:disconnectButt = new disconnectButt();

	var telemetry:Object;

	var frameData:Object;
	var renderFlag:Boolean = false;
	var hasFocus:Boolean = false;
	var initialConnect:Boolean = false;
	
	var pointablesContainer:Sprite = new Sprite();


	public function Runway () {
		init ();
	}

	private function init ():void {
		
		addChild(pointablesContainer);

		pointablesContainer.addChild (pointerTip_0);
		pointablesContainer.addChild (pointerTip_1);
		pointablesContainer.addChild (pointerTip_2);
		pointablesContainer.addChild (pointerTip_3);
		pointablesContainer.addChild (pointerTip_4);
		pointablesContainer.addChild (pointerTip_5);
		pointablesContainer.addChild (pointerTip_6);
		pointablesContainer.addChild (pointerTip_7);
		pointablesContainer.addChild (pointerTip_8);
		pointablesContainer.addChild (pointerTip_9);
		pointablesContainer.addChild (pointerTip_10);
		pointablesContainer.addChild (pointerTip_11);
		pointablesContainer.addChild (pointerTip_12);
		pointablesContainer.addChild (pointerTip_13);
		pointablesContainer.addChild (pointerTip_14);
		pointablesContainer.addChild (pointerTip_15);
		pointablesContainer.addChild (pointerTip_16);
		pointablesContainer.addChild (pointerTip_17);
		pointablesContainer.addChild (pointerTip_18);
		pointablesContainer.addChild (pointerTip_19);
		pointablesContainer.addChild (pointerTip_20);

		
		addChild (connectButton);
		addChild (disconnectButton);

		connectButton.x = 22;
		connectButton.y = 432;
		disconnectButton.x = 136;
		disconnectButton.y = 432;

		connectButton.gotoAndStop (1);
		disconnectButton.gotoAndStop (2);

		connectButton.addEventListener (MouseEvent.CLICK, openConnection);
		disconnectButton.addEventListener (MouseEvent.CLICK, closeConnection);

		addEventListener (Event.ACTIVATE, activateHandler);
		addEventListener (Event.DEACTIVATE, deactivateHandler);
	}


	private function activateHandler (event:Event):void {
		trace ("activateHandler");
		// Sockets and Flash losing focus often results in buffering issues on sockets
		// so lets disconnect on de-activate and re-connect on active to avoid
		// a huge lag and other issues
		hasFocus = true;
		if (initialConnect) {
			websocket.connect ();
		}
	}

	private function deactivateHandler (event:Event):void {
		trace ("deactivateHandler");
		hasFocus = false;
		websocket.close ();
	}


	private function handleCreationComplete ():void {
		websocket = new WebSocket("ws://localhost","*");
	}

	private function handleWindowClosing (event:Event):void {
		if (websocket.connected) {
			websocket.close ();
		}
	}

	private function openConnection (event:MouseEvent):void {
		connectButton.enabled = false;
		connectButton.gotoAndStop (2);
		disconnectButton.gotoAndStop (1);
		websocket = new WebSocket("ws://127.0.0.1:6437","*");
		websocket.debug = true;
		websocket.connect ();
		websocket.addEventListener (WebSocketEvent.CLOSED, handleWebSocketClosed);
		websocket.addEventListener (WebSocketEvent.OPEN, handleWebSocketOpen);
		websocket.addEventListener (WebSocketEvent.MESSAGE, handleWebSocketMessage);
		websocket.addEventListener (IOErrorEvent.IO_ERROR, handleIOError);
		websocket.addEventListener (SecurityErrorEvent.SECURITY_ERROR, handleSecurityError);
		websocket.addEventListener (WebSocketErrorEvent.CONNECTION_FAIL, handleConnectionFail);
	}


	private function handleIOError (event:IOErrorEvent):void {
		connectButton.enabled = true;
		disconnectButton.enabled = false;
		connectButton.gotoAndStop (1);
		disconnectButton.gotoAndStop (2);
	}

	private function handleSecurityError (event:SecurityErrorEvent):void {
		connectButton.enabled = true;
		disconnectButton.enabled = false;
		connectButton.gotoAndStop (1);
		disconnectButton.gotoAndStop (2);
	}

	private function handleConnectionFail (event:WebSocketErrorEvent):void {
		WebSocket.logger ("Connection Failure: " + event.text);
	}

	private function handleWebSocketClosed (event:WebSocketEvent):void {
		WebSocket.logger ("Websocket closed.");
		disconnectButton.enabled = false;
		connectButton.enabled = true;
		connectButton.gotoAndStop (2);
		disconnectButton.gotoAndStop (1);
		removeEventListener (Event.ENTER_FRAME, render);
	}

	private function handleWebSocketOpen (event:WebSocketEvent):void {
		WebSocket.logger ("Websocket Connected");
		initialConnect = true;
		disconnectButton.enabled = true;
		connectButton.gotoAndStop (2);
		disconnectButton.gotoAndStop (1);
		addEventListener (Event.ENTER_FRAME,render);
	}

	public function drawPointables (frame:Object):void {
		
		// There is way more data than just the fingertip positions - this demo is only drawing those for now
		// More to come! Reference the following objects below for more data:
		
		/*
			trace("START");
			trace(telemetry.id);
			trace(telemetry.timestamp);
			trace(frameData.hands);
			trace(frameData.pointables);
			trace(frameData.r);
			trace(frameData.s);
			trace(frameData.t);
			trace("END");
		*/

		var fingerLoop:uint = 0;
		var handLoop:uint = 0;
		var pointerCount:uint;

		pointerCount = frame.pointables.length;
		
		// reset arrays (refactor to vectors for speed) and remove all unused pointers
		activeItems_arr.length = 0;
		activeIDs_arr.length = 0;
		removePointerTips (pointerCount);
		
		if (pointerCount>=1) {
			
			for (fingerLoop = 0; fingerLoop<=pointerCount-1; fingerLoop++) {
				var item = this["pointerTip_" + fingerLoop];
				activeItems_arr.push (item);
				//item.id = frame.pointables[fingerLoop].id;
				activeIDs_arr.push(frame.pointables[fingerLoop].id);				
				pointablesContainer.addChild (activeItems_arr[fingerLoop]);
				
				posX = 0;
				posY = 0;
				posZ = 0;
				this["pointerTip_" + fingerLoop].visible = true;

				posX = parseFloat(frame.pointables[fingerLoop].tipPosition[0]); //x
				posY = parseFloat(frame.pointables[fingerLoop].tipPosition[1]); //y
				// revisit this to add real depth and not psuedo scaled depth - true 3D next!
				posZ = 4 + parseFloat(frame.pointables[fingerLoop].tipPosition[2]) / 20 * 1; //z
				// keep the pseudo scale from getting too small 
				if (posZ<.5) {
					posZ = .5;
				}

				// Revisit scaling to adjust dimensions - perhaps allow for calibration of
				// min/max rect, etc. - but for now position them x,y and scaleX,scaleY to simulate z depth
				this["pointerTip_" + fingerLoop].x=stage.stageWidth/2-(posX/stage.stageWidth)*-(stage.stageWidth*2);
				this["pointerTip_" + fingerLoop].y=470-(posY)*1.25;//470
				this["pointerTip_" + fingerLoop].scaleX = posZ;
				this["pointerTip_" + fingerLoop].scaleY = posZ;

				// Revisit with 0.7.1 SDK to add r,s,t and revision to json beyond fingers to pointers and other
				// changes introduced in 0.7.1 for JSON data - see: 
				// https://developer.leapmotion.com/forums/forums/sdk-releases/topics/json-changes-in-0-7-1

			}
		}


	}

	public function removePointerTips (pointerCount:Number):void {
		// Need to add intelligence to only remove pointers with unused ID's to make more efficient
		while (pointablesContainer.numChildren > 0) {
			pointablesContainer.removeChildAt(0);
		}
	}

	public function render (event:Event):void {
		// Now we are driven by enter_frame event rather than the websocket event to avoid unneccessary redraws and overhead
		if (renderFlag) {
			drawPointables (frameData);
		} else {
			removePointerTips (20);
		}
	}

	private function handleWebSocketMessage (event:WebSocketEvent):void {
		//trace (event.message.type);
		//trace (event.message);
		//trace (event.message.utf8Data);

		// NOTE: Lots of data - if you turn on tracing of the messages and then minimize Flash
		// so it loses focus, and then come back - you might experience a lot of lag/latency
		// turn off traces of large messages and you should be fine

		telemetry = JSON.parse(event.message.utf8Data);
		// telemetry.hands != undefined && 
		if (telemetry.pointables != undefined) {
			frameData = telemetry;
			renderFlag = true;
		} else {
			renderFlag = false;
		}

	}

	public function closeConnection (event:MouseEvent):void {
		WebSocket.logger ("Disconnecting.");
		websocket.close ();
		connectButton.gotoAndStop (1);
		disconnectButton.gotoAndStop (2);
	}
}
}