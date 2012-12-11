Runway 0.1a for Leap Motion
===========================
Robert M. Hall, II - http://www.impossibilities.com/
----------------------------------------------------

Runway is a set of Flash/ActionScript 3 classes and example code for leveraging data from the Leap Motion input device - http://leapmotion.com/ 

See a short video of this in action here:
http://rhall.s3.amazonaws.com/runway_leapmotion_demo/runway_bridge_demo.mp4

Revision History:

12/11/2012:
	
	1. Changed the fingertip rendering to be driven by enter_frame instead of the ondata websocket event, to avoid unneccessary drawing/code execution
	2. Removed setting visibility, and moved to add or remove child model - need to fine tune this
	3. Prepped for making a standalone SWF to act as polyfill for browsers that lack support for WebSockets to allow JS access to Leap data

12/01/2012: 

	1. Leap SDK 0.6.6 now includes its own WebSocket server on 6437, serving JSON based info on the data captured by the device - fantastic!
	2. Removed old Python socketserver that was not a full WebSocket server implementation - it is now in the deprecated folder for reference/archival purposes
	3. Include as3corelib and Worlize WebSocket implementation class dependencies see: AS3_REQUIREMENTS_README.txt document in AS3 folder.
	4. Also requires free Flex 4.6.0 SDK libs - not included here due to size - AS3_REQUIREMENTS_README.txt has download links for all libs.
	5. Completed support for two hands and all finger tip data
	6. Now has a nice connect/disconnect button since the WebSocket server is more robust
	7. Linked activate/deactivate handlers to connecting/disconnecting from socket server to avoid garbage, etc. when Flash throttles down when focus is lost to avoid issues with sockets
	8. Core communications is now complete - can focus on leveraging data for various uses


11/29/2012 (Initial public release against Leap SDK 0.6.5):

	1. Functioning Python Socket server "Runway" to collect data from LeapMotion device, format into JSON and push out over a local socket port 8888.
	2. Functioning Flash library to connect via sockets to Runway Socket Server and collect/push JSON data for use in ActionScript 3
	3. Demo Flash file showing interaction, finger tip data rendering

USAGE:	

	1. make sure Leap application is open and Leap device is plugged in, and ready
	2. Open the runway_demo.fla in Flash CS6 and Publish Preview
	3. Hit Connect button
	4. Use the Leap with your hands - watch your finger tip points get rendered in real time :) 
	5. Extend, modify, improve and enjoy!
	
Pre 0.6.6 SDK (Deprecated Version) USAGE:

	1. Drop the python/Runway.py python script in with your Leap libs in the Leap SDK folder
	2. Launch it with: python Runway.py - App will start accepting connections
	3. Publish the leap_test1.fla or open the leap_test1.swf - wiggle your fingers over your Leap and watch the fun
	4. Observe output from terminal Runway.py app and Flash trace statements
	5. Extend, modify, improve and enjoy!
	
TODO:

	1. DONE: Add support for additional "hands" or "tools" in Runway - currently only supports first hand present
	2. DONE (No longer needed): Additional refinements and data points in Runway Python socket server, and AS3 bridge classes (Learn more Python!)
	3. TODO: More actual demos of usage of the data for control/input, etc - getting the communication down first!
	4. TODO: Add externalInterface methods to allow SWF to run faceless and act as a bridge to JavaScript - great for supporting older browsers with no websockets, or native plugins for LeapMotion
	5. DONE: Now included as part of Leap SDK 0.6.6 built in Websocket server can be leveraged in JavaScript directly - see JS folder for example HTML/JS
	6. MAYBE: (Now with built in WebSocket server in Leap this might not really be neccessary) Native Extension for Adobe AIR for Mac/PC to use native LeapMotion SDK to poll/collect data from LeapMotion for use in AS3/AIR apps.
	
NOTES:

	1. The Leap Motion SDK is in a state of flux as they refine things, expect changes an improvements there as they release updates.
	
So there you have it - all comments, criticisms welcome! Please log issues, pull requests, etc. Enjoy!	
		