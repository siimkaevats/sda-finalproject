

from django.http import HttpResponse
from django.shortcuts import render
import string
from collections import Counter
import sys
import re
import nltk
import numpy

import bs4 as bs
import urllib.request

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from textblob import TextBlob

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import word_tokenize, sent_tokenize
import numpy as np

from nltk.cluster.util import cosine_distance
import networkx as nx

import wikipedia
import heapq
from pyfiglet import Figlet

def index(request):
    return render(request, 'index.html')


def analyze(request):

    global in_a_sentence, count, blob, analyzed, stopwords
    djtext = request.POST.get('text', 'default')

    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    lowercase = request.POST.get('lowercase', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    countcharacters = request.POST.get('countcharacters', 'off')
    spellcheck = request.POST.get('spellcheck', 'off')
    generatesummary = request.POST.get('generatesummary', 'off')
    removestopwords = request.POST.get('removestopwords', 'off')



    if removepunc == "on":
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        analyzed = ""
        for char in djtext:
            if char not in punctuations:
                analyzed = analyzed + char

        params = {'purpose':'Removed Punctuations', 'analyzed_text': analyzed}
        djtext = analyzed

    if(fullcaps=="on"):
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.upper()

        params = {'purpose': 'Uppercase', 'analyzed_text': analyzed}
        djtext = analyzed

    if(lowercase=="on"):
        analyzed = ""
        for char in djtext:
            analyzed = analyzed + char.lower()

        params = {'purpose': 'LowerCase', 'analyzed_text': analyzed}
        djtext = analyzed

    if(extraspaceremover=="on"):
        analyzed = ""
        for index, char in enumerate(djtext):
            if not(djtext[index] == " " and djtext[index+1]==" "):
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        djtext = analyzed

    if (newlineremover == "on"):
        analyzed = ""
        for char in djtext:
            if char != "\n" and char!="\r":
                analyzed = analyzed + char

        params = {'purpose': 'Removed NewLines', 'analyzed_text': analyzed}
        analyzed

    if (countcharacters == "on"):
        analyzed = ""
        count = len(djtext)

        params = {'purpose': 'CharCounts', 'analyzed_text': count}
        analyzed

    if (spellcheck == "on"):
        analyzed = ""
        blob = TextBlob(djtext)
        a = "" #testword
        b = TextBlob(a)

        params = {'purpose': 'SpellCheck', 'analyzed_text': blob.correct()}
        analyzed

    if (generatesummary == "on"):
        analyzed = ""
        userLink = input("https://en.wikipedia.org/wiki/Starbucks")
        raw_data = urllib.request.urlopen(userLink)
        document = raw_data.read()

        parsed_document = bs.BeautifulSoup(document, 'lxml')

        article_paras = parsed_document.find_all('p')

        scrapped_data = ""

        for para in article_paras:
            scrapped_data += para.text

        print(scrapped_data[:1500])

        scrapped_data = re.sub(r'\[[0-9]*\]', ' ', scrapped_data)
        scrapped_data = re.sub(r'\s+', ' ', scrapped_data)

        formatted_text = re.sub('[^a-zA-Z]', ' ', scrapped_data)
        formatted_text = re.sub(r'\s+', ' ', formatted_text)

        all_sentences = nltk.sent_tokenize(scrapped_data)

        stopwords = nltk.corpus.stopwords.words('english')

        word_freq = {}
        for word in nltk.word_tokenize(formatted_text):
            if word not in stopwords:
                if word not in word_freq.keys():
                    word_freq[word] = 1
                else:
                    word_freq[word] += 1

        max_freq = max(word_freq.values())

        for word in word_freq.keys():
            word_freq[word] = (word_freq[word] / max_freq)

        sentence_scores = {}
        for sentence in all_sentences:
            for token in nltk.word_tokenize(sentence.lower()):
                if token in word_freq.keys():
                    if len(sentence.split(' ')) < 25:
                        if sentence not in sentence_scores.keys():
                            sentence_scores[sentence] = word_freq[token]
                        else:
                            sentence_scores[sentence] += word_freq[token]

        selected_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

        # text_summary = ' '.join(selected_sentences)
        # print(text_summary)

        params = {' '.join(selected_sentences)}
        analyzed

    if(removepunc != "on" and newlineremover!="on" and extraspaceremover!="on" and fullcaps!="on" and lowercase!="on" and countcharacters!="on" and spellcheck!="on" and generatesummary!="on" and removestopwords!="on"):
        return HttpResponse("Try again!")
    else:
        return render(request, 'analyze.html', params)
