# Atlas-I2C
# original driver : Atlas Scientific 
# rewrite / addons : Eric Soulliage (eric.soulliage@gmail.com)

#Usage: Atlas-I2C [verb] [address] (in any order)
#		verbs as in i2c Commands listed in Atlas Scientific documentation

#		atlas-I2C without parameter will detect connected i2c devices

#		atlas-I2C [address] will invoke i, information on the device at address 
#
#		atlas-i2c 99 r will read device at address 99
