from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import re, math
from collections import Counter
import random
from sklearn.externals import joblib

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
def test(x):
	return x
vectorizer = TfidfVectorizer(analyzer=test)
X = vectorizer.fit_transform(documents)
true_k = 5
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)
joblib.dump(model,'clustering.pkl')
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
cosine_values = []
text1 = input("User: ")
Y = vectorizer.transform([text1])
prediction = model.predict(Y)
# print(prediction[0])
query_cluster = prediction[0]

WORD = re.compile(r'\w+')

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

for ind in order_centroids[query_cluster, :10]:
    text2 = terms[ind]
    # print(' %s' % terms[ind])
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)
    cosine = get_cosine(vector1, vector2)
    cosine_values.append(cosine)

max_cosine_index = cosine_values.index(max(cosine_values))
#most_similar = terms[order_centroids[query_cluster, max_cosine_index]]

#print("Similarity:",cosine_values[max_cosine_index],"Most Similar Question:",most_similar)

#print("Most Similar Answer:",reference_table[most_similar][random.randint(0,len(reference_table[most_similar])-1)])
