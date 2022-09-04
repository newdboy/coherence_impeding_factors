# data from: aihub essay data (https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=545)

import json
from pprint import pprint
import numpy as np
import os
from tqdm import tqdm
import pandas as pd
import re

# import json files
folder_path = 'Users/kintch/Dropbox/sj/2022-2/2. 설명문 응집성 저해 요인 (한국작문학회) 9:10/설명글_training'

# make root / file name list
json_path_list = list()
for (root, directories, files) in os.walk(folder_path):
    json_path_list.append([root, files])
file_names = json_path_list[0][1]
root = json_path_list[0][0]

# extract data from json
coh_scores = list()
texts = list()
text_subjs = list()
text_prompts = list()
text_types = list()
stu_grades = list()
for file_name in tqdm(file_names):
    json_path = os.path.join(root, file_name)
    with open(json_path, 'r') as f:
        json_data = json.load(f)

        # confirm dict
        # [key for key, value in json_data.items()]

        # extract infos from json
        coh_score_3rater = list(map(lambda x: x[2], json_data['score']['essay_scoreT_detail']['essay_scoreT_org']))  #coherece 점수만 추출
        coh_score = np.average(coh_score_3rater)
        text = json_data['paragraph'][0]['paragraph_txt']
        text_subj = json_data['info']['essay_main_subject']  # '영화/독서감상문'
        text_prompt = json_data['info']['essay_prompt']  # 과제지시문
        text_type = json_data['info']['essay_type']  # 설명글
        stu_grade = json_data['student']['student_grade']

        # appending
        coh_scores.append(coh_score)
        texts.append(text)
        text_subjs.append(text_subj)
        text_prompts.append(text_prompt)
        text_types.append(text_type)
        stu_grades.append(stu_grade)

# make dataframe
data_frame = pd.DataFrame({
    'coh_scores': coh_scores,
    'texts': texts,
    'text_subjs': text_subjs,
    'text_prompts': text_prompts,
    'text_types': text_types,
    'stu_grades': stu_grades
              })

data_frame.to_csv('/Users/kintch/Dropbox/sj/2022-2/2. 설명문 응집성 저해 요인 (한국작문학회) 9:10/data_for_coh.csv',
                  encoding='utf-8')

# extract students' dataframe who show low coherece
coh01_students = data_frame[data_frame.coh_scores <= 1]
coh12_students = data_frame[(data_frame.coh_scores <= 2) & (data_frame.coh_scores > 1)]
# coh01_students.groupby('coh_scores').size()
coh01_students.groupby('stu_grades').size()
data_frame.groupby('stu_grades').size()
# df.groupby(['col1','col2']).size()
coh01_students.groupby('text_prompts').size()

# prompt text numbering
pt_text_numbering = dict()
n = 0
for pt_text in list(set(coh01_students['text_prompts'].tolist())):
    pt_text_numbering[pt_text] = n
    n += 1
pt_text_numbering

# extract only low coherece texts
coh01_texts = data_frame.texts[data_frame.coh_scores <= 1].tolist()
coh12_texts = data_frame.texts[(data_frame.coh_scores <= 2) & (data_frame.coh_scores > 1)].tolist()
# preprocessing
coh01_texts_pped = list(map(lambda x: re.sub(r'#@문장구분#', '', x), coh01_texts))
coh12_texts_pped = list(map(lambda x: re.sub(r'#@문장구분#', '', x), coh12_texts))

# save students' text to txt (line by lines)
with open('/Users/kintch/Dropbox/sj/2022-2/2. 설명문 응집성 저해 요인 (한국작문학회) 9:10/coh12_texts.txt',
          'w', encoding='utf-8') as f:
    n = 0
    for text in coh12_texts_pped:
        f.writelines('학생' + str(n) + '\n' + text + '\n' + '\n')
        n += 1

# save prompt text to txt (line by lines)
with open(
        '/Users/kintch/Dropbox/sj/2022-2/2. 설명문 응집성 저해 요인 (한국작문학회) 9:10/prompt_texts.txt',
        'w', encoding='utf-8') as f:
    n = 0
    for p_text in list(set(coh01_students['text_prompts'].tolist())):
        f.writelines(
            '프롬프트'
            + str(n)
            + '\n'
            + p_text
            + '\n'
            + '---' * 30
            + '---'*30
            + '\n')
        n += 1
