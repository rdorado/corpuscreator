import re
import random
import sys
import time

subject = ["math", "science", "english", "social science", "languages", "other",]

topic_keywords = ["math", "science", "english", "social", "language", "arithmetic", "geometry", "calculus", "discrete","math", "pure","mathematics", "applied ", "mathematics", "statistics", "probability", "trigonometry", "algebra", "pre-calculus", "sets", "biology", "physics", "chemistry", "ecology", "geology", "biochemistry", "neurobiology", "cell biology", "organic chemistry", "inorganic chemistry", "stoichiometry", "physical","sciences", "english", "essay","writing", "literature", "canadian history", "american history", "world history", "religion", "humanities", "art history", "sociology", "psychology", "theology", "anthropology", "history", "french", "spanish", "german", "mandarin", "hebrew", "arabic", "romanian", "italian", "music","theory", "computer","science", "microeconomics", "macroeconomics", "marketing", "accounting",]

topic_subject_map = {0: {0:0.6, 1:0.4}, 1: {0:0.2, 1:0.8}, 2:{2:0.6,4:0.4}}

class GradeSlamChat(object):


    def __init__(self):
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("Gradeslam chatbot v.0.0.1\n---------")
        print("GradeSlam offers academic tutoring on topics such as calculus, essay writing, biology, chemistry, physics, etc.")
        print("Interact with our chatbot Slamy by typing in plain English, using normal upper-")
        print('and lower-case letters and punctuation. He will help you to find the topic and connect you')
        print('with the right tutor. ')
        print('Enter "quit" when done.')
        print('=' * 72)

        time.sleep(1)
        print("Slamy >  hi Saad! This is Slamy and I'm here to connect you with the right tutor.")
        time.sleep(1.5)
        print("Slamy >  What topic do you need help in?")

        self.chatState = findTopicState()

    #    self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]


    def respond(self, str):
        """
        Generate a response to the user input.

        :type str: str
        :param str: The string to be mapped
        :rtype: str
        """

        newState = self.chatState.respond(str)


        self.chatState = newState

        '''# check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp
        '''


    def converse(self, quit="quit"):
        input = ""
        while input != quit:
            input = quit
            try:
                input = raw_input("You > ")
            except EOFError:
                print(input)
            if input:
                while input[-1] in "!.": input = input[:-1]
                self.respond(input)


class chatState():

    keywords = []
    topic = []
    subject = []
    picture = []
    firstTime = True

    reflections = {
        "i am": "you are",
        "i was": "you were",
        "i": "you",
        "i'm": "you are",
        "i'd": "you would",
        "i've": "you have",
        "i'll": "you will",
        "my": "your",
        "you are": "I am",
        "you were": "I was",
        "you've": "I have",
        "you'll": "I will",
        "your": "my",
        "yours": "mine",
        "you": "me",
        "me": "you"
    }

    def __init__(self):
        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in self.pairs]
        self._regex = self._compile_reflections()

    def _substitute(self, str):
        return self._regex.sub(lambda mo:
                self.reflections[mo.string[mo.start():mo.end()]],
                    str.lower())

    def _compile_reflections(self):
        sorted_refl = sorted(self.reflections.keys(), key=len, reverse=True)
        return  re.compile(r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE)

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos + 1:pos + 2])
            response = response[:pos] + \
                       self._substitute(match.group(num)) + \
                       response[pos + 2:]
            pos = response.find('%')
        return response

class findTopicState(chatState):

    pairs = (
    (r'hi(.*)',
     ("Hi again! Can you tell me the topic of your question?",
      "Hi again! Can you tell me the topic of your question?")),

    (r'I need help with (.*)',
     ("OK. Can you be more specific about the topics of %1?",
      "I don't understand %1?. What topic is that?")),

    (r'(.*)',
     ("Please tell me more about the topic.",
      "Can you elaborate on that?",
      "What topic is that?"))
    );


    def respond(self, str):

        for word in str.lower().split(" "):
           if word in topic_keywords and word not in self.keywords:
               self.keywords.append(word)
               #subjects = topic_subject_map[topic_keywords.index(word)]

               time.sleep(1)
               print "Slamy > Let me see if there are tutors available"
               time.sleep(3)
               print "Slamy > Ok Saad"

               time.sleep(2)
               rndm = random.choice([1, 2])
               if rndm == 1:
                  print "Slamy > I'll transfer you over to Assaf who can assist you in "+word
                  time.sleep(2)
                  print "Slamy > Have a god one!"
                  time.sleep(2)
                  sys.exit(0)
               else:
                   print "Slamy > There are not tutors online that can help you with "+word
                   print "Slamy > Omar is an excellent "+word+" tutor and he will be on tonight at 10pm! Would you like to chat with another tutor right now? "
                   return ynConfirmOtherTutorAppointment()


        for (pattern, response) in self._pairs:
            match = pattern.match(str)
            if match:
                resp = random.choice(response)    # pick a random response
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                print resp
                return self

        return self


class ynConfirmOtherTutorAppointment(chatState):
    pairs = (
    (r'yes(.*)',
     ("Great! I will transfer then",
      "Great! I will transfer then")),

    (r'no(.*)',
     ("OK. Then you will have to wait",
      "OK. Then you will have to wait")),

    );


    def respond(self, str):
        for (pattern, response) in self._pairs:
            match = pattern.match(str)
            if match:
                resp = random.choice(response)    # pick a random response
                print "Slamy > "+resp
                sys.exit(0)
        print "Slamy > I understad. But you will wait or talk to other tutor. Do you want to chat with a different tutor?"
        return self


slamy = GradeSlamChat()

if __name__ == "__main__":
    slamy.converse()