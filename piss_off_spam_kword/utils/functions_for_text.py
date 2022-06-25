# 코드 to 문자 / 문자 to 코드 등의 각 종 변경 함수들
from konlpy.tag import Okt


def to_complete_ascii(x):
    result = ''
    for ind, char in enumerate(x):
        result += str(ord(char))
        if ind < len(x)-1:
            result +=','
    return result

def first_tag_check(text, tagger, DEL_TAG = [], DEL_PUNCTUATION = [], USE_NUMBER = []):
    # 반드시 Okt 여야 하는데 이부분은 바뀔 가능성이 없어서 그냥 고정으로 가도 될듯..?
    pos = tagger.pos(text)
    for comp,tag in pos:
        if (tag == 'Alpha') and (len(comp)>=5) or (tag == 'Number' and comp not in USE_NUMBER) \
        or (tag in DEL_TAG) or (comp in DEL_PUNCTUATION):
            text = text.replace(comp,'')
    return text

def complete_fake_to_real(text, df):
    text_list = list(text)

    for ind, comp in enumerate(text_list):
        tmp = df[df['complete_emoji']==comp]['complete_letter']
        if len(tmp.values):
            text_list[ind] = tmp.iloc[0]

    return ''.join(text_list)

def comp_to_len(input_data):
    for key in input_data:
        input_data[key] = list(range(len(input_data[key])))
    
    return input_data