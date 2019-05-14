
# coding: utf-8



class Reader:
    
    def read_files(self,filename):
        results = {}
        with open(filename, "r", encoding="utf-8") as file:
            for line in file.readlines():
                splited = line.replace("\n", "").split("\t")
                #print(splited)
                result, score = splited[0],splited[1]
                results[result.lower()] = score
        return results

import nltk
import os
import re
import json
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
import textblob
from textblob import TextBlob
from urllib.request import urlretrieve
from imageai.Detection import ObjectDetection
#from nltk import wordnet
reader = Reader()

def get_hashtags(text):
    
    hashtags = []
    for word in text:
        if word.startswith('#'):
            hashtags.append(word)
            text = [token for token in text if token != word]
    return text, hashtags

def get_punctuations(text):
 
    punctuations = []
    new_text = []
    for word in text:
        if re.search('[\s+\.\!\?\-\/_,$^*(+\"]+|[+——！，。？、~@#￥%……&*:;（）<=>“]+',word) != None:
            tokens = list(word)
            for character in tokens:
                if character == '?' or character == '!':
                    punctuations.append(character)
                    tokens = [char for char in tokens if char != character]
                elif re.match('[\s+\.\-\/_,$%^*(+\"]+|[+——！，。？、~@#￥%……:;&*（）<=>”]+',character):
                    tokens = [char for char in tokens if char != character]
            tokens = ''.join(tokens)
            if tokens != '':
                new_text.append(tokens)
        else:
            new_text.append(word)
            
    return new_text, punctuations
    
def is_emoji(word):
    
    if not word:
        return False
    if u"\U0001F600" <= word and word <= u"\U0001F64F":
        return True
    elif u"\U0001F300" <= word and word <= u"\U0001F5FF":
        return True
    elif u"\U0001F680" <= word and word <= u"\U0001F6FF":
        return True
    elif u"\U0001F1E0" <= word and word <= u"\U0001F1FF":
        return True
    else:
        return False

def process_expressions(text):
    
    expressions = []
    new_text = []
    for token in text:
        if re.search(r'[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U0001F1E0-\U0001F1FF]',token) != None:
            tokens = list(token)
            #print(tokens)
            for character in tokens:
                if is_emoji(character):
                    code = f'U+{ord(character):X}'
                    expressions.append(code)
                    tokens = [char for char in tokens if char != character]
            tokens = ''.join(tokens)
            if tokens != '':
                new_text.append(tokens)
        else:
            new_text.append(token)
            
    return new_text, expressions

def remove_number(text):
    
    text = [word for word in text if not word.isdigit()]
    return text

def remove_handles(text):
    
    for token in text:
        word_compiled = re.compile('@')
        if word_compiled.match(token) != None:
            text = [word for word in text if word != token]
    return text

def remove_stopwords(text):
    
    stop_words = stopwords.words('english')
    text = [word for word in text if word not in stop_words]
    return text

def remove_url(text):
    
    #print(text)
    results = re.compile(r'https?://[a-zA-Z0-9.?/&=:]*',re.S)
    text = results.sub("",text)
    return text
    
def preprocessing(text):
    
    text = remove_url(text)
    text = text.split()
    text = remove_handles(text)
    text = remove_number(text)
    text = remove_stopwords(text)
    text,expressions = process_expressions(text)
    text,hashtags = get_hashtags(text)
    text,punctuations = get_punctuations(text)
    text = [token.lower() for token in text]
    return text,expressions,hashtags,punctuations




ADVERBS = reader.read_files("lexicons/list-English-adverbs.txt")
ANGRYS = reader.read_files("lexicons/lexicons_angry.txt")
ANTICIPATIONS = reader.read_files("lexicons/lexicons_anticipation.txt")
HASHTAG_ANGRY_LIST = reader.read_files("lexicons/lexicons_hashtags_angry.txt")
HASHTAG_ANTICIPATION_LIST = reader.read_files("lexicons/lexicons_hashtags_anticipation.txt")
FOODS = reader.read_files("lexicons/food_list.txt")

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()

#from nltk.stem import WordNetLemmatizer
wnl = nltk.stem.WordNetLemmatizer()

def count_expressions(expressions,expressions_list):
    
    count = 0
    for expression in expressions:
        if expression in expressions_list:
            count += 1
    return count

def count_punctuations(punctuations):
    
    if len(punctuations) > 2:
        return len(punctuations) - 2
    else:
        return 0

def count_hashtags(hashtags,hashtag_list):
    
    values = []
    for hashtag in hashtags:
        if hashtag in hashtag_list:
            value = float(hashtag_list[hashtag])
            values.append(value)
    return values

