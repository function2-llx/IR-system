import random

import torch
import numpy as np
from tqdm import tqdm
from transformers import BertModel, BertTokenizer

if __name__ == '__main__':
    random.seed(2333)
    tokenizer = BertTokenizer.from_pretrained('hfl/chinese-macbert-base')
    model = BertModel.from_pretrained('hfl/chinese-macbert-base').cuda()
    lines = list(open('rmrb1946-2003-delrepeat.all'))
    lines = random.sample(lines, k=500000)
    open('sample.txt', 'w').writelines(lines)
    batch_size = 16
    rep = np.zeros((len(lines), model.config.hidden_size))
    for i in tqdm(range(0, len(lines), batch_size), ncols=80):
        batch = list(map(str.strip, lines[i:i + batch_size]))
        inputs = tokenizer(batch, padding=True, truncation=True, return_tensors='pt', max_length=128)
        for k, v in inputs.items():
            inputs[k] = v.cuda()
        rep[i:i + batch_size, :] = model.forward(**inputs)[1].detach().cpu().numpy()
    np.save('rep.npy', rep)
