from sklearn.datasets import fetch_20newsgroups
from xml.sax.saxutils import escape

def valid_xml_char_ordinal(c):
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )


#categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
#categories = ['soc.religion.christian', 'comp.graphics', 'sci.med', 'rec.autos', 'rec.sport.hockey']
categories = ['alt.atheism', 'comp.graphics', 'rec.autos', 'rec.sport.hockey']
twenty_train = fetch_20newsgroups(subset='train', random_state=None, categories=categories, shuffle=True, remove=('headers', 'footers', 'quotes'))
#	
ncat = range(len(categories))
ntargets = 20
counts = [0 for x in ncat]
complete = [False for x in ncat]
goal = [ntargets for x in ncat]

i=0
idfile=1
while counts != goal:
  if counts[twenty_train.target[i]] < ntargets: 

    result ='<doc target="'+categories[twenty_train.target[i]]+'">\n'
    
    cleaned_string = ''.join(c for c in twenty_train.data[i] if valid_xml_char_ordinal(c))
    result+=escape(cleaned_string)

    result+='\n</doc>\n'
    counts[twenty_train.target[i]]+=1

    text_file = open("../data/20newsgroups/"+str(idfile)+".xml", "w")
    text_file.write(result)
    text_file.close()
    idfile+=1
  
  i+=1


