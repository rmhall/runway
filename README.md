Runway 0.1a for Leap Motion
===========================
Robert M. Hall, II - http://www.impossibilities.com/
----------------------------------------------------

Runway is a set of Python, Flash/ActionScript 3, and JavaScript helpers for leveraging data from the Leap Motion input device - http://leapmotion.com/ 

See a short video of this in action here:
http://rhall.s3.amazonaws.com/runway_leapmotion_demo/runway_bridge_demo.mp4

Current State as of 11/29/2012:

	1. Functioning Python Socket server "Runway" to collect data from LeapMotion device, format into JSON and push out over a local socket port 8888.
	2. Functioning Flash library to connect via sockets to Runway Socket Server and collect/push JSON data for use in ActionScript 3
	3. Demo Flash file showing interaction, finger tip data rendering
	
USAGE:

	1. Drop the python/Runway.py python script in with your Leap libs in the Leap SDK folder
	2. Launch it with: python Runway.py - App will start accepting connections
	3. Publish the leap_test1.fla or open the leap_test1.swf - wiggle your fingers over your Leap and watch the fun
	4. Observe output from terminal Runway.py app and Flash trace statements
	5. Extend, modify, improve and enjoy!
	
TODO:

	1. Add support for additional "hands" or "tools" in Runway - currently only supports first hand present
	2. Additional refinements and data points in Runway Python socket server, and AS3 bridge classes (Learn more Python!)
	3. More actual demos of usage of the data for control/input, etc - getting the communication down first!
	4. Add externalInterface methods to allow SWF to run faceless and act as a bridge to JavaScript - great for supporting older browsers with no websockets, or native plugins for LeapMotion
	5. Websocket based JavaScript lib to match Flash/AS3 functionality for modern browsers - see great example Leapfrog here using websockets, JSON and Processing:  https://github.com/tylerwilliams/leapfrog
	6. Native Extension for Adobe AIR for Mac/PC to use native LeapMotion SDK to poll/collect data from LeapMotion for use in AS3/AIR apps.
	
NOTES:

	1. This is down and dirty, was going from 0 to wanting something I could play with in Flash in less than a day after receiving the Leap Motion device and reviewing the SDK. My python chops are on the dangerous beginner level - probably much better ways to do what I did, including handling the sockets and creating the JSON - welcome tips there!
	2. The AS3 is pretty decent used some of my previous socket code from another app and adapted it - note there are issues around sockets and Flash losing	focus and throttling things down. Welcome any suggestions on this as well.
	3. Ideally I'd like the Runway.py socket server to do standard HTML5 websocket implementation and change the AS3 implementation to use that as well so its totally interchangeable (again see the Leapfrog link above), but it seemed like overkill and extra latency and the HTML5 websocket implementations I found for AS3 were lacking - any recommendations there welcome.
	4. The Leap Motion SDK is in a state of flux as they refine things, expect changes an improvements there as they release updates.
	
So there you have it - all comments, criticisms welcome! Please log issues, pull requests, etc. Enjoy!	
		