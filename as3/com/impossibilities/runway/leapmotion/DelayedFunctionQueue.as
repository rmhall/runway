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
*/

package com.impossibilities.runway.leapmotion 
{
	import flash.events.Event;
	import flash.display.Sprite;

	public class DelayedFunctionQueue
	{
		protected var queue:Array;
		protected var dispatcher:Sprite;
		protected var frameCnt:Number = 0;

		public function DelayedFunctionQueue()
		{
			queue = new Array();
			dispatcher = new Sprite();
		}

		public function add( func:Function, ... args ):void
		{
			var delegateFn:Function = function():void
			        {
			            func.apply( null, args );
			        };
			queue.push( delegateFn );
			if (queue.length == 1)
			{
				dispatcher.addEventListener( Event.ENTER_FRAME, count, false, 0, true );
			}
		}

		protected function count(event:Event):void
		{
			frameCnt++;
			if (frameCnt>=4)
			{
				frameCnt = 0;
				onEF(null);
			}
		}

		protected function onEF( event:Event ):void
		{
			var delegateFn:Function = queue.shift(); //queue.pop();
			//trace("Executing Command Queue: ");
			delegateFn();
			if (queue.length <= 0)
			{
				dispatcher.removeEventListener( Event.ENTER_FRAME, count, false );
			}
		}
	}
}