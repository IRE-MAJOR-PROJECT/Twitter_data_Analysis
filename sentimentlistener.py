# sentimentlisener.py
"""Script that searches for tweets that match a search string
and tallies the number of positive, neutral and negative tweets."""
import keys
import sys
from textblob import TextBlob
import tweepy
import preprocessor as p
import tweepy
import re
import string
import os
import csv
from operator import add
from scipy import spatial
import glob
import sys
import numpy as np
from scipy.spatial import distance
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import random
import heapq
from sklearn.metrics.pairwise import cosine_similarity
# from summarization import get_sentences, get_vectors, ranking, beam_search
import nltk
import pandas as pd
import re
import networkx as nx
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import glob
from nltk.tokenize import sent_tokenize
from geopy import OpenMapQuest
import folium
import sys

nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
sent = open("sentiment.txt", "a")

def sentiment():
    tweet_files = glob.glob("tweet_location/*")
    for file in tweet_files:
        print(file)
        with open(file, "r") as f:
            lines = f.readlines()
            for line in lines:
                tweet = line.split('|')
                tweet_text = tweet[0]
                # update self.sentiment_dict with the polarity
                blob = TextBlob(tweet_text)
                if blob.sentiment.polarity > 0:
                    sent.write(tweet_text + "|" + "Positive" + "|" + tweet[2])
                elif blob.sentiment.polarity == 0:
                    sent.write(tweet_text + "|" + "Neutral" + "|" + tweet[2])
                else:
                    sent.write(tweet_text + "|" + "Negative" + "|" + tweet[2])
        summarization()

# -*- coding: utf-8 -*-
"""SUMMARIZATION.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BLNiH1k5ySQAcNTT24hgxfbe9vTsML88
"""
def summarization():
    fn = open("summarized_tweet.txt", "a")
    word_embeddings = {}
    f = open('glove.6B.100d.txt', encoding='utf-8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()


    # def get_sentences(tag):
    def get_sentences():
        # files = glob.glob("../data/tweets/"+tag+"/*")
        # files=open("/content/drive/My Drive/us_elections1.txt","r")
        sentences = []
        # for file in files:
        fd = open("sentiment.txt","r")
        for line in fd:
            sentences.append(line)
        fd.close()
        return sentences

    def get_vectors(sentences,model):
        sen_vectors = []
        for sentence in sentences:
            test_data = word_tokenize(sentence.lower())
            v1 = model.infer_vector(test_data)
            sen_vectors.append(v1)
        return sen_vectors

    def sentence_tokenize(tweets):
        sentences = []
        for tweet in tweets:
            sentences.append(sent_tokenize(tweet))
        sentences = [y for x in sentences for y in x]
        return sentences

    def remove_stopwords(sen):
        sen_new = " ".join([i for i in sen if i not in stop_words])
        return sen_new


    def text_processing(sentences):
        clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")
        clean_sentences = [s.lower() for s in clean_sentences]
        clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]
        return clean_sentences

    def vector_representations(clean_sentences):
        sentence_vectors = []
        for i in clean_sentences:
            if len(i) != 0:
                v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
            else:
                v = np.zeros((100,))
            sentence_vectors.append(v)
        return sentence_vectors

    def similarity_matrix(sentence_vectors):
        sim_mat = np.zeros([len(sentence_vectors), len(sentence_vectors)])
        for i in range(len(sentence_vectors)):
            for j in range(len(sentence_vectors)):
                if i != j:
                    sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
        return sim_mat

    def apply_pagerank(sim_mat):
        nx_graph = nx.DiGraph(sim_mat)
        scores = nx.pagerank(nx_graph)
        return scores

    def summary_extraction(scores,sentences,k):
        ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
        for i in range(k):
            fn.write(ranked_sentences[i][1] + "\n")
            print(ranked_sentences[i][1])

    sentences = get_sentences()
    sentences = sentence_tokenize(sentences)
    clean_sentences = text_processing(sentences)
    sentence_vectors = vector_representations(clean_sentences)
    sim_mat = similarity_matrix(sentence_vectors)
    scores = apply_pagerank(sim_mat)
    summary_extraction(scores,sentences,5)
    fn.close()
    geomap()

def geomap():
    mapquest_key = 'ATbf4YYsSjOwhAKJi5Xy1tMyHMn459G9'

    usmap = folium.Map(location=[39.8283, -98.5795], tiles='Stamen Terrain', zoom_start=5, detect_retina=True)

    with open ("summarized_tweet.txt", "r") as f:
        lines = f.readlines()
        for row, line in enumerate(lines, start=1):
            location = line.split('|')
            text = location[0]
            x = location[2]

            geo = OpenMapQuest(api_key=mapquest_key)
            try:
                geo_location = geo.geocode(x)
            except:
                print('OpenMapQuest service timed out. Waiting.')
            if geo_location:  
                a = geo_location.latitude
                b = geo_location.longitude
                popup = folium.Popup(text, parse_html=True)
                # marker = folium.Marker((a, b),popup=popup, marker_icon='cloud')
                if "Positive" in location[1]:
                    marker = folium.Marker((a,b),
                        popup=popup, icon=folium.Icon(color='green', icon='cloud'))
                    marker.add_to(usmap)
                elif "Neutral" in location[1]:
                    marker = folium.Marker((a,b),
                        popup=popup, icon=folium.Icon(color='orange', icon='cloud'))
                    marker.add_to(usmap)
                else:
                    marker = folium.Marker((a,b),
                        popup=popup, icon=folium.Icon(color='red', icon='cloud'))
                    marker.add_to(usmap)
            else:
                pass
    
    #Saving the Map
    usmap.save('tweet_map.html')

if __name__ == '__main__':
    sentiment()