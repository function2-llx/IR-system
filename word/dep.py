import json
from tqdm import tqdm
from ltp import LTP

if __name__ == '__main__':
    batch_size = 32
    ltp = LTP('base')
    print('loaded ltp model')
    lines = list(open('../rmrb1946-2003-delrepeat.all'))[:10000]
    corpus = []
    for i in tqdm(range(0, len(lines), batch_size)):
        batch = list(map(str.strip, lines[i:i + batch_size]))
        batch_tokens, hidden = ltp.seg(batch, is_preseged=False)
        batch_pos = ltp.pos(hidden)
        batch_dep = ltp.dep(hidden)
        corpus.extend([{
            'tokens': tokens,
            'pos': pos,
            'dep': dep,
        } for tokens, pos, dep in zip(batch_tokens, batch_pos, batch_dep)])
    json.dump(corpus, open('corpus.json', 'w'), indent=4, ensure_ascii=False)
