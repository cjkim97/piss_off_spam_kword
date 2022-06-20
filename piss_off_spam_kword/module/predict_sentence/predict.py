

class Predict:
    def __init__(self):
        # 폰트 설정 ** 갓터리 - 파란망고 - 타이포럭키 순서를 지켜주세요 ** 
        font_path = 'font/'
        self.FONT=[font_path+'OdGodttery.ttf',font_path+'LAB파란망고.ttf',
        font_path+'Typo_luckypangB.ttf']
    
    def input_preprocess(self,input_data):
        Id = [] 
        Part_Id = []
        letter = []

        for key in input_data.keys():
            part_id = 0
            for partition in input_data[key]:
                Id.extend([key for _ in range(len(partition))])
                Part_Id.extend([part_id for _ in range(len(partition))])
                letter.extend([letter for letter in partition])
                part_id += 1

        input_dict = {'result_id': Id,
                    'partition_id': Part_Id,
                    'letter': letter}
        input_df = pd.DataFrame(input_dict)
        input_df['pred_letter_440'] = [np.nan for _ in range(len(input_df))] # 나중에 예측결과가 올 것
        input_df['pred_letter_385'] = [np.nan for _ in range(len(input_df))] # 나중에 예측결과가 올 것
        input_df['pred_letter_759'] = [np.nan for _ in range(len(input_df))] # 나중에 예측결과가 올 것

        input_df['pred_score_440']=[np.nan for _ in range(len(input_df))] # 나중에 예측확률이 올 것
        input_df['pred_score_385'] = [np.nan for _ in range(len(input_df))] # 나중에 예측확률이 올 것
        input_df['pred_score_759'] = [np.nan for _ in range(len(input_df))] # 나중에 예측확률이 올 것

        input_df['pred_letter_best'] = [np.nan for _ in range(len(input_df))] # 나중에 최종예측결과가 올 것

        return input_df