/*
	The MIT License
	 
	Copyright (c) 2012 Robert M. Hall, II, Inc. dba Feasible Impossibilities - http://www.impossibilities.com/
	 
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
*/

package com.impossibilities.leapmotion 
{
	import flash.display.Sprite;
	import flash.display.MovieClip;
	import flash.events.*;
	import flash.display.Stage;
	import flash.display.StageAlign;
	import flash.display.StageScaleMode;

	import com.impossibilities.leapmotion.DelayedFunctionQueue;
	import com.impossibilities.leapmotion.CustomSocket;

	public class LeapCore extends Sprite
	{

		private var leapINIT:Boolean = false;
		
		private var cmdQUEUE:CommandQueue = new CommandQueue();
		private var socket:CustomSocket; 
		
		private var cursorIcon1:cursor = new cursor();
		private var cursorIcon2:cursor = new cursor();
		private var cursorIcon3:cursor = new cursor();
		private var cursorIcon4:cursor = new cursor();
		private var cursorIcon5:cursor = new cursor();
		
		private var hasFocus:Boolean = false;

		public function LeapCore()
		{
			stage.align = StageAlign.TOP_LEFT; 
			//stage.scaleMode = StageScaleMode.NO_SCALE;
			initComm();
			cursorIcon1.visible=false;
			cursorIcon2.visible=false;
			cursorIcon3.visible=false;
			cursorIcon4.visible=false;
			cursorIcon5.visible=false;
			addChild(cursorIcon1);
			addChild(cursorIcon2);
			addChild(cursorIcon3);
			addChild(cursorIcon4);
			addChild(cursorIcon5);
			
			addEventListener(Event.ACTIVATE, activateHandler);
			addEventListener(Event.DEACTIVATE, deactivateHandler);

		}
		
		private function activateHandler(event:Event):void
		{
				trace("activateHandler");
				// might want to put in a delay here as regaining focus can
				// still allow some data to overflow the socket buffer
				hasFocus=true;
		}

		private function deactivateHandler(event:Event):void
		{
			trace("deactivateHandler");
			hasFocus = false;
		}
		
		private function initComm():void
		{
			if (! leapINIT)
			{
				var netWorkType:String = detectNetworkType();
				if (netWorkType)
				{
					leapINIT = true;
					socket = new CustomSocket(this,"127.0.0.1",8888);
					//cmdQUEUE.add(socket.sendCommand, "!1MVLQSTN");
				}
			}

		}
		

		private function networkState(event:Event):void
		{
			trace(event);
		}

		private function detectNetworkType():String
		{
			return "ETHER";
			/*
			var returnVal:String;
			if (NetworkInfo.isSupported)
			{

				var interfaces:Vector.<NetworkInterface >  = NetworkInfo.networkInfo.findInterfaces();

				addEventListener(Event.NETWORK_CHANGE, networkState);

				for (var i:uint = 0; i < interfaces.length; i++)
				{
					trace(interfaces[i].name);

					if (interfaces[i].name.toLowerCase() == "wifi" && interfaces[i].active)
					{

						trace("WiFi connection enabled");
						returnVal = "WIFI";
						break;
					}
					else if (interfaces[i].name.toLowerCase() == "mobile" && interfaces[i].active)
					{
						trace("Mobile data connection enabled");
						returnVal = "MOBILE";
						break;
					}
					else if (interfaces[i].name.toLowerCase().substr(0,2) == "en" && interfaces[i].active)
					{
						// for desktop
						trace("Local Ethernet data connection enabled");
						returnVal = "ETHER";
						break;
					}

				}
			}
			else
			{
				returnVal = "NOGO";
			}
			return returnVal;
			*/
		}
		
		
		private var posZ:Number = 0;
		private var posX:Number = 0;
		private var posY:Number = 0;
		
		private var fingerVector:Vector.<uint>;
		private var palmVector:Vector.<uint>;// = Vector.<Type>(array);
		private var fingerDataArray:Array = [];
		private var fingerInfoArray:Array = [];
		private var palmDataArray:Array = [];
		private var fingerCount:uint = 0;
		private var fingerInfo:String = ""
		private var fingersArray:Array = [];
		private var cnt:Number= 0;
		private var telemetry:Object;

		public function sendData(jsonString:String):void {
			if(hasFocus && jsonString != null && jsonString != "CONNECTED" && jsonString != "") {
				try {
					telemetry = JSON.parse(jsonString);
					} catch (err:Error) {
						cnt++;
						trace("Dropping Frame: "+cnt);
						trace("ERROR:"+err+"\nJSON: '"+ jsonString+"'\n");
					}
				//trace(telemetry.frame.id +" - "+telemetry.frame.timestamp);	
				
				if(telemetry.frame != undefined) {
					if(telemetry.frame.hands != undefined) {
						if(telemetry.frame.hands.fingers != undefined) {
							//trace(telemetry.frame.hands[0].fingers[0].tip.position.x);
							positionHand(telemetry.frame.hands)
						}
					}
				}
			}
			
			
		}
		
		function positionHand(hand:Object):void {
			
			trace(hand.fingers[0].tip.position.x);
			cursorIcon1.visible=true;
			cursorIcon1.x = hand.fingers[0].tip.position.x;
			var i:uint=0;
			var fingerCount = hand.fingers.length;
			
			for( i = 0; i<5; i++) {
				this["cursorIcon"+(i+1)].visible=false;
			}
				
				var tipArray:Array =[];
				if(fingerCount>0) {
					trace("fingercount: "+	fingerCount);
					for( i = 0; i<fingerCount; i++) {
						posX = 0;
						posY = 0;
						posZ = 0;
						this["cursorIcon"+(i+1)].visible=true;
						
						posX = parseInt(hand.fingers[i].tip.position.x);
						posY = parseInt(hand.fingers[i].tip.position.y);
						posZ = 4+parseInt(hand.fingers[i].tip.position.z)/20*1;
						
						if(posZ<.5) {
							posZ=.5;
						}
						
						this["cursorIcon"+(i+1)].x=stage.stageWidth/2-(posX/stage.stageWidth)*-(stage.stageWidth*2);
						this["cursorIcon"+(i+1)].y=470-(posY)*1.25; //470
						
						this["cursorIcon"+(i+1)].scaleX=posZ;
						this["cursorIcon"+(i+1)].scaleY=posZ;
						//trace("FINGER "+i+": "+this["cursorIcon"+(i+1)].x,this["cursorIcon"+(i+1)].y);

					}
				}
			
			
		}
		
		function trim(s:String):String { 
			return s ? s.replace(/^\s+|\s+$/gs, '') : ""; 
		}
		
		

	}

}
