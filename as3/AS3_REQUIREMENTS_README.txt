AS3 Dependencies:
	
	WebSocket Classes:
	https://github.com/Worlize/AS3WebSocket
	
	Included in this project
		
		WebSocket has dependencies on:
		as3corelib (also included in this project):
		https://github.com/mikechambers/as3corelib/
		and
		Adobe's Flex SDK (tested with 4.6.0 and 4.6.1 NOT included in this project)
		http://www.adobe.com/devnet/flex/flex-sdk-download.html
		

From your ActionScript settings panel, make sure to include the path to either Flex SDK 4.6.0 or 4.6.1 in order for all the neccessary class files to be present. Same goes for the as3corelib SWC file. All other neccessary classes are included in the com class folder in this project.		


Also note the network settings on the Flash file are set for Network only and will work fine within the IDE - but there is currently no polciy socket server with Leaps built in WebSocket server on por 6437 (as of SDK version 0.6.6) Until they include one, you will need to set the permissions explicitly on your local system to allow the socket communications. Leap will be including a policy socket server in a futrue release.)