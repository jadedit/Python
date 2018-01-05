#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import requests
from bs4 import BeautifulSoup
import re
from langdetect import detect_langs,detect,DetectorFactory
from collections import Counter
#from impala.dbapi import connect
import codecs
import string
from operator import add
import operator
import sys
import json
from LexTo import LexTo
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

config = ConfigParser.ConfigParser()
#config.read("/home/serveradm/WebResolver/config_site.ini")
config.read("config_site.ini")
proxy = config.get("network","proxy")
#api_key = config.get("thaisegmentapi","api_key")
stopwordList = config.get("cleansing","stopword")
stopwordTHList = config.get("cleansing","stopword_th")
filtering = config.get("cleansing","filtering").split(",")
#spark = config.get("spark-setting","spark")
#spark = True
spark = False
#host = config.get("database","host")
#port = config.get("database","port")
root_path = config.get("folder_path","root_path")
log_path = config.get("folder_path","log_path")
dictionary_filename = config.get("folder_path","dictionary_filename")
input_filename = config.get("folder_path","input_filename")
output_filename = config.get("folder_path","output_filename")
#rootUrl = config.get("thaisegmentapi","rootUrl")
DetectorFactory.seed = config.get("langdetect","seed")
dictionary = dict()
lexto = LexTo()

if spark:
	import pyspark
	from pyspark import SparkContext, SparkConf

def getStrTime():
	return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def getLogTime():
	return datetime.datetime.now().strftime("%Y%m%d %H%M%S : ")

"""
def connectDatabase():
	global host,port
	conn = connect(host=host, port=port)
	return conn.cursor()
"""

def createDictionary():
	global dictionary_filename,dictionary
	f = codecs.open(root_path + dictionary_filename,'r',encoding='utf8').read().split("\n")
	for row in f:
		try:
			word = row.split(" ")[0].strip().lower()
			cat = row.split(" ",1)[1]
			dictionary[word] = cat
		except:
			pass

def webCrawler(s):
	global proxy
	try:
		if proxy != '':
			proxies = {'http':proxy, 'https':proxy}
			headers = {'x-redirect-url':s}
			try:
				req = requests.request('get',proxy,proxies=proxies,headers=headers, timeout=10)
			except:
				s=s.replace('http:', 'https:')
				headers = {'x-redirect-url':s}
				req = requests.request('get',proxy,proxies=proxies,headers=headers, timeout=10)
		else:
			req = requests.get(s, timeout=10)
		
		req.headers['content-type']
		req.encoding='utf-8'

		if req.status_code == 200:
			return req.text, s
		else:
			return '', s
	except requests.exceptions.ReadTimeout:
		return '', s

def htmlRemoval(s):
	textNoScript = re.subn(r'<(script).*?</\1>(?s)', '', s)
	textNoCSS = re.subn(r'<(style).*?</\1>(?s)', '', textNoScript[0])
	soup = BeautifulSoup(textNoCSS[0],"html.parser")
	texturl = soup.get_text()
	textNoHTMLTag = re.sub('<[^>]*>', '', texturl)
	return textNoHTMLTag

def punctuationRemoval(s):
	word = s.replace(":"," ")
	word = word.replace("/"," ")
	word = word.replace("."," ")
	word = word.replace(","," ")
	word = word.replace("!"," ")
	word = word.replace("@"," ")
	word = word.replace("#"," ")
	word = word.replace("$"," ")
	word = word.replace("%"," ")
	word = word.replace("^"," ")
	word = word.replace("&"," ")
	word = word.replace("*"," ")
	word = word.replace("("," ")
	word = word.replace(")"," ")
	word = word.replace("-"," ")
	word = word.replace("_"," ")
	word = word.replace("+"," ")
	word = word.replace("="," ")
	word = word.replace("["," ")
	word = word.replace("]"," ")
	word = word.replace("{"," ")
	word = word.replace("}"," ")
	word = word.replace(";"," ")
	word = word.replace("'"," ")
	word = word.replace('"'," ")
	word = word.replace("<"," ")
	word = word.replace(">"," ")
	word = word.replace("?"," ")
	word = word.replace("\\"," ")
	word = word.replace("|"," ")
	word = word.replace("`"," ")
	word = word.replace("~"," ")
	word = word.replace("\t"," ")
	word = word.replace("\n"," ")
	word = re.sub(' +', ' ', word)
	return word

def detectLang(s):
	try:
		if 'th' in str(detect_langs(s)):
			return 'th'
		else:
			return 'en'
	except:
		return 'en'

def thaiWordTokenizer(s):
	tmp = ' '.join(lexto.tokenize(s))
	return tmp

def stopWordRemoval(s):
	global stopwordList,stopwordTHList
	return ' '.join([word for word in s.split(' ') if word not in stopwordList])

def wordCounting(s):
	if spark:
		return s
	else:
		return Counter(s.split(" "))

def search_word(s):
	try:
		return dictionary[s]
	except:
		return ''

