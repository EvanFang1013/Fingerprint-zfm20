            
import csv
import os
import pandas as pd
import numpy as np

#with open('./data_log.csv', 'r') as inp, open('./data_log123.csv', 'w') as out:
	#writer = csv.writer(out)
	#rows = csv.DictReader(inp)
	#writer.writerows([['positionnumber']+['empolynumber']])
	#for row in rows:		
		#if row['positionnumber'] != '2':
				#writer.writerow([row['positionnumber'],row['empolynumber']])
#os.rename('./data_log123.csv','./data_log.csv')

df = pd.read_csv('./data_log.csv')
data_empoly = []
#[data_empoly.append(i) for i in df.empolynumber ]
for row in df.positionnumber:

	if row ==0 :
		print(df.empolynumber)

		
		
			

		
		
