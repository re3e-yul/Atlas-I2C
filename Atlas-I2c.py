#!/usr/bin/python
import io # used to create file streams
import fcntl # used to access I2C parameters like addresses
import time # used for sleep delay and timestamps
import sys

class atlas_i2c():
	
    	long_timeout = 1.5 # the timeout needed to query readings and calibrations
    	short_timeout = .5 # timeout for regular commands
    	default_bus = 1 # the default bus for I2C on the newer Raspberry Pis, certain older boards use bus 0
    	default_address = 103 # the default address for the pH sensor
        current_addr = default_address
    	def __init__(self, address=default_address, bus=default_bus):
       		# open two file streams, one for reading and one for writing
        	# the specific I2C channel is selected with bus it is usually 1, except for older revisions where its 0 wb and rb indicate binary read and write
        	self.file_read = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
        	self.file_write = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)
        	# initializes I2C to either a user specified or default address
        	self.set_i2c_address(address)
    	def set_i2c_address(self, addr):
        	# set the I2C communications to the slave specified by the address
        	0 # The commands for I2C dev using the ioctl functions are specified in
        	# the i2c-dev.h file from i2c-tools
        	I2C_SLAVE = 0x703
        	fcntl.ioctl(self.file_read, I2C_SLAVE, addr)
        	fcntl.ioctl(self.file_write, I2C_SLAVE, addr)
    	def write(self, string):
        	# appends the null character and sends the string over I2C
        	string += "\00"
        	self.file_write.write(string)
    	def read(self, num_of_bytes=31):
       		# reads a specified number of bytes from I2C, then parses and displays the result
        	res = self.file_read.read(num_of_bytes) # read from the board
        	response = filter(lambda x: x != '\x00', res) # remove the null characters to get the response
        	if (ord(response[0]) == 1): # if the response isnt an error
            		char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:])) # change MSB to 0 for all received characters except the first and get a list of characters
            		# NOTE: having to change the MSB to 0 is a glitch in the raspberry pi, and you shouldn't have to do this!
            		return ''.join(char_list) # convert the char list to a string and returns it
        	else:
            		return "Error " + str(ord(response[0]))
    	def query(self, string):
        	# write a command to the board, wait the correct timeout, and read the response
        	self.write(string)
        	# the read and calibration commands require a longer timeout
        	if ((string.upper().startswith("R")) or
                	(string.upper().startswith("CAL"))):
            		time.sleep(self.long_timeout)
        	elif ((string.upper().startswith("SLEEP"))):
            		return "sleep mode"
        	else:
            		time.sleep(self.short_timeout)
        	return self.read()
    	def close(self):
        	self.file_read.close()
        	self.file_write.close()

	def list_i2c_devices(self):
                prev_addr = self.current_addr # save the current address so we can restore it after
                i2c_devices = []
                for i in range (0,128):
                        try:
                                self.set_i2c_address(i)
                                self.read()
                                i2c_devices.append(i)
                        except IOError:
                                pass
                self.set_i2c_address(prev_addr) # restore the address we were using
                return i2c_devices


def main():

	for x in range(1,len(sys.argv)):
        	try:
                	y=sys.argv[x]
	                float(y)
        	        addr = y
	        except ValueError:
        	        verb = y


	device = atlas_i2c()     # creates the I2C port object, specify the address or bus if necessary
	if (verb == 'list'):
	        devices = device.list_i2c_devices()
                for i in range(len (devices)):
        	        print devices[i]

		exit()

	device.set_i2c_address(int(addr))

	#print("I2C address set to " + str(addr))


        # main loop
	try:
		print(device.query(verb))
	except IOError:
        	print("Query failed \n - Address may be invalid, use List_addr command to see available addresses")


if __name__ == '__main__':
        main()
