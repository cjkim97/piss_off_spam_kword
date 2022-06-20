import sys
sys.path.append('/Users/gimchaejeong/Desktop/Projects/piss_off_spam_kword/piss_off_spam_kword/')

import pandas as pd
from module import main_setting
from utils.change_to_code import to_complete_ascii

class making_complete_fake_df(main_setting):
    def __init__(self):
        super().__init__()
    
    def making(self, to_csv=True, file_name='complete_fake_df.csv'):
        complete_fake_df = pd.DataFrame(self.COMPLETE_FAKE_LETTER, 
                                        index=range(len(self.COMPLETE_FAKE_LETTER)), 
                                        columns = ['complete_emoji'])
        
        complete_fake_df['emoji_ascii'] = complete_fake_df['complete_emoji'].apply(lambda x: ord(x))
        
        
        # 위에 맞춰서 데이터 작성하는 부분인데.. 추후 수정 가능성 높음
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
        ##################################################
        
        
        complete_fake_df['complete_letter'] = data1
        complete_fake_df['letter_ascii'] = complete_fake_df['complete_emoji'].apply(lambda x: to_complete_ascii(x))
        print('Finish making the complete_fake_df!!')
        
        
        if to_csv:
            # 나중에 상대경로 지정 해줘야 함
            pd.to_csv('default/'+file_name, index=False)
            print('Finish saving the complete_fake_df!!')
        
        return complete_fake_df