def process_images(url):
    #count = 1
    if url != None:
        #print(count)
        #count+=1
        index = 0
        try:
            urlretrieve(url, 'image/img' + str(index) + '.jpg') 
        except:
            return 0
        execution_path = os.getcwd()
        detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , 'image/img' + str(index) + '.jpg'), output_image_path=os.path.join(execution_path , 'image/img' + str(index) + 'new.jpg'))
        for eachObject in detections:
            if eachObject["name"] in ['bottle','wine glass','cup','fork', 'knife','spoon','bowl','banana','apple','sandwich','orange','broccoli', 'carrot', 'hot dog','pizza','donot','cake']:
                return 1
    return 0

def process_words(text,emotion,lexicons):
    
    privatives = ['not','cannot','no','never']
    value = float(0)
    
    for token in text:
        #if token in lexicons and reader.get_emotion(token,emotion,lexicons) != None:
        if token in lexicons:
            #value = value * float(reader.get_emotion(token,emotion,lexicons))
            value += 1
            if emotion == 'anticipation':
                value = value * 0.4
        if emotion == 'anticipation' and wnl.lemmatize(token) in FOODS:
            value += 1
        if token in ADVERBS:
            value = value * float(ADVERBS[token])
        if re.search("n't",token) != None or token in privatives:
            value = value * (-1)
    
    return value

def sentiment_analyse_angry(text):

    text = initial_text_processing(text)
    text, expressions, hashtags, punctuations = preprocessing(text)
    value = process_words(text,'anger',ANGRYS)
    expressions_list = ['U+1F624','U+1F621','U+1F620','U+1F92C','U+1F608','U+1F47F','U+1F480','U+2620','U+1F47A','U+1F63E','U+1F5EF']
    num_expressions = count_expressions(expressions,expressions_list)
    num_punctuations = count_punctuations(punctuations)
    value_hashtags = count_hashtags(hashtags,HASHTAG_ANGRY_LIST)
    total = value + (num_expressions + num_punctuations) * 0.8 + sum(value_hashtags)
    if total >= 1:
        return "angry"
    return "not_angry"

def sentiment_analyse_gluttony(text, url):
    
    text = initial_text_processing(text)
    text, expressions, hashtags, punctuations = preprocessing(text)
    value = process_words(text,'anticipation', ANTICIPATIONS)
    expressions_list = ['U+1F970','U+1F60D','U+1F929','U+1F618','U+1F60B','U+1F347','U+1F348','U+1F349','U+1F34A','U+1F34B','U+1F34C','U+1F34D','U+1F34E','U+1F34F','U+1F96D','U+1F350','U+1F351','U+1F352','U+1F353','U+1F345','U+1F95D','U+1F965','U+1F951','U+1F346','U+1F954','U+1F955','U+1F33D','U+1F336','U+1F952','U+1F96C','U+1F966','U+1F9C4','U+1F9C5','U+1F344','U+1F95C','U+1F330','U+1F35E','U+1F950','U+1F956','U+1F968','U+1F96F','U+1F95E','U+1F9C7','U+1F9C0','U+1F356','U+1F357','U+1F969','U+1F953','U+1F354','U+1F35F','U+1F355','U+1F32D','U+1F96A','U+1F32E','U+1F32F','U+1F959','U+1F37F','U+1F359','U+1F363','U+1F990','U+1F99E','U+1F980','U+1F366','U+1F367','U+1F369','U+1F36A','U+1F382','U+1F370','U+1F9C1','U+2615','U+1F377','U+1F378','U+1F37A','U+1F37B','U+1F942','U+1F95F','U+1F35A','U+1F35C']    
    num_expressions = count_expressions(expressions,expressions_list)
    image_value = process_images(url)
    #num_punctuations = count_punctuations(punctuations)
    value_hashtags = count_hashtags(hashtags,HASHTAG_ANTICIPATION_LIST)
    total = value + num_expressions * 0.8 + sum(value_hashtags) + image_value
    if total >= 1:
        return "gluttony"
    return "not_gluttony"

def initial_text_processing(text):

    blob = TextBlob(text)
    text = str(blob.correct())
    return text

# def analyse(filename):
#     import time
#     with open(filename) as file:
#         line = file.readline()
#         line = file.readline()
#         #print(line)
#         while line:
#             start = time.clock()
#             line = line[:-2]
#             line = json.loads(line)
            
#             line['angry'] = 0
#             line['gluttony'] = 0
#             text = line['doc']['text']
#             url = line['doc']['image']
#             #print(url)
#             blob = TextBlob(text)
#             text = str(blob.correct())
#             #print(text)
#             result1 = sentiment_analyse_angry(text)
#             if result1 >= 1:
#                 line['angry'] = 1
                
#             result2 = sentiment_analyse_gluttony(text,url)
#             if result2 >= 1:
#                 line['gluttony'] = 1
#                 print('gluttony')
#             elapsed = (time.clock() - start)
#             print(elapsed)
#             line = file.readline()

# analyse('data.json')

