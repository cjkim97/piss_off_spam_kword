################## 사용 모듈 #####################
import pandas as pd

# 초성 얻어 낼려고
import hgtk

# ㄷㄷㄷ, ㅋㅋㅋ , ㅠㅠㅠ -> ㄷㄷ, ㅋㅋ, ㅠㅠ 로 변환
from soynlp.normalizer import *

# 순열 구하기
import itertools

import warnings
warnings.filterwarnings('ignore')

# 형태소분석
from konlpy.tag import Okt
##################################################

'''
preprocessor 속성
- TAGGER
- TAG_LIST
- KP_DICT
- double_ja
- COMPLETE_FAKE_LETTER
- DEL_PUNCTUATION
- DEL_NUMBER

preprocessor 메서드
- init
- 
'''



class preprocessor:
    # ====================================================================
    # __init__
    if True:
        # --------------------------------------------------------------------
        # 주 메서드
        def __init__(self):
            self.TAGGER=Okt()

            self.TAG_LIST=['Adjective', 'Adverb', 'Conjunction', 'Determiner', 'Eomi', 'Exclamation', 'Josa', 'Noun', 'PreEomi', 'Suffix', 'Verb',
            'VerbPrefix', 'Modifier']

            mo = list('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
            ja = list('ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉ')

            self.KP_DICT={'ja':ja,'mo':mo}

            self.double_ja = ['ㄱ','ㄷ','ㅂ','ㅅ','ㅈ']

            COMPLETE_FAKE_LETTER = [chr(i) for i in range(ord('㈎'), ord('㈎')+17)]
            COMPLETE_FAKE_LETTER.extend([chr(i) for i in range(ord('㉮'), ord('㉮')+17)])
            COMPLETE_FAKE_LETTER.extend([chr(i) for i in range(ord('㉠'), ord('㉭')+1)])
            COMPLETE_FAKE_LETTER.extend([chr(i) for i in range(ord('㈀'), ord('㈍')+1)])

            self.DEL_PUNCTUATION = [',','.',"'",'"','?',';',':']
            self.DEL_TAG=['Email', 'URL', 'ScreenName']
            self.DEL_NUMBER = ['2','3','4','5','8','9']

            self.complete_fake_df = pd.DataFrame(COMPLETE_FAKE_LETTER, index=range(len(COMPLETE_FAKE_LETTER)), columns = ['완전형 특수기호'])
            self.complete_fake_df['특수기호_아스키코드'] = self.complete_fake_df['완전형 특수기호'].apply(lambda x: ord(x))

            data1 = list('가나다라마바사아자차카타파하주')
            tmp = list('가나다라마바사아자차카타파하')
            data2 = ['오전','오후']
            data3 = ['참고','주의','우']
            data4 = list('ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ')

            data1.extend(data2)
            data1.extend(tmp)
            data1.extend(data3)
            data1.extend(data4)
            data1.extend(data4)

            self.complete_fake_df['완전형 문자'] = data1
            self.complete_fake_df['문자_아스키코드'] = self.complete_fake_df['완전형 문자'].apply(lambda x: self.to_complete_ascii(x))

        # --------------------------------------------------------------------       
        # 보조 메서드
        if True:
            def to_complete_ascii(self,x):
                result = ''
                for ind, char in enumerate(x):
                    result += str(ord(char))
                    if ind < len(x)-1:
                        result +=','
                return result

    # ====================================================================
    # first_preprocessing    
    if True:
        # --------------------------------------------------------------------
        # 주 메서드
        def first_preprocessing(self,text):
            text = self.complete_fake_to_real(text)
            text = self.first_tag_check(text)
            return text

        # --------------------------------------------------------------------       
        # 보조 메서드
        if True:
            # complete_fake_to_real
            def complete_fake_to_real(self,text):
                text_list = list(text)
                
                for ind, comp in enumerate(text_list):
                    tmp = self.complete_fake_df[self.complete_fake_df['완전형 특수기호']==comp]['완전형 문자']
                    if len(tmp.values):
                        text_list[ind] = tmp.iloc[0]
                        
                return ''.join(text_list)

            # first_tag_check            
            def first_tag_check(self,text):
                pos = self.TAGGER.pos(text)

                for comp,tag in pos:
                    if (tag == 'Alpha') and (len(comp)>=5) or (tag in self.DEL_TAG) or (comp in self.DEL_PUNCTUATION) or (comp in self.DEL_NUMBER):
                        text = text.replace(comp,'')

                return text
              
    # ====================================================================
    # morpheme_processing   
    if True:
        # --------------------------------------------------------------------
        # 주 메서드        
        def morpheme_processing(self,text):
            text = ' '.join(text)
            # 삭제가 덜 된 형태소 체크를 한번 더 하겠습니다
            text = self.first_tag_check(text)
            
            tmp_letter_list = []
            tmp_tag_list = []

            result_list = []
            result_tag_list = []
            
            pos = self.TAGGER.pos(text)
          
            for letter,tag in pos:

                if not len(tmp_letter_list):
                    tmp_letter_list.append(letter)
                    tmp_tag_list.append(tag)
                    continue
                
                if tag in self.TAG_LIST:

                    if len(tmp_letter_list) == 1:
                        if (tmp_letter_list[-1] in self.double_ja) and (tmp_letter_list[-1] == hgtk.letter.decompose(letter)[0]):
                            tmp_letter_list.append(letter)
                            tmp_tag_list.append(tag)
                        else: 
                            tmp_letter_list = list()
                            tmp_tag_list = list()
                            tmp_letter_list.append(letter)
                            tmp_tag_list.append(tag)
                    else:
                        if (tmp_tag_list[-1] in self.TAG_LIST):
                            result_list.append(tmp_letter_list[:-1])
                            result_tag_list.append(tmp_tag_list[:-1])
                            tmp_letter_list = list()
                            tmp_tag_list = list()
                            tmp_letter_list.append(letter)
                            tmp_tag_list.append(tag)
                        elif (tmp_letter_list[-1] == hgtk.letter.decompose(letter)[0]):
                            tmp_letter_list.append(letter)
                            tmp_tag_list.append(tag)
                        else:
                            result_list.append(tmp_letter_list)
                            result_tag_list.append(tmp_tag_list)
                            tmp_letter_list = list()
                            tmp_tag_list = list()
                            tmp_letter_list.append(letter)
                            tmp_tag_list.append(tag)
                else:
                    if letter in self.KP_DICT['ja'] :
                        if len(tmp_letter_list)==1:
                            if ((tmp_letter_list[-1] == letter) and (letter in self.double_ja)):
                                tmp_letter_list.append(letter)
                                tmp_tag_list.append(tag)
                            else:
                                tmp_letter_list = list()
                                tmp_tag_list = list()
                                tmp_letter_list.append(letter)
                                tmp_tag_list.append(tag)
                        else:
                            if ((tmp_letter_list[-1] == letter) and (letter in self.double_ja)):
                                tmp_letter_list.append(letter)
                                tmp_tag_list.append(tag)
                            else:
                                result_list.append(tmp_letter_list)
                                result_tag_list.append(tmp_tag_list)
                                tmp_letter_list = list()
                                tmp_tag_list = list()
                                tmp_letter_list.append(letter)
                                tmp_tag_list.append(tag)
                    else:
                        tmp_letter_list.append(letter)
                        tmp_tag_list.append(tag)
                        

            if (len(tmp_letter_list) >=2) :
                result_list.append(tmp_letter_list)
                result_tag_list.append(tmp_tag_list)
            
            
            return result_list, result_tag_list

    # ====================================================================
    # part_to_image   
    if True:
        # --------------------------------------------------------------------
        # 주 메서드
        def part_to_image(self,weird_part, weird_part_tag):
                image_dict = {}
                ind = 0
                for parts, tags in zip(weird_part,weird_part_tag):
                    if ('Foreign' in tags) or ('Noun' in tags):
                        foreign = True
                    else:
                        foreign = False
                    partition_cases = self.get_partition_cases(len(parts),foreign)
                    part_case=[]
                    for case in partition_cases:
                        tmp_case=[]
                        tmp_slicing = 0
                        for slicing in case:
                            tmp_case.append(''.join(parts[tmp_slicing:tmp_slicing+slicing]))
                            tmp_slicing = tmp_slicing+slicing
                        part_case.append(tmp_case)
                    image_dict[ind] = part_case
                    ind+=1
                return image_dict

        # --------------------------------------------------------------------       
        # 보조 메서드
        if True:
            def get_partition_cases(self,n, foreign=False):
                case_list = []
                
                perm_list = []
                
                result_perm_list = []
                
                if foreign:
                    d_possible = [i for i in range(n//4,-1,-1)]
                    for d_pos in d_possible:
                        n2 = n-4*d_pos
                        c_possible = [i for i in range(n2//3,-1,-1)]
                        for c_pos in c_possible:
                            n3 = n2 - 3*c_pos
                            b_possible = [i for i in range(n2//2,-1,-1)]
                            for b_pos in b_possible:
                                n4 = n3 - 2*b_pos
                                a = n4
                                if (a>=0) and((a + 2*b_pos + 3*c_pos + 4*d_pos) == n):
                                    case_list.append((a,b_pos,c_pos,d_pos))
                    
                    for case in case_list:
                        tmp_perm = []
                        start = 1
                        for count in case:
                            use_group = [start for i in range(count)]
                            tmp_perm.extend(use_group)
                            start+=1
                        perm_list.append(tmp_perm)
                
                else:
                    c_possible = [i for i in range(n//4,-1,-1)]
                    for c_pos in c_possible:
                        n2 = n-4*c_pos
                        b_possible = [i for i in range(n2//3,-1,-1)]
                        for b_pos in b_possible:
                            n3 = n2 - 3*b_pos
                            a = n3//2
                            if (2*a + 3*b_pos + 4*c_pos) == n:
                                case_list.append((a,b_pos,c_pos))
                    for case in case_list:
                        tmp_perm = []

                        start = 2
                        for count in case:
                            use_group = [start for i in range(count)]
                            tmp_perm.extend(use_group)
                            start+=1
                        perm_list.append(tmp_perm)
                        
                for perm in perm_list:
                    nPr = list(itertools.permutations(perm, len(perm)))
                    result_perm_list.extend(nPr)
                                
                return set(result_perm_list)
        
    # ====================================================================
    # call 매서드
    def __call__(self,text):
        text                        =   self.first_preprocessing(text)
        # sd.Beep(500,500)
        weird_part,weird_part_tag   =   self.morpheme_processing(text)
        # sd.Beep(1000,500)
        image_dict                  =   self.part_to_image(weird_part,weird_part_tag)
        # sd.Beep(2000,500)
        return image_dict

