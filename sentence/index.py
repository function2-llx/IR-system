import json

from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import numpy as np

client = Elasticsearch()

if __name__ == '__main__':
    lines = list(map(str.strip, open('sentence.txt').readlines()))
    reps = np.load('rep.npy')
    chunk_size = 1000
    for i in tqdm(range(0, len(lines), chunk_size)):
        chunk_lines = lines[i:i + chunk_size]
        chunk_reps = reps[i:i + chunk_size]
        actions = []
        for j in range(0, len(chunk_lines), 2):
            actions.append({
                '_id': i * chunk_size + j,
                '_source': {
                    'content': chunk_lines[j],
                    'content_vector': chunk_reps[j].tolist(),
                },
            })
        results = bulk(client, actions, index='sentence')
