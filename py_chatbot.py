import random, re
from collections import defaultdict
from chatbot import Chat, reflections, multiFunctionCall
import wikipedia


def whoIs(query, sessionID="general"):
    try:
        return wikipedia.summary(query)
    except:
        for newquery in wikipedia.search(query):
            try:
                return wikipedia.summary(newquery)
            except:
                pass
    return "I don't know about " + query


call = multiFunctionCall({"whoIs": whoIs})
firstQuestion = "Hi, how are you?"
Chat('sentences.text', reflections, call=call).converse(firstQuestion)


class LString:
    def __init__(self):
        self._total = 0
        self._successors = defaultdict(int)

    def put(self, word):
        self._successors[word] += 1
        self._total += 1

    def get_random(self):
        ran = random.randint(0, self._total - 1)
        for key, value in self._successors.items():
            if ran < value:
                return key
            else:
                ran -= value


couple_words = defaultdict(LString)


def load(phrases):
    with open(phrases, 'r') as f:
        for line in f:
            add_message(line)


def add_message(message):
    message = re.sub(r'[^\w\s\']', '', message).lower().strip()
    words = message.split()
    for i in range(2, len(words)):
        couple_words[(words[i - 2], words[i - 1])].put(words[i])
        couple_words[(words[-2], words[-1])].put("")


def generate():
    result = []
    while len(result) < 10 or len(result) > 20:
        result = []
        s = random.choice(list(couple_words.keys()))
        result.extend(s)
        while result[-1]:
            w = couple_words[(result[-2], result[-1])].get_random()
            result.append(w)

    return " ".join(result)


if __name__ == "__main__":
    load("sentences.text")
    print(generate())
