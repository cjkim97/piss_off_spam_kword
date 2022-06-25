# piss_off_spam_kword
ㅅr 고ㅏ E l ㅂ i 물렀거라

### 📌 프로젝트를 만든 이유
유투브를 보면서 가장 많이 보는 화면이 있습니다. 물론 영상 목록이겠지만, 영상 별 달린 댓글을 쭉 읽게 되는데 한때 xx티비 광고가 댓글을 점령했던 영상을 본 적도 있었고, 해당 유투버가 차단 키워드를 설정했는지 xxEl비 등 다양한 변화로 키워드를 피해가는 것을 볼 수 있었습니다. 그래서 재밌겠다 싶어서 '사과티비'라는 키워드만 입력해서 모든 변화구를 다 잡아보는 프로젝트를 진행하게 되었습니다

### 📂 모듈 구조
- 📁 piss_off_spam_kword
    - 📁 model : 해당 서비스에 사용되는 ML/DL 등의 모델 관련 소스들이 들어 있습니다
        - __ init __.py
        - 추후 수정
    - 📁 module : 해당 서비스에 사용되는 python 모듈이 있습니다
        - __ init __.py
        - 📁 complete_fake_df(완료) : 완전형 특수문자(ex. ㉼)를 원래 문자로 바꿔주는 모듈
            - __ init __.py
            - making_complete_fake_df.py
        - 📁 predict_sentence(미완) : 문자 예측에 관련된 모듈
            - 📁 base 
            - 📁 files
            - 📁 font
            - __ init __.py
            - predict.py
        - 📁 text_preprocessing(완료) : 텍스트 처리에 관련된 모듈
            - 📁 default
            - __ init __.py
            - text_preprocessing.py
    - 📁 utils : 모듈에 사용되는 각 종 함수들이 있습니다
        - __ init __.py
        - functions_for_math.py : 수학계산에 사용되는 함수들
        - functions_for_predict.py : 예측 모듈에 사용되는 함수들
        - functions_for_text.py : 텍스트 처리에 사용되는 함수들