import random
import json

if __name__ == "__main__":
    corpus = json.load('corpus.json')
    n = int(len(corpus) / 10)
    corpus = random.sample(corpus, n)
    json.dump(corpus, open('sample.json', 'w'))
