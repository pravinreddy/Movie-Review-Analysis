import os
import re
import csv

doctable2_objects = []
class doctable3:
 doctableCount = 0
 def __init__(self,docnumber,title,reviewer,Snippet,rate):
  self.Docnumber = docnumber
  self.Title = title.replace(",","")
  self.Reviewer = reviewer.replace(",","")
  self.Rate = rate
  self.Snippet = Snippet
  doctable3.doctableCount = doctable3.doctableCount + 1

def rankdoc(listid3):
 ranklist3 = []
 print len(doctable2_objects)
 for i in range(len(listid3)):
  for j in range(len(doctable2_objects)):
   if(listid3[i]==doctable2_objects[j].Docnumber):
    if(doctable2_objects[j].Rate=="P\n"):
     ranklist3.append(listid3[i])

 for i in range(len(listid3)):
  for j in range(len(doctable2_objects)):
   if(listid3[i]==doctable2_objects[j].Docnumber):
    if(doctable2_objects[j].Rate=="N\n"):
     ranklist3.append(listid3[i])

 for i in range(len(listid3)):
  for j in range(len(doctable2_objects)):
   if(listid3[i]==doctable2_objects[j].Docnumber):
    if(doctable2_objects[j].Rate=="NA\n"):
     ranklist3.append(listid3[i])

 return ranklist3

def dretrieve(ilist):
 rlist = []
 for x in range(len(ilist)):
  with open('dictionary.csv') as csvfile:
   csvReader = csv.reader(csvfile)
   for row in csvReader:
    if(ilist[x]==row[0]):
     rlist.append(row[2])
   csvfile.close()
 return rlist

def pretrieve(ilist):
 rlist = []
 for x in range(len(ilist)):
  with open('postinglist.csv') as csvfile:
   csvReader = csv.reader(csvfile)
   for row in csvReader:
    if(ilist[x]==row[0]):
     rlist.append(row[1])
   csvfile.close()
 return rlist

def retrievefile(fil):
 makestr3 = ''
 for j in range(len(doctable2_objects)):
  if(fil==doctable2_objects[j].Docnumber):
   makestr3 = doctable2_objects[j].Docnumber+"," + doctable2_objects[j].Title+","+doctable2_objects[j].Reviewer+","+doctable2_objects[j].Snippet+","+doctable2_objects[j].Rate
   #print str(doctable2_objects[j].Snippet)
 return makestr3


stop_list = ['','and','a','the','an','by','from','for','hence','of','with','in','within','who','when','where','why','how','whom','have','has','had','not','for','but','do','does','done','as','was','',' ']

doc_lines = []
with open("doctable.txt" , "r") as text_file:
 for line in text_file:
  doc_lines.append(line)

for i in range(len(doc_lines)):
 line_list=doc_lines[i].split(",")
 doctable2_objects.append(doctable3(line_list[0],line_list[1],line_list[2],line_list[3],line_list[4]))


for i in range(100):
 file = open("output.txt","a")
 inputquery=raw_input("Enter the query:")
 file.write(inputquery+"\n")
 and_flag = 0
 andnot_flag = 0
 or_flag = 0
 if(inputquery=="EXIT"):
  quit()
 else:
  if "AND" in inputquery:
   and_flag = 1
   print("AND is Present")
  if "NOT" in inputquery:
   andnot_flag = 1
   print("and not is present in the string")
  if "OR" in inputquery:
   or_flag = 1
   print("OR is present")

 if((and_flag==1) and (andnot_flag==1)):
  cut3 = "AND"
  cut4 = "AND NOT "
  #stlen = inputquery.index(cut4) - inputquery.index(cut3)
  #result33 = inputquery[inputquery.index(cut3) + stlen:]
  list93 =inputquery.split(cut4)
  str91 = list93[0]
  str33 = str91[str91.index(cut3) + len(cut3):]
  str34 = list93[1]
  #print("string33"+str33)
  #print("string34"+str34)
  list33 = str33.split(" ")
  list34 = str34.split(" ")
  my_list33 = [element.lower() for element in list33]
  my_list34 = [element.lower() for element in list34]
  new_list33 = [x for x in my_list33 if x not in stop_list]
  new_list34 = [x for x in my_list34 if x not in stop_list]
  result33_set = {}
  result34_set = {}
  for i in range(len(new_list33)):
   docl36 = dretrieve([new_list33[i]])
   docl37 = pretrieve(docl36)
   if(i==0):
    result33_set = set(docl37)
    #print [new_list33[i]]
   else:
    result33_set = set(docl37) & result33_set
  
  for i in range(len(new_list34)):
   docl38 = dretrieve([new_list34[i]])
   docl39 = pretrieve(docl38)
   if(i==0):
    result34_set = set(docl39)
    #print [new_list34[i]]
   else:
    result34_set = set(docl39) & result34_set

  result34_list = list(result33_set - result34_set)
  #print(result34_list)
  final31_result= rankdoc(result34_list)
  #print(final31_result)
  for i in range(len(final31_result)):
   print retrievefile(final31_result[i])
  

 elif(and_flag == 1):
  cut1 = "AND "
  result31 = inputquery[inputquery.index(cut1) + len(cut1):]
  #print("AND result:"+result31)
  list31 = result31.split(" ")
  my_list31 = [element.lower() for element in list31]
  new_list31 = [x for x in my_list31 if x not in stop_list]
  print new_list31
  result32_set ={}
  for i in range(len(new_list31)):
   docl38 = dretrieve([new_list31[i]])
   docl39 = pretrieve(docl38)
   if(i==0):
    result32_set = set(docl39)
    #print [new_list31[i]]
   else:
    result32_set = set(docl39) & result32_set
  result32_list=list(result32_set)
  #print result32_list
  final32_result = rankdoc(result32_list)
  #print final32_result
  for i in range(len(final32_result)):
   print retrievefile(final32_result[i])
  
 elif(or_flag == 1):
  cut2 = "OR"
  result32 = inputquery[inputquery.index(cut2) + len(cut2):]
  #print("OR result:"+result32)
  list32 = result32.split(" ")
  my_list32 = [element.lower() for element in list32]
  new_list32 = [x for x in my_list32 if x not in stop_list]
  #print new_list32
  docl33 = dretrieve(new_list32)
  docl34 = pretrieve(docl33)
  aset34 = set(docl34)
  list99 = list(aset34)
  #print list99
  final33_result = rankdoc(list99)
  #print final33_result
  for i in range(len(final33_result)):
   file.write(retrievefile(final33_result[i]))
   print retrievefile(final33_result[i])