import MySQLdb
#import xml.etree.ElementTree as ET
import sys
#from xml.dom.minidom import parseString
from random import random
from lxml.etree import CDATA
from lxml.builder import E
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf8')


def valid_xml_char_ordinal(c):
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )


info_tut_vec = [0 for x in range(57)]
info_sub_vec = [0 for x in range(7)]
try:

  # Database connection and query
  db = MySQLdb.connect(host="localhost", user="root", passwd="secret",  db="gradeslam")
  print "[INFO] Connection successful"
  cur = db.cursor()
  cur.execute("SELECT ts.id, ts.subject_id, ts.topic_id FROM tutor_sessions ts;")
  tut_sessions = {}
  for row in cur.fetchall():
    tut_session = {"subject":row[1],"topic":row[2]}
    tut_sessions[row[0]] = tut_session
    if row[1] != None: info_sub_vec[row[1]] += 1
    if row[2] != None: info_tut_vec[row[2]] += 1

  cur.execute("SELECT * FROM user_tutors;")
  tut_ids = []
  for row in cur.fetchall():
    tut_ids.append(row[1])

  cur.execute("SELECT m.id, m.session_id, m.message, m.user_id FROM messages m order by m.session_id, m.id;")
  print "[INFO] Query performed"

  # create xml element and set variables
  root = etree.Element("document")
  nid=1
  cid=-1
  tutor_id = "-1"
  student_id = "-1"
  #categories = ["Cat1","Cat2","Cat3"]


  # iterate over the data and create the xml structure
  text="\n"
  ndocs=0
  for row in cur.fetchall():

    if tut_sessions[row[1]]["subject"] == None or tut_sessions[row[1]]["topic"] == None: continue


#    if tut_sessions[row[1]]["topic"] != None and info_tut_vec[tut_sessions[row[1]]["topic"]] < 20: continue
#    if tut_sessions[row[1]]["subject"] != None and info_tut_vec[tut_sessions[row[1]]["subject"]] < 20: continue

    if cid != row[1]:

      if cid!=-1 and len(text) > 1000:
        convEL = etree.SubElement(root, "conversation",id=str(cid),topic=str(tut_sessions[cid]["topic"]),subject=str(tut_sessions[cid]["subject"]),tutor_id=tutor_id,student_id=student_id)
        convEL.text = text
        ndocs+=1

      text = "\n"
      tutor_id = "-1"
      student_id = "-1"
      cid = row[1]

    user_id = row[3]
    if row[3] in tut_ids:
      tutor_id = str(row[3])
    else:
      student_id = str(row[3])

    #docEL = etree.SubElement(convEL,'utterance',id=str(row[0]),dialog_act="UNK",user_id=str(user_id),user_type=user_type)
    #docEL = ET.SubElement(convEL,'utterance',id=str(row[0]),dialog_act="UNK",user_id=str(user_id),user_type=user_type)
    #docEL.text = unicode(row[2], errors='replace')
    cleaned_string = ''.join(c for c in unicode(row[2], errors='replace') if valid_xml_char_ordinal(c))
    #docEL.text = etree.CDATA( cleaned_string )
   # docEL.text = cleaned_string
    text+=cleaned_string+"\n"
    nid+=1
    if nid%10000 == 0: print "[INFO] ",nid," rows processed."


  db.close()
  #print info_tut_vec
  print "[INFO]",ndocs,"documents written"
  # save xml to file
  text_file = open("data.xml", "w")
  text_file.write(etree.tostring(root, pretty_print=True))
  #text_file.write( parseString(ET.tostring(root)).toprettyxml(indent=" ") )
  #text_file.write(ET.tostring(root))
  text_file.close()

#except:
#  print "Unexpected error:", sys.exc_info()[0]


finally:
  print "Execution finished."
