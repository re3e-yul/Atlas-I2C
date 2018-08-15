# Atlas-I2C
Usage: Atlas-I2C [verb] [address] (in any order)
		verbs as in i2c Commands listed in Atlas Scientific documentation
		address as reported by i2cdetect -y [1/0] 
		atlas-I2C without parameter will detect connected i2c devices
		atlas-I2C [address] will invoke i, information on the device at address 

		atlas-i2c 99 r will read device at address 99
