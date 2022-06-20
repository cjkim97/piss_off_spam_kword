## 사용 모듈 ##
import pandas as pd
import hgtk # 초성 얻는 모듈 
import itertools # 순열구하는 모둘

# 형태소분석
from konlpy.tag import Okt

class main_setting:
    '''
    각 종 공유 변수들을 세팅함
    - TAG_LIST : 일반 Konlpy Tag 목록
    - MO : 모음
    - JA : 자음
    - DOUBLE_JA : 쌍자음으로 사용할 수 있는 자음
    - COMPLETE_FAKE_LETTER : 완전한 글자 이모티콘
    - DEL_PUNCTUATION : 무시할 기호 목록
    - DEL_TAG : 무시할 TAG 목록
    - DEL_NUMBER : 무시할 숫자 목록
    '''
    def __init__(self, tagger = Okt(), nice_to_meet_u = True, tagger_name = 'Okt'):
        # 다른 태거의 범용성을 고려할 필요가 있음
        self.TAGGER = tagger
        if nice_to_meet_u:
            self.TAGGER = Okt()
            readme = '만나서 반갑습니다! Mail : nuang0530@naver.com'
            print(readme)
            print(f'Initialize the {tagger_name} Tagger...')
            # 태깅 초기화
            pos = self.TAGGER.pos(readme)
            print(f'Complete initializing!!!')
        
        # 정상 태그
        self.TAG_LIST=['Adjective', 'Adverb', 'Conjunction', 'Determiner', 'Eomi', 
                       'Exclamation', 'Josa', 'Noun', 'PreEomi', 'Suffix', 'Verb',
                       'VerbPrefix', 'Modifier']
        
        # 모음과 자음
        self.MO= list('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
        self.JA = list('ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㄲㄸㅃㅆㅉ')
        self.DOUBLE_JA = ['ㄱ','ㄷ','ㅂ','ㅅ','ㅈ'] # 쌍자음 가능한 자음
        
        # 딕셔너리 형태
        self.KP_DICT={'ja':self.JA,'mo':self.MO}

        # 완전한 글자 이모티콘(추후 추가 예정 및 방식 변경 가능성 있음)
        self.COMPLETE_FAKE_LETTER = [chr(i) for i in range(ord('㈎'), ord('㈎')+17)]
        self.COMPLETE_FAKE_LETTER.extend([chr(i) for i in range(ord('㉮'), ord('㉮')+17)])
        self.COMPLETE_FAKE_LETTER.extend([chr(i) for i in range(ord('㉠'), ord('㉭')+1)])
        self.COMPLETE_FAKE_LETTER.extend([chr(i) for i in range(ord('㈀'), ord('㈍')+1)])

        # 무시할 기호 목록
        self.DEL_PUNCTUATION = [',','.',"'",'"','?',';',':']
        self.DEL_TAG=['Email', 'URL', 'ScreenName']
        self.DEL_NUMBER = ['2','3','4','5','8','9']
    