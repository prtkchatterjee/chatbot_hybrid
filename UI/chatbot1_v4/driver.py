from time import sleep
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import re, math
from collections import Counter
import random
from sklearn.externals import joblib
from textblob import TextBlob
from nltk.corpus import brown
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
'''true_k = 5
model = joblib.load('clustering.pkl')
#print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]'''
terms = vectorizer.get_feature_names()
'''clusters = []
for i in range(true_k):
	t = []
	#print("Cluster %d:" % i)
	for ind in order_centroids[i, :10]:
		if(mark[ind] == 0):
			#print(' %s' % terms[ind])
			t.append(terms[ind])
			mark[ind] = 1
	clusters.append(t)'''
while(True):	
	cosine_values = {}
	text1 = ""
	with open('driver_inp.txt', 'r') as the_file:
		text1 = the_file.readline()
		if text1 != "":
			with open('driver_inp.txt', 'w') as f1:
				f1.write("")
		else:
			continue
	print(">",text1)
	emojis = [':D',':P',':-D',':-P',':)',':-)',':(',':-(',':(']
	for i in emojis:
		if i in text1:
		    text1 = text1.replace(i,"")
	line = open("ProfanityCorpus.txt").read().splitlines()
	flag = False
	greeting_inputs = ["hey","hi","hello"]
	greeting_replies = ["What's up?","How's life?","Greetings"]
	greeting_indi = False
	for j in ''.join(e for e in text1.lower() if (e.isalnum() or e == ' ')).split(" "):
		if j in greeting_inputs:
			random_index = random.randint(0,len(greeting_replies)-1)
			with open('driver_op.txt', 'w') as f1:
        			f1.write(greeting_replies[random_index] + ";3")
			print(greeting_replies[random_index])
			greeting_indi = True
	if greeting_indi:
		continue
	for i in line :
    		if i.split(",")[0] in ''.join(e for e in text1.lower() if (e.isalnum() or e == ' ')).split(" "):
        		no = int(i.split(",")[1])
        		if no == 1 :
        			continue
        		stat_op = ""
        		if no == 2 :
        			stat_op = "You don't really expect me to answer that, do you?"
        		if no == 3 :
        			stat_op = "Well you need to wash your mouth with soap  "
        		if no == 4 :
        			stat_op = "I have your mum on speed dial."
        		if no == 5 :
        			stat_op = "Well, I think we've reached the end of this conversation."
        		print(stat_op)
        		with open('driver_op.txt', 'w') as f1:
        			f1.write(stat_op + ";-1")
        		flag = True
        		break
	if flag:
		continue
	generic_replies = ["Point noted.","Cool!","Got it!","I see","Oh okay!"]
	sentiment = TextBlob(text1.lower())
	print("Sentiment Score: ", sentiment.sentiment.polarity)
	if sentiment.sentiment.polarity >= -0.01 and sentiment.sentiment.polarity <= 0.01 and text1[len(text1)-1:] != "?":
		random_index = random.randint(0,len(generic_replies)-1)
		print(generic_replies[random_index])
		with open('driver_op.txt', 'w') as f1:
        		f1.write(generic_replies[random_index]+";-1")
		continue
	Y = vectorizer.transform([text1])
	'''prediction = model.predict(Y)
	# print(prediction[0])
	query_cluster = prediction[0]'''

	WORD = re.compile(r'\w+')

	'''for ind in order_centroids[query_cluster, :10]:
		text2 = terms[ind]
		# print(' %s' % terms[ind])
		vector1 = text_to_vector(text1)
		vector2 = text_to_vector(text2)
		cosine = get_cosine(vector1, vector2)
		cosine_values.append(cosine)'''
	for i in reference_table:
		vector1 = text_to_vector(text1.lower())
		vector2 = text_to_vector(i.lower())
		cosine = get_cosine(vector1, vector2)
		cosine_values[i] = cosine
	max_cosine_value = 0
	most_similar = ""
	for i in cosine_values:
		if(cosine_values[i] > max_cosine_value):
			max_cosine_value = cosine_values[i]
			most_similar = i
	print("Max. Cosine Value:",max_cosine_value)
	print("Most Similar:",most_similar)
	indi = -1
	if max_cosine_value < 0.6:
		with open('ip1.txt', 'w') as the_file:
			the_file.write(text1.lower())
			indi = 0
	else:
		#with open('ip2.txt', 'w') as the_file:
		#	the_file.write(text1.lower())
		#	indi = 1
		print("Mr. Context:",reference_table[most_similar])
		with open('op.txt', 'w') as the_file:
			the_file.write(reference_table[most_similar][random.randint(0,len(reference_table[most_similar])-1)])
	while(True):
		op = ""
		with open('op.txt', 'r') as the_file:
			op = the_file.readline()
		op = op.strip()
		if op != "":
			with open('op.txt', 'w') as f1:
				f1.truncate()
			with open('driver_op.txt', 'w') as f1:
				f1.truncate()
			flag = False
			for i in line :
				if i.split(",")[0] in ''.join(e for e in op.lower() if (e.isalnum() or e == ' ')).split(" "):
					no = int(i.split(",")[1])
					if no == 1 :
						continue
					stat_op = ""
					if no == 2 :
						stat_op = "I'm bored! Lets change the topic"
					if no == 3 :
						stat_op = "I'd rather not say"
					if no == 4 :
						stat_op = "I dont think I should speak up for that"
					if no == 5 :
						stat_op = "My words are not appropriate for your ears"
					flag = True
					print(stat_op)
					with open('driver_op.txt', 'w') as f1:
						f1.write(stat_op+";-1")
					break
			if flag:
				continue
			if "thread" in ''.join(e for e in op.lower() if (e.isalnum() or e == ' ')).split(" "):
				print("I'm bored! Lets change the topic")
				with open('driver_op.txt', 'w') as f1:
					f1.write("I'm bored! Lets change the topic;-1")
			sentiment = TextBlob(op.lower())
			sentiment_score = 0
			print("Sentiment Score: ", sentiment.sentiment.polarity)
			if sentiment.sentiment.polarity >= 0.8:
				sentiment_score = 3
			elif sentiment.sentiment.polarity >= 0.2 and sentiment.sentiment.polarity<0.8:
				sentiment_score = 2
			elif sentiment.sentiment.polarity >= -0.2 and sentiment.sentiment.polarity <0.2:
				sentiment_score = 1
			elif sentiment.sentiment.polarity < -0.6:
				sentiment_score = 0
			else:
				sentiment_score = -1
			with open('driver_op.txt', 'w') as f1:
				if(indi == 0):
					f1.write(op + ";" + str(sentiment_score))
					print("Mr. Context: "+op)
				else:
					f1.write(op + ";" + str(sentiment_score))
					print("Ms. Personality: "+op)
				break
