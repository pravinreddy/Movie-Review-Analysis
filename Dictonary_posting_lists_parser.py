import os
from collections import Counter
import re
import csv
import glob

with open('dictionary.csv', 'wb') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = ["Term", "Doc_Frequency", "Offset"])
    writer.writeheader()

with open('postinglist.csv', 'wb') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = ["Offset","DocId", "Term_Frequency"])
    writer.writeheader()

class dictcsv:
 dictcsvCount = 0
 def __init__(self,term,docFrequency,offset):
  self.term = term
  self.docFrequency = docFrequency
  self.offset = offset
  dictcsv.dictcsvCount = dictcsv.dictcsvCount + 1


class postinglistcsv:
 postinglistCount = 0
 def __init__(self,off , docPid, termFrequency):
  self.off = off
  self.docPid = docPid
  self.termFrequency = termFrequency
  postinglistcsv.postinglistCount = postinglistcsv.postinglistCount + 1

  
class dictonary:
 dictCount = 0
 def __init__(self,docName,docId,dictList,mapList):
  self.docName = docName
  self.docId = docId
  self.dictList = dictList
  self.mapList = mapList
  dictonary.dictCount = dictonary.dictCount + 1

 def display(self):
  print("doc name",self.docName)
  print("docid",self.docId)
  print("term frequency",self.mapList["review"])

 def checkElement(self, element): #document word check
  b = element in self.dictList
  if (b == True):
   return 1
  else:
   return 0

 def countElement(self, element): #term frequency counting
  try:
   d = self.mapList[element]
  except Exception:
   d = 0
  return d

 def getdocId(self): #to get the document id
  return self.docId

 def getdictList(self): #to get the elements in the particular document
  return self.dictList

 def getdocName(self): # to get the document name
  return self.docName

 def getmapList(self): # to get the dictonary map
  return self.mapList

#clean all the html code
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

#get the list of words in the document
def getWords(file):
 stop_list = ['','and','a','the','an','by','from','for','hence','of','with','in','within','who','when','where','why','how','whom','have','has','had','not','for','but','do','does','done','as','was']
 with open(file , "r") as text_file:
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
 text_file.close()
 return final_list
 
def sortList(initList):
 aset = set(initList)
 asetList = list(aset)
 asetList.sort()
 return asetList

def mapping(initList):
 #counter for counting the items in the list
 fin = Counter(initList)
 fin.keys()
 #maping the variables to hash map
 dict_map = {}
 for key,value in fin.items():
  dict_map[key] = value
 return dict_map
 
j = 1;          # to count the document number

dict_objects = []

for filename in glob.glob('*.html'):
 with open(filename , "r") as text_file:
  doc_id = j
  doc_name = filename
  wordlist = getWords(filename)
  dict_list = sortList(wordlist)
  map_list = mapping(wordlist)
  dict_objects.append(dictonary(filename, doc_id, dict_list , map_list))
 j=j+1

total_list = []
for l in range(dictonary.dictCount):
 total_list = total_list + dict_objects[l].getdictList()

final_map_list = mapping(total_list)
final_sorted_list = sortList(total_list)

dictcsv_objects = []
postingcsv_objects = []

for i in range(len(final_sorted_list) - 1):
 Term = final_sorted_list[i]
 Offset = i
 try:
  docfreq = final_map_list[Term]
 except Exception:
  docfreq = 0
 dictcsv_objects.append(dictcsv(Term, docfreq, Offset))
 for j in range(dictonary.dictCount):
  p =  dict_objects[j].checkElement(Term)
  if(p==1):
   tfeq = dict_objects[j].countElement(Term)
   Id = dict_objects[j].docId
   postingcsv_objects.append(postinglistcsv(Offset,Id,tfeq))
   
for i in range(postinglistcsv.postinglistCount):
 with open("postinglist.csv", "a+") as out_file:
  out_string = ""
  out_string += str(postingcsv_objects[i].off)
  out_string += "," + str(postingcsv_objects[i].docPid)
  out_string += "," + str(postingcsv_objects[i].termFrequency)
  out_string += "\n"
  out_file.write(out_string)
 out_file.close()
# print(postingcsv_objects[i].off,postingcsv_objects[i].docPid,postingcsv_objects[i].termFrequency)

for i in range(dictcsv.dictcsvCount):
 with open("dictionary.csv", "a+") as out_file:
  out_string = ""
  out_string += str(dictcsv_objects[i].term)
  out_string += "," + str(dictcsv_objects[i].docFrequency)
  out_string += "," + str(dictcsv_objects[i].offset)
  out_string += "\n"
  out_file.write(out_string)
 out_file.close()
 #print(dictcsv_objects[i].term,dictcsv_objects[i].docFrequency,dictcsv_objects[i].offset)


