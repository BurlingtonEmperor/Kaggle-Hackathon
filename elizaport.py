import re
import random

# Reflections used to switch pronouns
reflections = {
    "am": "are",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

# Simple reflection function
def reflect(fragment):
    tokens = fragment.lower().split()
    reflected = [reflections.get(word, word) for word in tokens]
    return ' '.join(reflected)

# Pattern-response pairs
patterns = [
    (r'I need (.*)',
     ["Why do you need {0}?",
      "Would it really help you to get {0}?",
      "Are you sure you need {0}?"]),

    (r'Why don\'?t you ([^\?]*)\??',
     ["Do you really think I don't {0}?",
      "Perhaps eventually I will {0}.",
      "Do you really want me to {0}?"]),

    (r'Why can\'?t I ([^\?]*)\??',
     ["Do you think you should be able to {0}?",
      "If you could {0}, what would you do?",
      "I don't know -- why can't you {0}?",
      "Have you really tried?"]),

    (r'I can\'?t (.*)',
     ["How do you know you can't {0}?",
      "Perhaps you could {0} if you tried.",
      "What would it take for you to {0}?"]),

    (r'I am (.*)',
     ["Did you come to me because you are {0}?",
      "How long have you been {0}?",
      "How do you feel about being {0}?"]),

    (r'I\'?m (.*)',
     ["Why are you {0}?",
      "How does being {0} make you feel?",
      "Do you enjoy being {0}?"]),

    (r'(.*) mother(.*)',
     ["Tell me more about your mother.",
      "What was your relationship with your mother like?",
      "How do you feel about your mother?"]),

    (r'Hello(.*)',
     ["Hello... I'm glad you could drop by today.",
      "Hi there... how are you today?",
      "Hello, how are you feeling today?"]),

    (r'Quit',
     ["Thank you for talking with me.",
      "Goodbye.",
      "Have a great day!"]),

    (r'(.*)',
     ["Please tell me more.",
      "Let's change focus a bit... Tell me about your family.",
      "Can you elaborate on that?",
      "Why do you say that {0}?",
      "I see.",
      "Very interesting.",
      "{0}.",
      "I see. And what does that tell you?",
      "How does that make you feel?",
      "How do you feel when you say that?"])
]

# Main chat loop
def eliza_chat():
    print("ELIZA: Hello. How are you feeling today?")
    while True:
        user_input = input("YOU: ")
        if user_input.lower() in ['quit', 'exit']:
            print("ELIZA: Goodbye. Take care!")
            break
        for pattern, responses in patterns:
            match = re.match(pattern, user_input, re.IGNORECASE)
            if match:
                response = random.choice(responses)
                groups = match.groups()
                reflected_groups = [reflect(g) for g in groups]
                print("ELIZA:", response.format(*reflected_groups))
                break

if __name__ == "__main__":
    eliza_chat()
