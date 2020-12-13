import sys

from transformers import BertModel, BertTokenizer

tokenizer = BertTokenizer.from_pretrained('hfl/chinese-macbert-base')
model = BertModel.from_pretrained('hfl/chinese-macbert-base').cuda()

print('transformer loaded')

while True:
    sent = input()
    inputs = tokenizer(sent, return_tensors='pt')
    for k, v in inputs.items():
        inputs[k] = v.cuda()
    outputs = model(**inputs)
    print(' '.join(map(str, outputs[1][0].tolist())))
    sys.stdout.flush()
