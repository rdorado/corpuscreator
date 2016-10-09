import pickle
import xml.etree.ElementTree as ET
import random
from lxml import etree

tree = ET.parse('../data.xml')
root = tree.getroot()
data = []
selected = []
ids = []
conversations = []
id_map = {}

subjects = {1:"Math",2:"Science",3:"English",4:"Social Science",5:"Languages",6:"Other"}
topics = {1:"Arithmetic", 2:"Geometry", 3:"Calculus 1", 4:"Calculus 2", 5:"Calculus 3", 6:"Discrete Math", 7:"Pure Mathematics", 8:"Applied Mathematics", 9:"Statistics", 10:"Probability", 11:"Trigonometry", 12:"Algebra", 13:"Pre-Calculus", 14:"AP Calculus", 15:"Sets", 16:"Biology", 17:"Physics", 18:"Chemistry", 19:"Ecology", 20:"Geology", 21:"Biochemistry", 22:"Neurobiology", 23:"Cell Biology", 24:"Organic Chemistry", 25:"Inorganic Chemistry", 26:"Stoichiometry", 27:"Physical Sciences", 28:"English as a Second Language", 29:"Essay Writing", 30:"English Literature", 31:"Canadian History", 32:"American History", 33:"World History", 34:"Religion", 35:"Humanities", 36:"Art History", 37:"Sociology", 38:"Psychology", 39:"Theology", 40:"Anthropology", 41:"History", 42:"French", 43:"Spanish", 44:"German", 45:"Mandarin", 46:"Hebrew", 47:"Arabic", 48:"Romanian", 49:"Italian", 50:"Music Theory", 51:"Computer Science", 52:"Microeconomics", 53:"Macroeconomics", 54:"Marketing", 55:"Accounting"}

indx=0
print "[INFO] Loading data from XML"
for conversation in root:
  conversations.append( conversation )
  #ids.append( conversation.attrib["id"] )
  #id_map[conversation.attrib["id"]]=indx
  #indx+=1

#print ids[:10]
#random.shuffle( ids )
#print ids[:10]

#infofile = '"Subject id","Subject","Topic id","Topic","Session id","Tutor id","Manual verification","Topic in tutor exp", "Comments"\n'
#root = ET.Element("document")
for node in conversations:
#  node = conversations[ id_map[ ids[i] ] ]
  #root.append( node )

  node.attrib["subject"] = subjects[int(node.attrib["subject"])]
  node.attrib["topic"] = topics[int(node.attrib["topic"])]

  text_file = open("../../data/raw/"+node.attrib["id"]+".xml", "w")
  text_file.write(etree.tostring( etree.fromstring(ET.tostring(node)), pretty_print=True))
  text_file.close()

  #idsub = int(node.attrib["subject"])
  #idtop = int(node.attrib["topic"])
  #idtut = int(node.attrib["tutor_id"])
  #infofile = infofile+str(idsub)+',"'+subjects[idsub]+'",'+str(idtop)+',"'+topics[idtop]+'",'+str(ids[i] )+','+str(idtut)+',"","",""\n'
#  if conversation.attrib["topic"] in ["None"]: continue
#  targets.append(conversation.attrib["topic"])
#  text=""
#  for utterance in conversation:
#    if utterance.text != None: text=text+" "+utterance.text
#  data.append(text)
# print "[INFO] Data loaded"

#text_file = open("info.csv", "w")
#text_file.write(infofile)
#text_file.close()