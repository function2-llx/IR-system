import json
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

client = Elasticsearch()

inner_sep = '\t'
token_sep = ' '

if __name__ == '__main__':
    corpus = json.load(open('sample.json'))
    chunk_size = 1000

    for i in tqdm(range(0, len(corpus), chunk_size)):
        batch = corpus[i:i + chunk_size]
        actions = []
        for j, doc in enumerate(corpus[i:i + chunk_size]):
            tokens = doc['tokens']
            content = token_sep.join([inner_sep.join((token, pos, tokens[head - 1] if head else '', rel)) for token, pos, (_, head, rel) in zip(tokens, doc['pos'], doc['dep'])])
            actions.append({
                '_id': i * chunk_size + j,
                '_source': {'content': content}
            })
        results = bulk(client, actions, index='docs')
