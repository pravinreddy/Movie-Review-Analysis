import os
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ' ', raw_html)
  cleantext = cleantext.replace('"',' ').replace("'","")
  cleantext = cleantext.replace('(',' ').replace(")"," ")
  cleantext = cleantext.replace('[',' ').replace("]"," ")
  cleantext = cleantext.replace('{',' ').replace("}"," ")
  cleantext = cleantext.replace('-',' ').replace(", "," ")
  cleantext = cleantext.replace('. ',' ').replace("! "," ")
  cleantext = cleantext.replace(': ',' ').replace("; "," ").replace("/"," ")
  cleantext = cleantext.replace('? ',' ').replace("*"," ").replace("+"," ")  
  cleantext = re.sub(' +',' ',cleantext)
  return cleantext


stop_list = ['','and','a','the','an','by','from','for','hence','of','with','in','within','who','when','where','why','how','whom','have','has','had','not','for','but','do','does','done','as','was']
input1 = raw_input("Enter the input file name to index: ");
with open(input1 , "r") as text_file:
	str = text_file.read().replace('\n', ' ')
	lines = cleanhtml(str)
	my_list = lines.split(' ')	
	my_list = [element.lower() for element in my_list]

new_list = [x for x in my_list if x not in stop_list]                       #removing the stopwords from the list
word_list = [i for i in new_list if len(i) > 1 ]                            #removing the single characters in the list

for i in range(len(word_list)) :
 if word_list[i].endswith('ies') and not word_list[i].endswith('eies') and not word_list[i].endswith('aies'):
        new_word=word_list[i][:-3]+'y'
        word_list[i] = new_word
 if word_list[i].endswith('es') and not word_list[i].endswith('aes') and not word_list[i].endswith('ees') and not word_list[i].endswith('oes'):
        new_word=word_list[i][:-2]+'e'
        word_list[i] = new_word
 if word_list[i].endswith('s') and not word_list[i].endswith('ss') and not word_list[i].endswith('us'):
        new_word=word_list[i][:-1]
        word_list[i] = new_word

word_list.sort()

final_list = [i for i in word_list if len(i) > 1 ]                             #removing the single characters in the list

for word in final_list:
 print word
text_file.close()

