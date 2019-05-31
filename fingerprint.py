#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import argparse
from pyfingerprint.pyfingerprint import PyFingerprint
import pandas as pd
import csv
import os



parser = argparse.ArgumentParser(
                         description="predict fingerprint." )
parser.add_argument( '-f', '--function', type=str,
                         default='predict',
                         help="Choose The function ex. predict/enroll/index" )   
ARGS = parser.parse_args()  


                
class Fingerprint():
	def __init__(self,com,port):

		self.com = com
		self.port = port
	
	def enroll(self):
		try:
			f = PyFingerprint(self.com, self.port, 0xFFFFFFFF, 0x00000000)
			if ( f.verifyPassword() == False ):
				raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
				print('The fingerprint sensor could not be initialized!')
				print('Exception message: ' + str(e))
				exit(1)

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to enroll new finger
		try:
				
				empoly_number = input('\n[SET]Please input the Employee No , (ex.48628) = ')  
				if len(empoly_number) ==0:
					raise Exception('Empoly number error')
				
				print('[INFO]Waiting for finger...')
				## Wait that finger is read
				while ( f.readImage() == False ):
						pass

				## Converts read image to characteristics and stores it in charbuffer 1
				f.convertImage(0x01)

				## Checks if finger is already enrolled
				result = f.searchTemplate()
				positionNumber = result[0]

				if ( positionNumber >= 0 ):
						print('Template already exists  #' + str(empoly_number))
						exit(0)

				print('Remove finger...')
				time.sleep(2)

				print('[INFO]Waiting for same finger again...')

				## Wait that finger is read again
				while ( f.readImage() == False ):
						pass

				## Converts read image to characteristics and stores it in charbuffer 2
				f.convertImage(0x02)

				## Compares the charbuffers
				if ( f.compareCharacteristics() == 0 ):
						raise Exception('Fingers do not match')

				## Creates a template
				f.createTemplate()

				## Saves template at new position number
				positionNumber = f.storeTemplate()
				
				
				cw = open("./data_log.csv",'a+')
				cw.write(str(positionNumber) +","+str(empoly_number)+"\n")
								
				print('[OK]Finger enrolled successfully!')
				print('[OK]New template position #' + str(empoly_number))

		except Exception as e:
				print('Operation failed!')
				print('Exception message: ' + str(e))
				exit(1)
				
	def predict(self):

		try:
				f = PyFingerprint(self.com,self.port, 0xFFFFFFFF, 0x00000000)

				if ( f.verifyPassword() == False ):
						raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
				print('The fingerprint sensor could not be initialized!')
				print('Exception message: ' + str(e))
				exit(1)

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to search the finger and calculate hash
		try:
				print('Waiting for finger...')

				## Wait that finger is read
				while ( f.readImage() == False ):
						pass

				## Converts read image to characteristics and stores it in charbuffer 1
				f.convertImage(0x01)

				## Searchs template
				result = f.searchTemplate()

				positionNumber = result[0]
				accuracyScore = result[1]

				if ( positionNumber == -1 ):
						print('No match found!')
						exit(0)
				else:
					with open('./data_log.csv', 'r') as file:
						self.rows = csv.DictReader(file)
						for row in self.rows:
							if row['positionnumber'] ==str(positionNumber):
								print('Name :',row['empolynumber'])
							
						#print('\nName : ', self.data_empoly[positionNumber])
						#print('Found template at position #' + str(positionNumber))
						print('The accuracy score is: ' + str(accuracyScore))

				## OPTIONAL stuff
				##

				## Loads the found template to charbuffer 1
				f.loadTemplate(positionNumber, 0x01)

				## Downloads the characteristics of template loaded in charbuffer 1
				characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

				## Hashes characteristics of template
				#print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

		except Exception as e:
				print('Operation failed!')
				print('Exception message: ' + str(e))
				exit(1)
				
	def delete(self):
		try:
			f = PyFingerprint(self.com, self.port, 0xFFFFFFFF, 0x00000000)

			if ( f.verifyPassword() == False ):
				raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
			print('The fingerprint sensor could not be initialized!')
			print('Exception message: ' + str(e))
			exit(1)

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to delete the template of the finger
		try:
			positionNumber = input('Please enter the template position you want to delete: ')
			positionNumber = int(positionNumber)

			if ( f.deleteTemplate(positionNumber) == True ):
				with open('./data_log.csv', 'r') as inp, open('./data_log_edit.csv', 'w') as out:
					writer = csv.writer(out)
					rows = csv.DictReader(inp)
					writer.writerows([['positionnumber']+['empolynumber']])
					for row in rows:		
						if row['positionnumber'] != str(positionNumber):
							writer.writerow([row['positionnumber'],row['empolynumber']])
				os.rename('./data_log_edit.csv','./data_log.csv')
				print('Template deleted!')

		except Exception as e:
			print('Operation failed!')
			print('Exception message: ' + str(e))
			exit(1)
			
	def index(self):

	## Tries to initialize the sensor
		try:
			f = PyFingerprint(self.com, self.port, 0xFFFFFFFF, 0x00000000)

			if ( f.verifyPassword() == False ):
				raise ValueError('The given fingerprint sensor password is wrong!')

		except Exception as e:
			print('The fingerprint sensor could not be initialized!')
			print('Exception message: ' + str(e))
			exit(1)

		## Gets some sensor information
		print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

		## Tries to show a template index table page
		try:
			page = input('Please enter the index page (0, 1, 2, 3) you want to see: ')
			page = int(page)

			tableIndex = f.getTemplateIndex(page)

			for i in range(0, len(tableIndex)):
				print('Template at position #' + str(i) + ' is used: ' + str(tableIndex[i]))

		except Exception as e:
			print('Operation failed!')
			print('Exception message: ' + str(e))
			exit(1)




if __name__ == "__main__":
	com = '/dev/ttyAMA0'
	port = 57600
	func_name = ARGS.function
	maincode = Fingerprint(com,port)	
	Target_function = getattr(maincode, func_name)
	Target_function()

	
