# # torch
# import torch
# from torch import nn
# import torch.nn.functional as F
# import torch.optim as optim
# from torch.utils.data import Dataset, DataLoader
# import gluonnlp as nlp
# import numpy as np
# from tqdm import tqdm, tqdm_notebook
#
# # kobert
# from kobert.utils import get_tokenizer
# from kobert.pytorch_kobert import get_pytorch_kobert_model
#
# # CPU 사용
# device = torch.device("cpu")
#
# # BERT 모델, Vocabulary 불러오기 필수
# bertmodel, vocab = get_pytorch_kobert_model()
#
# ## Setting parameters
# max_len = 512
# batch_size = 32
# warmup_ratio = 0.1
# num_epochs = 10
# max_grad_norm = 1
# log_interval = 200
# learning_rate = 5e-5
#
# # KoBERT에 입력될 데이터셋 정리
# class BERTDataset(Dataset):
#     def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len, pad, pair):
#         transform = nlp.data.BERTSentenceTransform(bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)
#
#         self.sentences = [transform([i[sent_idx]]) for i in dataset]
#         self.labels = [np.int32(i[label_idx]) for i in dataset]
#
#     def __getitem__(self, i):
#         return (self.sentences[i] + (self.labels[i],))
#
#     def __len__(self):
#         return (len(self.labels))
#
#
# # 모델 정의
# class BERTClassifier(nn.Module):  ## 클래스를 상속
#     def __init__(self, bert, hidden_size=768, num_classes=6,  ##클래스 수 조정##
#                  dr_rate=None, params=None):
#         super(BERTClassifier, self).__init__()
#         self.bert = bert
#         self.dr_rate = dr_rate
#
#         self.classifier = nn.Linear(hidden_size, num_classes)
#         if dr_rate:
#             self.dropout = nn.Dropout(p=dr_rate)
#
#     def gen_attention_mask(self, token_ids, valid_length):
#         attention_mask = torch.zeros_like(token_ids)
#         for i, v in enumerate(valid_length):
#             attention_mask[i][:v] = 1
#         return attention_mask.float()
#
#     def forward(self, token_ids, valid_length, segment_ids):
#         attention_mask = self.gen_attention_mask(token_ids, valid_length)
#
#         _, pooler = self.bert(input_ids=token_ids, token_type_ids=segment_ids.long(),
#                               attention_mask=attention_mask.float().to(token_ids.device))
#         if self.dr_rate:
#             out = self.dropout(pooler)
#         return self.classifier(out)
#
#
#
# def new_softmax(a):
#     c = np.max(a)
#     exp_a = np.exp(a - c)
#     sum_exp_a = np.sum(exp_a)
#     y = (exp_a / sum_exp_a) * 100
#     return np.round(y, 3)
#
#
# def predict(predict_sentence):
#     tokenizer = get_tokenizer()
#     tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)
#
#     model1 = BERTClassifier(bertmodel, dr_rate=0.5)
#     model1.load_state_dict(torch.load("/Users/dmswl/Capstone/api/post/testmodel.pt", map_location = 'cpu'))
#     model1.to(device)
#
#     data = [predict_sentence, '0']
#     dataset_another = [data]
#
#     another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
#     test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size, num_workers=5)
#
#     model1.eval()
#
#     for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
#         token_ids = token_ids.long().to(device)
#         segment_ids = segment_ids.long().to(device)
#         valid_length = valid_length
#         label = label.long().to(device)
#
#         out = model1(token_ids, valid_length, segment_ids)
#
#         test_eval = []
#         for i in out:
#             logits = i
#             logits = logits.detach().cpu().numpy()
#
#             if np.argmax(logits) == 0:
#                 test_eval.append("기쁨이 ")
#             elif np.argmax(logits) == 1:
#                 test_eval.append("당황이 ")
#             elif np.argmax(logits) == 2:
#                 test_eval.append("분노가 ")
#             elif np.argmax(logits) == 3:
#                 test_eval.append("불안이 ")
#             elif np.argmax(logits) == 4:
#                 test_eval.append("상처가 ")
#             elif np.argmax(logits) == 5:
#                 test_eval.append("슬픔이 ")
#
#             print(" >> 입력하신 내용에서 " + test_eval[0] + "느껴집니다.")
#
#     return test_eval[0]
