from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chatbot
chatbot = ChatBot('MyBot')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot on the English language data
trainer.train('chatterbot.corpus.english')

# Get a response from the chatbot
response = chatbot.get_response('Hello, how are you?')

print(response)
