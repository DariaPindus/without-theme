import pandas as pd

headers = []
alternatives = []

class CustomDecisionException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def process_2_level_matrix(filepath):
	df=pd.read_csv(filepath, sep=',')
	df.drop(df.columns[0], inplace=True,axis=1)
	global headers
	headers = list(df)
	tw = df.apply(find_tw, axis=1)
	q2=calc_qn(df)
	return q2

def calc_qn(df):
	res = []	
	tw = df.apply(find_tw, axis=1)
	power = len(list(df))
 
	for index, row in df.iterrows():
		w = tw[index]**(1/float(power))
		res.append(w)
	r = sum(res)
	res[:]=map(lambda x: x/r, res)
	return res
	
#make lambda
def find_tw(row):
	val = 1
	for i, key in enumerate(row):
		val *= row[i]
	return val
	

def process_3_level_matrix():
	print "enter number of alternatives :"
	alt_number = int(raw_input())
	global alternatives
	print "enter ordered names of alternatives: "
	for i in range(0, alt_number):
		alternatives.append(raw_input())
	variant_matrix = init_variant_matrix(alt_number)

	for header in headers:
		q3 = get_criteria_grades(header)
		for i, key in enumerate(q3) :
			variant_matrix[i].append(key)
	return variant_matrix
  
def get_criteria_grades(criteria_name):
	df = {}
	while True:
		try:
			print "enter {} file source".format(criteria_name)
			source = raw_input()
			df=pd.read_csv(source, sep=',')
			break
		except IOError:
			print "file doesn't exist"		
	df.drop(df.columns[0], inplace=True,axis=1)
	q3=calc_qn(df)
	return q3
	
		
def init_variant_matrix(length):
	res = []
	for i in range(length):
		res.append([])
	return res

def main_file_flow():
	print("Enter full file path")
	path = raw_input()
	q2 = process_2_level_matrix(path)
	q3 = process_3_level_matrix()
	priorities_res = multiply_matrix_vector(q3, q2)
	show_user_priorities(priorities_res)

	
def multiply_matrix_vector(a, b):
	if len(a[0]) != len(b):
		raise CustomDecisionException('wrong matrixes')
	M = len(a)	
	N = len(b)
	res = [0] * M

	for i in range(M):
		val = 0
		for j in range(N):
			val += a[i][j] * b[j]
		res[i]=val
	return res	

def show_user_priorities(priorities_res):
	global alternatives
	print "Your result :"
	tuples = []
	for i in range(len(alternatives)):
		tuples.append((alternatives[i], priorities_res[i]))
	sorted(tuples, key=lambda x: x[1])
	for (i,j) in tuples:
		res_str = repr(i) + " - " + repr(j)
		print res_str

if __name__ == '__main__':
	#todo
	#print("Choose data source : \n1.csv \n2.console")
	#source = raw_input()
	#if(source == 1)
		main_file_flow()
