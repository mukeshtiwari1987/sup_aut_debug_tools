import csv

def ftm():
	with open("18may19.csv") as csv_file:
		csv_reader = list(csv.DictReader(csv_file, delimiter=','))
	return csv_reader

def im(cr):
	for row in cr:
		print(row['hashed_id'])

cr = ftm()
im(cr)
