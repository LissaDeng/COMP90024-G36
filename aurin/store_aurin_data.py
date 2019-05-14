import couchdb
import json


def storeDiabetesData(filename, cityName, database):
	try:
		with open(filename, 'r') as file:
			data = json.load(file)
			if data['features']:
				for row in data['features']:
					if row['properties']:
						output_data = {'type': 'diabetes', 'city': cityName,\
						'area_name': row['properties']['area_name'],\
						'rate': row['properties']["diabetes_me_2_rate_3_11_7_13"]
						}
						database.save(output_data)
	except Exception as e:
		print('Error: ' + str(e))


def storeEducationData(filename, cityName, database):
	try:
		with open(filename, 'r') as file:
			data = json.load(file)
			if data['features']:
				for row in data['features']:
					if row['properties']:
						output_data = {'type': 'education', 'city': cityName,\
						'area_name': row['properties']['area_name'],\
						'rate': row['properties']['educatn_16_3_percent_6_11_6_11']
						}
						database.save(output_data)
	except Exception as e:
		print('Error: ' + str(e))


def storePovertyData(filename, cityName, database):
	try:
		with open(filename, 'r') as file:
			data = json.load(file)
			if data['features']:
				for row in data['features']:
					if row['properties']:
						output_data = {'type': 'poverty', 'city': cityName,\
						'area_name': row['properties']['sa2_name16'],\
						'rate': row['properties']['pov_rt_syn']
						}
						database.save(output_data)
	except Exception as e:
		print('Error: ' + str(e))


def storeMentalProblemData(filename, cityName, database):
	try:
		with open(filename, 'r') as file:
			data = json.load(file)
			if data['features']:
				for row in data['features']:
					if row['properties']:
						output_data = {'type': 'mental_problem', 'city': cityName,\
						'area_name': row['properties']['area_name'],\
						'rate': round(row['properties']['mntl_bh_p_me_2_rate_3_11_7_13'],3)
						}
						database.save(output_data)
	except Exception as e:
		print('Error: ' + str(e))


if __name__ == '__main__':
	dbServer = couchdb.Server('http://g36:1q2w3e@127.0.0.1:5984')
	db = dbServer['aurin']

	# Loads the diabetes data into the database
	storeDiabetesData('diabetes/diabetes_adelaide.json', 'adelaide', db)
	storeDiabetesData('diabetes/diabetes_brisbane.json', 'brisbane', db)
	storeDiabetesData('diabetes/diabetes_goldCoast.json', 'goldCoast', db)
	storeDiabetesData('diabetes/diabetes_melbourne.json', 'melbourne', db)
	storeDiabetesData('diabetes/diabetes_perth.json', 'perth', db)
	storeDiabetesData('diabetes/diabetes_sydney.json', 'sydney', db)

	storeEducationData('education/education_adelaide.json', 'adelaide', db)
	storeEducationData('education/education_brisbane.json', 'brisbane', db)
	storeEducationData('education/education_goldCoast.json', 'goldCoast', db)
	storeEducationData('education/education_melbourne.json', 'melbourne', db)
	storeEducationData('education/education_perth.json', 'perth', db)
	storeEducationData('education/education_sydney.json', 'sydney', db)

	storePovertyData('poverty/poverty_adelaide.json', 'adelaide', db)
	storePovertyData('poverty/poverty_brisbane.json', 'brisbane', db)
	storePovertyData('poverty/poverty_goldCoast.json', 'goldCoast', db)
	storePovertyData('poverty/poverty_melbourne.json', 'melbourne', db)
	storePovertyData('poverty/poverty_perth.json', 'perth', db)
	storePovertyData('poverty/poverty_sydney.json', 'sydney', db)

	storeMentalProblemData('mental_problems/mentalProblem_adelaide.json', 'adelaide', db)
	storeMentalProblemData('mental_problems/mentalProblem_brisbane.json', 'brisbane', db)
	storeMentalProblemData('mental_problems/mentalProblem_goldCoast.json', 'goldCoast', db)
	storeMentalProblemData('mental_problems/mentalProblem_melbourne.json', 'melbourne', db)
	storeMentalProblemData('mental_problems/mentalProblem_perth.json', 'perth', db)
	storeMentalProblemData('mental_problems/mentalProblem_sydney.json', 'sydney', db)




