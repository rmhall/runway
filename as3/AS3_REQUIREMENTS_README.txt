AS3 Dependencies:

	Leap Motion SDK 0.7.1
	
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


Also note the network settings on the Flash file are set for Network only and will work fine within the IDE - but there is currently no socket policy file server included with the Leap app or Leap SDK as of SDK version 0.7.1. Until one is included, you will need to set the permissions explicitly on your local system to allow the socket communications. Alternatively you may run your own socket policy file server.
	A simple perl based solution is available here with detailed instructions: http://www.lightsphere.com/dev/articles/flash_socket_policy.html
	By default it is set to * for all sockets and * for all domains you can (should) adjust it from * to just port 6437
	and any domains settings you might want to reflect. The Leap Motion SDK should come with a socket policy file server soon.
