#!/usr/bin/env python

# Luis Enrique Coronado Zuniga

# You are free to use, change, or redistribute the code in any way you wish
# but please maintain the name of the original author.
# This code comes with no warranty of any kind.

class decode_message():
	"""This class decodes a message from a set of strings used in the wearAmi programs. Because there are different format it is necessary specify the delimiter.
	   
	:param string: delimiter used. Example ";"

	"""
        def __init__(self,string):
                self.delimiter = string

        def decode(self,line):
                """Acceleration decodification

                :param line: string with a sample of the accelerometer or gyroscope sensor
                :param remote_ip: ip of the server
                :return: 
			- success: True if the string has the correct format
			- option: if option == 0 then is aceleration data, if option = =1 then is gyroscope data
			- value1: x value
			- value2: y value
			- value3: z value

               	An example of a format used for a wearAmi program is:

                - <indicator>;number;x_value;y_value:z_value
            	
		where <indicator> can be a (acceleration) or y (gyroscope), 

                """
                line_list = line.split(self.delimiter)
                if(line_list[0] == 'a'):
                        if(len(line_list)==5 and line_list[4] != ''):
                                x = line_list[2]
                                y = line_list[3]
                                z = line_list[4]
                                return True,0,x,y,z
                if(line_list[0] == 'y'):
                        if(len(line_list)==5 and line_list[4] != ''):
                                x = line_list[2]
                                y = line_list[3]
                                z = line_list[4]
                                return True,1,x,y,z
                return False,0,0,0,0

if __name__ == "__main__":
    import doctest
    doctest.testmod()