def dictionary_matching(s):
	global spark
	if spark:
		print 'Spark'
		sc = SparkContext("local","website_cateogorization")
		webRDD = sc.parallelize(s.split(" "), "4")
		category =  webRDD.map(lambda word: (word,1))\
			.reduceByKey(add)\
			.map(lambda (word,freq): (search_word(word),freq))\
			.flatMap(lambda (w,f): [(wo,f) for wo in w.split(",")])\
			.reduceByKey(add)\
			.sortBy(lambda a:-1 * a[1])\
			.collect()
		cat_idx = 0
		try:
			cat = category[cat_idx][0]
			if cat == '':
				cat_idx = 1
				cat = category[cat_idx][0]
		except:
			cat = 'None-Cat-s'
		write_file(root_path + getStrTime() + "dam2.txt", str(cat), "a+")
	else:
		print 'No Spark'
		tmp = dict()
		for w,f in s.iteritems():
			print type(w)
			
			try:
				print "w :", w.encode('cp874')
			except:
				print "w2 :", w
			
			print "f :", f
			tmp_cat = search_word(w)
			print "Search :", tmp_cat

			if tmp_cat != '':
				for cat in tmp_cat.split(","):
					if tmp.has_key(cat):
						tmp_freq = tmp[cat]
						tmp_freq = tmp_freq + f
						tmp[cat] = tmp_freq
					else:
						tmp[cat] = f
		if len(tmp) > 0:
			cat = sorted(tmp.items(), key=operator.itemgetter(1), reverse=True)[0]
		else:
			cat = 'None-Cat'
	print "tmp :", tmp
	print "Cat :", str(cat)

	if 'travel' in cat:
		return 'travel'
	elif 'food' in cat:
		return 'food'
	elif 'entertain' in cat:
		return 'entertain'
	else:
		return str(cat)

def write_file(path,txt,type_):
	f = codecs.open(path, type_, encoding='utf8')
	f.write(txt)

def url_filtering(s):
	global filtering
	for w in filtering:
		if w in s:
			return False
	return True

def map_category():
	mapped_tmp = dict()
	f = open(root_path +"mapping_cat.csv",'r').read().split("\n")
	for row in f:
        	try :
                	a,b = row.split(",")
                	mapped_tmp[a] = b
        	except:
                	pass
	print "Aft: ", mapped_tmp

	return mapped_tmp

createDictionary()
#mapped = map_category()
#mapped = dict()
input_ = open(root_path + input_filename).read().split("\n")

strTime = getStrTime()
log_filepath = log_path + strTime

output_ = log_filepath + "_" + output_filename
punctuation_ = log_filepath + "_punctuation.log"
stopword_ = log_filepath + "_stopword.log"
wordcount_ = log_filepath + "_wordcount.log"
logscreen_ = log_filepath + "_screen.log"


for url in input_:
	url = url.strip(' ')
	print "URL ", url
	write_file(logscreen_, "---------------------------------------------------" + "\n", "a+")
	write_file(logscreen_, getLogTime() + "URL : " + url + "\n", "a+")

	if url_filtering(url) and url != '':
		if "http" not in url:
			url = "http://" + url

		text,url = webCrawler(url)

		if text != '':
			text = htmlRemoval(text)
			text = punctuationRemoval(text).lower()
			print "punctuation"
			write_file(logscreen_, getLogTime() + "Step: punctuation" + "\n", "a+")
			print type(text)
			write_file(punctuation_, getLogTime() + str(type(text)) + "\n", "a+")
			write_file(punctuation_, getLogTime() + "\n", "a+")
			write_file(punctuation_, text + "\n", "a+")


			if 'th' == detectLang(text):
				print "word: th"
				write_file(logscreen_, getLogTime() + "word: th" + "\n", "a+")	
				text = thaiWordTokenizer(text)
			else:
				print "word: en"
				write_file(logscreen_, getLogTime() + "word: en" + "\n", "a+")

			text = stopWordRemoval(text)
			print "stopWordRemoval"
			write_file(logscreen_, getLogTime() + "Step: stopWordRemoval" + "\n", "a+")
			print type(text)
			write_file(stopword_, getLogTime() + str(type(text)) + "\n", "a+")
			write_file(stopword_, getLogTime() + "\n", "a+")
			write_file(stopword_, text + "\n", "a+")

			wc = wordCounting(text)
			print "word Count"
			write_file(logscreen_, getLogTime() + "Step: word Count" + "\n", "a+")
			print type(wc)
			write_file(wordcount_, getLogTime() + str(type(wc)) + "\n", "a+")
			write_file(wordcount_, getLogTime() + "\n", "a+")
			write_file(wordcount_, str(wc) + "\n", "a+")

			output = dictionary_matching(wc)

			print "Output: ", output
			write_file(logscreen_, getLogTime() + "Output: " + output + "\n", "a+")

			if output not in ('None-Cat', 'food', 'travel', 'entertain', 'None-Cat-s'):
				#output = mapped[output.split(",")[0][3:-1]]
				output = output.split(",")[0][3:-1]
			write_file(output_, getLogTime() + url + " " + output + "\n", "a+")

			print url,output
			write_file(logscreen_, getLogTime() +  url + output + "\n", "a+")	
		else:
			print url,"No Content"
			write_file(logscreen_, getLogTime() +  url + "No Content" + "\n", "a+")
	else:
		pass
