#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

Author: Ruben Dorado
Last modified: October 2016
"""
import xml.etree.ElementTree as ET
import glob

class Document(object):

    def __init__(self, tag="", text="", attribs={}):
        self.rootTag = tag
        self.text=text
        self.attribs = attribs

class Corpus(object):

  docs = []
  attributes = []
  values = {}
  ndocs=0

  def __init__(self, dirname):
      self.readFromFile(dirname)


  def getAttributeVal(self, docindx, attname):
      attindx = self.attributes.index(attname)
      return self.docs[docindx].attribs[attindx]

  def readFromFile(self, dirname):
      self.ndocs=0
      for doc in glob.glob(dirname+"/*.xml"):
        try: 
          tree = ET.parse(doc)
          root = tree.getroot()
          attribs = {}
          for key, value in root.attrib.iteritems():
            if not key in self.attributes:
                self.attributes.append(key)
            idkey = self.attributes.index(key)
            attribs[idkey] = value

          doc = Document(root.tag, root.text, attribs)
          self.docs.append(doc)
          self.ndocs+=1
        except:
	  print "Error reading file '"+doc+"'"  
