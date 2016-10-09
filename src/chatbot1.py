import random

gs_greetings = ['hi, how can i help you?', 'hi! welcome to GradeSlam!', 'hello! How can i help you today?']
greetings = ['hola', 'hello', 'hi', 'Hi', 'hey!','hey']
random_greeting = random.choice(greetings)



question = ['How are you?','How are you doing?']
responses = ['Okay',"I'm fine"]
random_response = random.choice(responses)


print "GradeSlam chatbot ver 0.0.1. Type exit to terminate.\n\n"

greeting = random.choise(gs_greetings)
print ">>> "+greeting

exit_program = False
while True:

    userInput = raw_input(">>> ")
    if userInput == "exit":
      exit_program = True
    elif userInput in greetings:
      print ""