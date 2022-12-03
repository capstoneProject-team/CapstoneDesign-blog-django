# torch
import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
import re
from tqdm import tqdm, tqdm_notebook
from kss import split_sentences

# kobert
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

# CPU 사용
device = torch.device("cpu")

# BERT 모델, Vocabulary 불러오기 필수
bertmodel, vocab = get_pytorch_kobert_model()


# KoBERT에 입력될 데이터셋 정리
class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i],))

    def __len__(self):
        return (len(self.labels))

    # 모델 정의


class BERTClassifier(nn.Module):  ## 클래스를 상속
    def __init__(self,
                 bert,
                 hidden_size=768,
                 num_classes=7,  ##클래스 수 조정##
                 dr_rate=None,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size, num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)

    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
        return attention_mask.float()

    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        _, pooler = self.bert(input_ids=token_ids, token_type_ids=segment_ids.long(),
                              attention_mask=attention_mask.float().to(token_ids.device))
        if self.dr_rate:
            out = self.dropout(pooler)
        return self.classifier(out)


tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

model1 = BERTClassifier(bertmodel, dr_rate=0.5)
model1.load_state_dict(torch.load("/capstone_deploy/backend/api/post/model-4.pt", map_location = 'cpu'))
model1.to(device)

## Setting parameters
max_len = 128
batch_size = 32
warmup_ratio = 0.1
num_epochs = 10
max_grad_norm = 1
log_interval = 200
learning_rate = 5e-5

def new_softmax(a):
    c = np.max(a)
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    y = (exp_a / sum_exp_a) * 100
    return np.round(y, 3)

def predict(content):
    dataset_another = []

    def makeContent():
        new_content = content.replace("\n", " ")
        pattern = '<[^>]*>'
        result_content = re.sub(pattern=pattern, repl='', string=new_content)
        print(result_content)
        sp_sen = split_sentences(result_content)
        for i in range(0, len(sp_sen)):
            data = [sp_sen[i], '0']
            dataset_another.append(data)

    makeContent()
    another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)
    emotion_list = []

    model1.eval()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)
        valid_length = valid_length
        label = label.long().to(device)

        out = model1(token_ids, valid_length, segment_ids)

        test_eval = []

        for i in out:
            logits = i
            logits = logits.detach().cpu().numpy()
            min_v = min(logits)
            total = 0
            probability = []
            logits = np.round(new_softmax(logits), 3).tolist()
            for logit in logits:
                probability.append(np.round(logit, 3))

            if np.argmax(logits) == 0:
                emotion = "기쁨"
            elif np.argmax(logits) == 1:
                emotion = "당황"
            elif np.argmax(logits) == 2:
                emotion = "분노"
            elif np.argmax(logits) == 3:
                emotion = "불안"
            elif np.argmax(logits) == 4:
                emotion = "상처"
            elif np.argmax(logits) == 5:
                emotion = "슬픔"
            elif np.argmax(logits) == 6:
                emotion = "중립"

            probability.append(emotion)
            emotion_list.append(emotion)

    a = b = c = d = e = f = g = 0
    for j in range(0, len(dataset_another)):
        print(str(j) + "." + dataset_another[j][0] + " >> " + emotion_list[j])
        print('---')
        dataset_another[j][1] = emotion_list[j]
        if emotion_list[j] == "기쁨":
            a += 1
        elif emotion_list[j] == "당황":
            b += 1
        elif emotion_list[j] == "분노":
            c += 1
        elif emotion_list[j] == "불안":
            d += 1
        elif emotion_list[j] == "상처":
            e += 1
        elif emotion_list[j] == "슬픔":
            f += 1
        elif emotion_list[j] == "중립":
            g += 1
    print(len(emotion_list), a, b, c, d, e, f, g)
    emotion_cnt = [a, b, c, d, e, f, g]
    print(emotion_cnt)
    return emotion_cnt
