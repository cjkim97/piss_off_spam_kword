# 예측을 위한 전처리 함수
from PIL import ImageFont,ImageDraw,Image
import numpy as np
import itertools
from urllib.parse import unquote
import pandas as pd

def letter_to_image(letter_list, font_list = []):
    input_image = []
    for ttf in font_list:
        ttf_image = []
        for letter in letter_list:
            ttf_image.append(txt_to_bmp(letter, ttf))
        input_image.append(ttf_image)
    return input_image


def txt_to_bmp(text,use_font):
    chars = text
    font = ImageFont.truetype(font=use_font, size=100)
    x, y = font.getsize(chars)

    img_ground = Image.new('L', (x+3, y+3), color='white')
    img_draw = ImageDraw.Draw(img_ground)
    img_draw.text((0, 0), chars, font=font, fill='black')

    img = img_ground.resize((100, 100))
    img = np.array(img)
    img = abs(img/255-1)
    return img 

def sent_case(groups):
    result = []
    if len(groups) == 2:
        return list(itertools.product(groups[0], groups[1], repeat=1))
    elif len(groups) == 1:
        return list(itertools.product(groups[0], repeat=1))
    else:
        roots = groups[0]
        tmp = []
        for root in roots:
            tmp = (root,)
            for i in sent_case(groups[1:]):
                tmp += i
                result.append(tmp)
                tmp = (root,)
    return result

def change_sentence(self,text, id_list, input_df):
    text = text.replace(' ', '')
    ID = [i for i in range(len(id_list))]
    for i, j in zip(ID, id_list):
        tmp = input_df[(input_df['result_id'] == i) &
                        (input_df['partition_id'] == j)]
        # 바꿀 대상
        for a, pred in zip(tmp['letter'].values, tmp['pred_letter_best'].values):
            text = text.replace(a, pred, 1)
    return text


