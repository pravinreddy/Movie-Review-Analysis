from bs4 import BeautifulSoup
import re
from xlrd import open_workbook
import glob
import csv

with open('doc_table.csv', 'wb') as outcsv:
    writer = csv.DictWriter(outcsv, fieldnames = ["Doc number", "Title","Reviewer","Snippet","Rate"])
    writer.writeheader()

class doctable:
 doctableCount = 0
 def __init__(self,docnumber,title,reviewer,Snippet,rate):
  self.Docnumber = docnumber
  self.Title = title.replace(",","")
  self.Reviewer = reviewer.replace(",","")
  self.Rate = rate
  self.Snippet = ' '.join(Snippet).replace(",","")
  doctable.doctableCount = doctable.doctableCount + 1
  
  
  
###########################################################
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
  
  
###################################################
stop_list = ['','and','a','the','an','by','from','for','hence','of','with','in','within','who','when','where','why','how','whom','have','has','had','not','for','but','do','does','done','as','was']
get_title = re.compile("<TITLE>(.+?)</TITLE>")
doctable_objects = []


###########################################################
inpn = raw_input("Enter the input file for positive negitive terms: ");
book = open_workbook(inpn)
sheet = book.sheet_by_index(0)

coloumn_pos = []
coloumn_nev = []

for row in range(1,11789):
 if(sheet.cell(row,2).value=="Positiv"):
  coloumn_pos.append(str(sheet.cell(row,0).value))
 elif(sheet.cell(row,3).value=="Negativ"):
  coloumn_nev.append(str(sheet.cell(row,0).value))

coloumn_pos = [element.lower() for element in coloumn_pos]
coloumn_nev = [element.lower() for element in coloumn_nev]
#####################################################

for input1 in glob.glob('*.html'):
 with open(input1, "r") as text_title:
  match = re.search(get_title,text_title.read())
  title = match.group(1) if match else "No title"
  title = title.replace("Review for ","")
 text_title.close()

 with open(input1 , "r") as text_file:
  for i, line in enumerate(text_file):
    if i == 5 :
     ln=line
 text_file.close()

 s6 = cleanhtml(ln)
 s7 = "reviewed by "
 reviewer = s6[s6.index(s7) + len(s7):]
 reviewer = reviewer.replace("\n","")


 page = open(input1)
 soup = BeautifulSoup(page,'html.parser')

 l2 = soup.find_all('p')
 r1 = soup.find_all('p')
 r = soup.find_all('pre')
 l1 = "Capsule review:"
 r2 = "-4 to +4"
 
 cflag = 0
 fflag = 0
 r1flag=0
 r2flag=0
 r3flag=0
 r4flag=0
 rat=0
 ratef="NA"
 rate1="NA"
 rate2="NA"
 rate3="NA"
 rate4="NA"

 for i in range(len(r1)):
  t = r1[i].get_text()
  if r2 in t:
   ree=t
   needed = ree[ree.index(r2)-35:ree.index(r2)]
   pos = [" 1"," 2"," 3"," 4","+1","+2","+3","+4"]
   for j in range(len(pos)):
    if pos[j] in needed:
     rate1="P"
     r1flag=1
     break
    elif "-" in needed:
     rate1="N"
     r1flag=1
     break

 for i in range(len(r)):
  t = r[i].get_text()
  if r2 in t:
   ree=t
   needed = ree[ree.index(r2)-25:ree.index(r2)]
   pos = [" 1"," 2"," 3"," 4","+1","+2","+3","+4"]
   for j in range(len(pos)):
    if pos[j] in needed:
     rate1="P"
     r1flag=1
     break
    elif "-" in needed:
     rate1="N"
     r1flag=1
     break

 for i in range(len(l2)-1):
  s = l2[i].get_text()
  if l1 in s:
   cflag = 1
   s = s.replace("\n"," ")
   s=s.replace('-',' ').replace(", "," ").replace('. ',' ').replace("! "," ")
   s=s.replace('"',' ').replace("'","").replace('(',' ').replace(")"," ")
   s=s.replace('[',' ').replace("]"," ").replace('{',' ').replace("}"," ")
   s=s.replace(': ',' ').replace("; "," ").replace("/"," ").replace('? ',' ').replace("*"," ").replace("+"," ")  
   s = re.sub(" +",' ',s)
   cap = s.split(' ')
   capsule= [str(i) for i in cap]

   s2=l2[0].get_text()
   s2=s2.replace("\n"," ")
   s2=s2.replace('-',' ').replace(", "," ").replace('. ',' ').replace("! "," ")
   s2=s2.replace('"',' ').replace("'","").replace('(',' ').replace(")"," ")
   s2=s2.replace('[',' ').replace("]"," ").replace('{',' ').replace("}"," ")
   s2=s2.replace(': ',' ').replace("; "," ").replace("/"," ").replace('? ',' ').replace("*"," ").replace("+"," ")  
   s2=re.sub(" +",' ',s2)
   fir0=s2.split(' ')
   first0 = [str(i) for i in fir0]
   capsule = capsule + first0
   snippet = capsule[:50]

  else:
   fflag = 1
   s3=l2[0].get_text()
   s3=s3.replace("\n"," ")
   s3=s3.replace('-',' ').replace(", "," ").replace('. ',' ').replace("! "," ")
   s3=s3.replace('"',' ').replace("'","").replace('(',' ').replace(")"," ")
   s3=s3.replace('[',' ').replace("]"," ").replace('{',' ').replace("}"," ")
   s3=s3.replace(': ',' ').replace("; "," ").replace("/"," ").replace('? ',' ').replace("*"," ").replace("+"," ")  
   s3=re.sub(" +",' ',s3)
   fir=s3.split(' ')
   first = [str(i) for i in fir]
  
   s4=l2[1].get_text()
   s4=s4.replace("\n"," ")
   s4=s4.replace('-',' ').replace(", "," ").replace('. ',' ').replace("! "," ")
   s4=s4.replace('"',' ').replace("'","").replace('(',' ').replace(")"," ")
   s4=s4.replace('[',' ').replace("]"," ").replace('{',' ').replace("}"," ")
   s4=s4.replace(': ',' ').replace("; "," ").replace("/"," ").replace('? ',' ').replace("*"," ").replace("+"," ")  
   s4=re.sub(" +",' ',s4)
   fir2=s4.split(' ')
   first2 = [str(i) for i in fir2]
   first = first + first2
   snippet = first[:50]

 snippet = [element.lower() for element in snippet]
 if cflag==1:
  for i in range(len(snippet)):
   if snippet[i] in coloumn_pos:
    rat = rat+1
   elif snippet[i] in coloumn_nev:
    rat = rat - 1

 if(rat>0):
  rate2="P"
  r2flag=1
 elif(rat<0):
  rate2="N"
  r2flag=1

 if(r1flag==1):
  ratef = rate1
 elif(r2flag==1):
  ratef = rate2

 doctable_objects.append(doctable(input1,title,reviewer,snippet,ratef))

for i in range(doctable.doctableCount):
 with open("doc_table.csv", "a+") as out_file:
  out_string = ""
  out_string += str(i+1)
  out_string += "," + doctable_objects[i].Title
  out_string += "," + doctable_objects[i].Reviewer
  out_string += "," + doctable_objects[i].Snippet
  out_string += "," + doctable_objects[i].Rate
  out_string += "\n"
  out_file.write(out_string)
 out_file.close()
# print(doctable_objects[i].Docnumber,doctable_objects[i].Title,doctable_objects[i].Reviewer,doctable_objects[i].Snippet,doctable_objects[i].Rate)

