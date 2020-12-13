import json
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

client = Elasticsearch()

if __name__ == '__main__':
    lines = open('docs-all.bulk').readlines()
    assert len(lines) % 2 == 0
    chunk_size = 1000

    for i in tqdm(range(0, len(lines), chunk_size)):
        cur_lines = lines[i:i + chunk_size]
        actions = []
        for j in range(0, len(cur_lines), 2):
            index, doc = map(json.loads, cur_lines[j:j + 2])
            actions.append({
                '_id': i * chunk_size + j,
                '_source': doc,
            })
        results = bulk(client, actions, index='docs')
 