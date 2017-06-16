#!/usr/bin/env python

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

import socket   #for sockets
import sys  #for exit
import time

class sim_client:
     """This class can be used to simulate client-server connection in case a smarthwatch is not available.
        In general sends messages as strings, then can be used for other types of projects.

        :param name_file: txt file with with data taken of the smartwacth (wearAmi offline version)
        :param remote_ip: ip of the server


        :Example:

        >>> from sim_client import*
        >>> name_file = "prova.txt"
        >>> remote_ip = "192.168.2.1
        >>> c = sim_client(name_file,remote_ip)

        """
     def __init__(self,name_file, remote_ip):
            
            try:
                #create an AF_INET, STREAM socket (TCP)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
                print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
                sys.exit();
             
            print 'Socket Created'
             
            host = socket.gethostname()
            port = 8080
             
            try:
                #Same computer
                remote_ip = socket.gethostbyname( host )
                #In a network
             
            except socket.gaierror:
                #could not resolve
                print 'Hostname could not be resolved. Exiting'
                sys.exit()
                 
            print 'Ip address of ' + host + ' is ' + remote_ip
             
            #Connect to remote server
            s.connect((remote_ip , port))
             
            print 'Socket Connected to ' + host + ' on ip ' + remote_ip

            f = open(name_file);
            i = 0
            while(i<300):
                try:
                    line = f.readline()
                    print i
                    s.sendall(line)
                    time.sleep(.005);
                    i = i +1
                except socket.error:
                    #Send failed
                    print 'Send failed'
                    sys.exit()

            print 'Message send successfully'

if __name__ == "__main__":
    import doctest
    doctest.testmod()

#Uncomment to run an example
#name_file = "prova.txt"
#remote_ip = "192.168.2.1"
#c = sim_client(name_file,remote_ip)

