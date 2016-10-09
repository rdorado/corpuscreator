import nltk
import re
from nltk.corpus import stopwords
import math

class BOW(object):
    vocab = {}
    nvocab=0
    binary=False

    def __init__(self, binary=False):
        self.vocab = {}
        self.binary=binary

    def add(self, word):
        try:
            if self.binary:
                self.vocab[word]=1
            else:
                self.vocab[word]+=1
        except KeyError:
            self.vocab[word]=1

    def getVocab(self):
        return self.vocab.keys()

    def getCount(self, word):
        try:
            return self.vocab[word]
        except KeyError:
            return 0

    def merge(self, bow):
        if self.binary:
            for word, value in bow.vocab.items():
                self.vocab[word]=value
        else:
            for word, value in bow.vocab.items():
                try:
                    self.vocab[word]+=value
                except KeyError:
                    self.vocab[word]=value

    def sum(self, bow):
        self.binary=False
        for word, value in bow.vocab.items():
            try:
                self.vocab[word]+=value
            except KeyError:
                self.vocab[word]=value

    def max(self, bow):
        self.binary=False
        for word, value in bow.vocab.items():

            try:
                self.vocab[word] = max(value, self.vocab[word])
            except KeyError:
                self.vocab[word]=value



    def printDict(self):
        for word, value in self.vocab.items():
            print word+"="+str(value)

class TextProcessor(object):

    tolower=True
    removePunctuation=True
    removeStopWords=True
    removeNumbers=True
    punctuation="!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    result=""
    ndocs=0

    additionalStopwords = ['hi','back','wait','hello','ok','great','yes']
    #totalTermFrequency = BOW()
    #maximumFrecuencies = BOW()

    def __init__(self):
        self.punctRegex = re.compile('[%s]' % re.escape(self.punctuation))
        self.stopwords = stopwords.words('english')+self.additionalStopwords

    def calculateTotalTermFrequency(self, corpus):
        self.totalTermFrequency = BOW(binary=True)
        self.maximumFrecuencies = BOW()
        for doc in corpus.docs:
            self.ndocs+=1
            tmp = BOW(binary=True)
            tmp2 = BOW()
            for word in self.process(doc.text, resultAs="vector"):
                tmp.add(word)
                tmp2.add(word)
            self.totalTermFrequency.sum(tmp)
            self.maximumFrecuencies.max(tmp2)

    def calculateConditionalFrequency(self, corpus, attribute, binary=False):
        self.allwords = BOW()
        self.frequencies = {}
	self.catcount = {}

        if attribute not in corpus.attributes: return

        indx = corpus.attributes.index(attribute)

        for doc in corpus.docs:
            self.ndocs+=1
            cat = doc.attribs[indx]
	    

            if not cat in self.frequencies:
                self.frequencies[cat] = BOW()

            tmp = BOW(binary)
            for word in self.process(doc, indx, resultAs="vector"):
                tmp.add(word)
		try:
	           self.catcount[cat]+=1 	
		except KeyError:
		   self.catcount[cat]=1

            self.allwords.sum(tmp)
            self.frequencies[cat].sum(tmp)
            #    tmp.add(word)
            #    tmp2.add(word)
            #self.totalTermFrequency.sum(tmp)
            #self.maximumFrecuencies.max(tmp2)

    def process(self, doc, indxCat, resultAs="term-class", ):
        text=doc.text

        if self.tolower:
            text=text.lower()

        if self.removePunctuation:
            text=self.punctRegex.sub(' ', text)

        if self.removeNumbers:
            text= " ".join(re.findall("[a-zA-Z]+", text))

        tokens = nltk.word_tokenize(text)

        if self.removeStopWords:
            tokens = [word for word in tokens if word not in self.stopwords]

        result = ""
        if resultAs=="counts":
            counter = BOW()
            for word in tokens:
                counter.add(word)
            for word in counter.getVocab():
                result+=word+"="+str( counter.getCount(word) )+"\n"
        elif resultAs=="td-idf_analysis":
            counter = BOW()
            for word in tokens:
                counter.add(word)
            for word in counter.getVocab():
                idf_count = self.totalTermFrequency.getCount(word)
                idf = math.log(self.ndocs/float(idf_count))
                tf = 0.5 + 0.5*(float(counter.getCount(word))/self.maximumFrecuencies.getCount(word))
                #result+=word+"= idf:"+str(idf_count)+","+str(idf)+" || "+str( counter.getCount(word) )+" tf:"+str(tf)+"\n"
                tfidf = idf*tf
                if tfidf > 2:
                    result += word + "=" + str(tfidf) + "\n"
        elif resultAs=="term-class":
	    tmpwords = []
	    res=[]
            for word in tokens:
		if word in tmpwords: continue
		tmpwords.append(word)
		    
                #result+=word+"="
                total=0
                probs = {}

                for key, bow in self.frequencies.iteritems():
                    count = bow.getCount(word)
                    probs[key] = float(count)
                    #result+=key+":"+str(count)+","
                    total+=count

                maxid = -1
                maxval = 0
                for key, bow in probs.iteritems():
                    probs[key] = probs[key]/self.catcount[key]
                    if maxval < probs[key]:
                        maxval = probs[key]
                        maxid = key
		
		res.append( (probs[maxid], word, maxid) )
		
                #if maxid ==  indxCat:
                #result += word+"="+str(probs[maxid])+" "+maxid+"\n"




                #self.allwords.sum(tmp)
                #self.frequencies[cat].sum(tmp)
	    res = sorted(res, reverse=True, key=lambda x:x[0])
	    for word in res:
               result+=str(word)+"\n" 
            return result
        elif resultAs=="vector":
            return tokens
        elif resultAs=="text":
            for word in tokens:
                result+=word+" "
        return result



