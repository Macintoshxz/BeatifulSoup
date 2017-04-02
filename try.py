from bs4 import BeautifulSoup
import os
from urllib.request import Request, urlopen
import re
import random
from random import randrange

os.chdir('C:/Users/Macintoshx/Documents/BeautifulSoup/trialdata')

# select files

def make_soup(url):
	html = open(url)
	return BeautifulSoup(html, 'lxml')

file = 'SplittableRandom.html'
soup = make_soup(file)


for findboth in soup.body.find_all('div', class_ = 'details'):
	for remove_span in (div for div in soup.body.find_all('div', class_ = 'block') if div.find('span')):
		remove_span.decompose()

	ans_resultset = findboth.find_all('div', class_ = 'block')
	print('removing... the sorted data left: %d' % len(ans_resultset))

q_list1 = []

for findQue in findboth.find_all('li', class_ = 'blockList'):
	q_list1.extend(findQue.find_all('pre', recursive = False))


a_list = []
for elements in ans_resultset:
	a_list.extend([elements.get_text()])

q_list=[]
for element in q_list1:
	q_list.append(element.get_text())
del(q_list1)



tided_q_list = []
tided_a_list = []

def tide_list (x, y):
	for element in x:
		element = ' '.join(re.findall(r'[\S.]+', element))
		y.append(element)
	return y

tide_list(q_list, tided_q_list)
tide_list(a_list, tided_a_list)


def create_distractor(ori_list):
    index_list= []
    distractor_list = []
    
    for n in range(0, len(ori_list)):

        while len(distractor_list) != len(ori_list):
            random_index = random.randrange(0, len(ori_list))
            if random_index in index_list or random_index == n:
                continue
            else:
                index_list.append(random_index)
                distractor_list.append(ori_list[random_index])
                break
    return distractor_list


def muti_distractor(ori_list):    
    distractor_dict = {}

    for x in range (0,10):
         distractor_dict['distractor_{0}'.format(x)] = create_distractor(ori_list)
    return distractor_dict

distractor_list = create_distractor(tided_q_list)
distractor_dict = muti_distractor(tided_q_list)


from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

    
lemmatizer = WordNetLemmatizer()
snowball_stemmer = SnowballStemmer('english')

def token_lemma(y):
#     x =[]
    x = y[:]
    
    for n in range (0, len(x)):
        x[n] = word_tokenize(x[n])
        
        for m in range (0, len(x[n])):      
            x[n][m] = lemmatizer.lemmatize(x[n][m],wordnet.VERB)
            x[n][m] = lemmatizer.lemmatize(x[n][m],wordnet.NOUN)
        
            for m in range(0,len(x[n])):
                x[n][m] = snowball_stemmer.stem(x[n][m])
        x[n] = ' '.join(x[n])
    return x




label_train = [1] * len(tided_q_list) + [0] *len(tided_q_list)
print(len(label_train)) # training set of Label
print(label_train)

distractor0 = list(distractor_dict['distractor_1'])
distractor1 = list(distractor_dict['distractor_2'])
distractor2 = list(distractor_dict['distractor_3'])
distractor3 = list(distractor_dict['distractor_4'])
distractor4 = list(distractor_dict['distractor_5'])
distractor5 = list(distractor_dict['distractor_6'])
distractor6 = list(distractor_dict['distractor_7'])
distractor7 = list(distractor_dict['distractor_8'])
distractor8 = list(distractor_dict['distractor_9'])

train_q_list = token_lemma(tided_q_list[:])
train_q_list.extend(token_lemma(list(distractor_dict['distractor_0']))) # training set of A
train_a_list = token_lemma(tided_a_list[:])
train_a_list.extend(train_a_list)

test_a_test = token_lemma(tided_a_list[:])  # testing set of A
test_q_test = token_lemma(tided_q_list[:])

token_lemma_distractor0 = token_lemma(distractor0)
token_lemma_distractor1 = token_lemma(distractor1)
token_lemma_distractor2 = token_lemma(distractor2)
token_lemma_distractor3 = token_lemma(distractor3)
token_lemma_distractor4 = token_lemma(distractor4)
token_lemma_distractor5 = token_lemma(distractor5)
token_lemma_distractor6 = token_lemma(distractor6)
token_lemma_distractor7 = token_lemma(distractor7)
token_lemma_distractor8 = token_lemma(distractor8)

os.chdir('C:/Users/Macintoshx/Documents/BeautifulSoup/')

import os, csv

with open("train_token_lemma_try4.csv", "w") as toWrite:   #training set file csv
    writer = csv.writer(toWrite)
    writer.writerow(['context','utterance','label'])
    writer.writerows(zip(train_a_list,train_q_list, label_train))

with open("test_token_lemma_try4.csv", "w") as toWrite:   #training set file csv
    writer = csv.writer(toWrite)
    writer.writerow(['Context','Ground  Truth Utterance','Distractor_0','Distractor_1',\
                     'Distractor_2','Distractor_3','Distractor_4','Distractor_5',\
                     'Distractor_6','Distractor_7','Distractor_8'])
    writer.writerows(zip(test_a_test, test_q_test,token_lemma_distractor0,\
                         token_lemma_distractor1,token_lemma_distractor2,\
                         token_lemma_distractor3,token_lemma_distractor4,\
                         token_lemma_distractor5,token_lemma_distractor6,\
                         token_lemma_distractor7,token_lemma_distractor8))