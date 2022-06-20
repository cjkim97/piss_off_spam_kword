import sys
sys.path.append('/Users/gimchaejeong/Desktop/Projects/piss_off_spam_kword/piss_off_spam_kword/')

import pandas as pd
import hgtk
from module import main_setting
from utils.functions_for_text import first_tag_check, complete_fake_to_real
from utils.functions_for_math import cartesian_product

class TextPreprocessing(main_setting):
    def __init__(self,text = '', complete_fake_df_path = '../complete_fake_df/default/complete_fake_df.csv'):
        super().__init__()
        self.complete_fake_df = pd.read_csv(complete_fake_df_path)
        self.origin_text = text
            
    def process(self):
        
        text = self.Stage1(self.origin_text)
        weird_part, weird_part_tag = self.Stage2(text)
        
        return self.Stage3(weird_part, weird_part_tag)
        
    def Stage1(self, text):
        
        text = complete_fake_to_real(text, df=self.complete_fake_df)
        text = first_tag_check(text, tagger = self.TAGGER)
        
        return text
    
    def Stage2(self, text):
        '''
        morpheme_processing
        '''
        text = ' '.join(text)
        # 삭제가 덜 된 형태소 체크를 한번 더 하겠습니다
        text = first_tag_check(text)

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
                    if (tmp_letter_list[-1] in self.DOUBLE_JA) and (tmp_letter_list[-1] == hgtk.letter.decompose(letter)[0]):
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
                        if ((tmp_letter_list[-1] == letter) and (letter in self.DOUBLE_JA)):
                            tmp_letter_list.append(letter)
                            tmp_tag_list.append(tag)
                        else:
                            tmp_letter_list = list()
                            tmp_tag_list = list()
                            tmp_letter_list.append(letter)
                            tmp_tag_list.append(tag)
                    else:
                        if ((tmp_letter_list[-1] == letter) and (letter in self.DOUBLE_JA)):
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
    
    def Stage3(self, weird_part, weird_part_tag):
        image_dict = {}
        ind = 0
        for parts, tags in zip(weird_part,weird_part_tag):
            if ('Foreign' in tags) or ('Noun' in tags):
                foreign = True
            else:
                foreign = False
            partition_cases = cartesian_product(len(parts),foreign)
            #print(partition_cases)
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

    
    
    