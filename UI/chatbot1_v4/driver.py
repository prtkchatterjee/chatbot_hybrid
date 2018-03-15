from time import sleep
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import re, math
from collections import Counter
import random
from sklearn.externals import joblib
def test(x):
	return x
def get_cosine(vec1, vec2):
	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])

	sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)

	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator

def text_to_vector(text):
	words = WORD.findall(text)
	return Counter(words)

f = open('Data.txt','r')
data = f.readlines()
for i in range(len(data)):
	data[i] = data[i][2:len(data[i])-1]
questions = data[::2]
answers = data[1::2]
reference_table = {}
for i in range(len(questions)):
	if(questions[i] in reference_table):
		reference_table[questions[i]].append(answers[i])
	else:
		reference_table[questions[i]] = [answers[i]]
questions = list(set(questions))
c = 0
t = []
q = []
num = len(questions)
for i in range(len(questions)):
	t.append(questions[i])
	c += 1
	if c == 5:
		q.append(t)
		c = 0
		t = []
if(len(t)>0):
	q.append(t)

documents = q
mark = []
for i in documents:
	for j in i:
		mark.append(0)
vectorizer = TfidfVectorizer(analyzer=test)
X = vectorizer.fit_transform(documents)
true_k = 5
model = joblib.load('clustering.pkl')
#print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
clusters = []
for i in range(true_k):
	t = []
	#print("Cluster %d:" % i)
	for ind in order_centroids[i, :10]:
		if(mark[ind] == 0):
			#print(' %s' % terms[ind])
			t.append(terms[ind])
			mark[ind] = 1
	clusters.append(t)
while(True):	
	cosine_values = []
	text1 = ""
	with open('driver_inp.txt', 'r') as the_file:
		text1 = the_file.readline()
		if text1 != "":
			with open('driver_inp.txt', 'w') as f1:
				f1.write("")
		else:
			continue
	line = open("ProfanityCorpus.txt").read().splitlines()
	flag = False
	for i in line :
    		if i.split(",")[0] in text1.lower().split(" "):
        		no = int(i.split(",")[1])
        		if no == 1 :
            			continue
        		if no == 2 :
            			print("You don't really expect me to answer that, do you?")
        		if no == 3 :
            			print("Well you need to wash your mouth with soap  ")
        		if no == 4 :
            			print("I have your mum on speed dial.")
        		if no == 5 :
            			print("Well, I think we've reached the end of this conversation.")
        		flag = True
        		break
	if flag:
		continue
	Y = vectorizer.transform([text1])
	prediction = model.predict(Y)
	# print(prediction[0])
	query_cluster = prediction[0]

	WORD = re.compile(r'\w+')

	for ind in order_centroids[query_cluster, :10]:
		text2 = terms[ind]
		# print(' %s' % terms[ind])
		vector1 = text_to_vector(text1)
		vector2 = text_to_vector(text2)
		cosine = get_cosine(vector1, vector2)
		cosine_values.append(cosine)

	max_cosine_index = cosine_values.index(max(cosine_values))
	#print("Similarity:",max_cosine_index)
	indi = -1
	if cosine_values[max_cosine_index] < 0.6:
		with open('ip1.txt', 'w') as the_file:
			the_file.write(text1)
			indi = 0
	else:
		with open('ip2.txt', 'w') as the_file:
			the_file.write(text1)
			indi = 1
	sleep(30)
	while(True):
		op = ""
		with open('op.txt', 'r') as the_file:
			op = the_file.readline()
		op = op.strip()
		if op != "":
			print("Output")
			with open('op.txt', 'w') as f1:
				f1.write("")
			flag = False
			for i in line :
				if i.split(",")[0] in op.lower().split(" "):
					no = int(i.split(",")[1])
					if no == 1 :
						continue
					if no == 2 :
						print("I'm bored! Lets change the topic")
					if no == 3 :
						print("I'd rather not say")
					if no == 4 :
						print("I dont think I should speak up for that")
					if no == 5 :
						print("My words are not appropriate for your ears")
					flag = True
					break
			if flag:
				continue
			with open('driver_op.txt', 'w') as f1:
				if(indi == 0):
					f1.write("Mr. Context: "+op)
				else:
					f1.write("Mrs. Personality: "+op)
				break
