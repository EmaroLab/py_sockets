#!/usr/bin/env python

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.


import sys
import rospy
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import signal
import socket   
import select
import Queue
from decode_messade import*

def signal_handler(signal, frame):
	"""Signal handler of the data"""
        print('Signal Handler, you pressed Ctrl+C!')
        print('Server will be closed')
        sys.exit(0)
        #conn.close()


def main():
        pub = rospy.Publisher('wearami_acc', Pose, queue_size=10)
        pub2 = rospy.Publisher('wearami_gyro', Pose, queue_size=10)
        
	rospy.init_node('wearami_socket', anonymous=True)
	r = rospy.Rate(20) # period
	signal.signal(signal.SIGINT, signal_handler)
	
        print('Press Ctrl+C to exit of this server')
        #A server must perform the sequence socket(), bind(), listen(), accept()
        HOST = socket.gethostname()   # Get local machine name
        PORT = 8080                # Reserve a port for your service.


	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setblocking(0)

        #Running an example several times with too small delay between executions, could lead to this error:
        #socket.error: [Errno 98] Address already in use
        # There is a socket flag to set, in order to prevent this, socket.SO_REUSEADDR:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('', PORT))

        # Listen for incoming connections
        server.listen(5)

        # Sockets from which we expect to read
        inputs = [ server ]

        # Sockets to which we expect to write
        outputs = [ ]

        # Outgoing message queues (socket:Queue)
        message_queues = {}
        #i = 0

        decode = decode_message(";")

        while not rospy.is_shutdown():

		# Wait for at least one of the sockets to be ready for processing
		readable, writable, exceptional = select.select(inputs, outputs, inputs)

		# Handle inputs
		for s in readable:
		        if s is server:
		            # A "readable" server socket is ready to accept a connection
		            connection, client_address = s.accept()
		            print >>sys.stderr, 'new connection from', client_address
		            connection.setblocking(0)
		            inputs.append(connection)

		            # Give the connection a queue for data we want to send
		            message_queues[connection] = Queue.Queue()

		        else:
				data = s.recv(1024)
				if data:
					# A readable client socket has data
					list_data = data.split("\n")
					#read each line
					for line in list_data:
	                                        condition, option, x,y,z = decode.decode(line)
						if(condition == True and option == 0):
						        try:
						            accel = Pose()
						            accel.position.x=  float(x)
						            accel.position.y=  float(y)
						            accel.position.z=  float(z)
						            pub.publish(accel)
						            #i = i+1
						            print >>sys.stderr, "sending..."
							except ValueError,e:
						        	#i = i
								pass
						if(condition == True and option == 1):
						        try:
						            gyro = Pose()
						            gyro.position.x=  float(x)
						            gyro.position.y=  float(y)
						            gyro.position.z=  float(z)
						            pub2.publish(gyro)
						            #i = i+1
						            print >>sys.stderr, "sending..."
						        except ValueError,e:
						        	#i = i
								pass
						message_queues[s].put(data)
						# Add output channel for response
						if s not in outputs:
						    outputs.append(s)
				else:
				        # Interpret empty result as closed connection
				        print >>sys.stderr, 'closing', client_address, 'after reading no data'
				        # Stop listening for input on the connection
				        if s in outputs:
				            outputs.remove(s)
				        inputs.remove(s)
				        s.close()

				        # Remove message queue
				        del message_queues[s]
		#r.sleep()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass






