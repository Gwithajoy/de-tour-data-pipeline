import os
import pandas as pd


강원도, 경기도, 경상남도, 경상북도, 광주광역시, 대구광역시, 대전광역시, 부산광역시, 서울특별시, 세종특별자치시, 울산광역시= [],[],[],[],[],[],[],[],[],[],[]
인천광역시, 전라남도, 전라북도, 제주특별자치도, 충청남도, 충청북도 = [],[],[],[],[],[]

location_map = {"강원" : "강원도",
                "경기":"경기도",
                "경남":"경상남도",
                "경북":"경상북도",
                "광주":"광주광역시",
                "대구":"대구광역시",
                "대전":"대전광역시",
                "부산":"부산광역시",
                "서울":"서울특별시",
                "세종시":"세종특별자치시",
                "울산":"울산광역시",
                "인천":"인천광역시",
                "전남":"전라남도",
                "전북":"전라북도",
                "제주":"제주특별자치도",
                "충남":"충청남도",
                "충북":"충청북도"
                }

def sort_by_location_year_month(file_location, description):
     
    for file in os.listdir(file_location):
        if '.xlsx' in file:
            df = pd.read_excel(file_location + file)
            print(file.split('_')[-1].split('.')[0])
            #파일을 기준연월을 추가하는 과정#
            df['기준연월'] = file.split('_')[-1].split('.')[0]
            #도로명주소에서 지역명 가져와서 지역명 ex) 강원 -> 강원도 / 세종시 ->세종특별자치시
            df['지역명'] = df['도로명주소'].apply(lambda x: location_map[x.split()[0]])
            df= df.drop('도로명주소', axis=1)
            #파일을 구분하는 과정#
            if '강원도' in file:
                강원도.append(df)
            elif '경기도' in file:
                경기도.append(df)
            elif '경상남도' in file:
                경상남도.append(df)
            elif '경상북도' in file:
                경상북도.append(df)
            elif '광주광역시' in file:
                광주광역시.append(df)
            elif '대구광역시' in file:
                대구광역시.append(df)
            elif '대전광역시' in file:
                대전광역시.append(df)
            elif '부산광역시' in file:
                부산광역시.append(df)
            elif '서울특별시' in file:
                서울특별시.append(df)
            elif '세종특별자치시' in file:
                세종특별자치시.append(df)
            elif '울산광역시' in file:
                울산광역시.append(df)
            elif '인천광역시' in file:
                인천광역시.append(df)
            elif '전라남도' in file:
                전라남도.append(df)
            elif '전라북도' in file:
                전라북도.append(df)
            elif '제주특별자치도' in file:
                제주특별자치도.append(df)
            elif '충청남도' in file:
                충청남도.append(df)
            elif '충청북도' in file:
                충청북도.append(df)

    #파일을 모으는 과정
    강원모음= pd.concat(강원도)
    경기모음= pd.concat(경기도)
    경남모음= pd.concat(경상남도)
    경북모음= pd.concat(경상북도)
    광주모음= pd.concat(광주광역시)
    대구모음= pd.concat(대구광역시)
    대전모음= pd.concat(대전광역시)
    부산모음= pd.concat(부산광역시)
    서울모음= pd.concat(서울특별시)
    세종모음= pd.concat(세종특별자치시)
    울산모음= pd.concat(울산광역시)
    인천모음= pd.concat(인천광역시)
    전남모음= pd.concat(전라남도)
    전북모음= pd.concat(전라북도)
    제주모음= pd.concat(제주특별자치도)
    충남모음= pd.concat(충청남도)
    충북모음= pd.concat(충청북도) 

    #파일을 내보내는 형식지정
    강원모음.to_csv(file_location+f'경기모음_{description}.csv', index =False)
    경남모음.to_csv(file_location+f'경남모음_{description}.csv', index =False)
    경북모음.to_csv(file_location+f'경북모음_{description}.csv', index =False)
    광주모음.to_csv(file_location+f'광주모음_{description}.csv', index =False)
    대구모음.to_csv(file_location+f'대구모음_{description}.csv', index =False)
    대전모음.to_csv(file_location+f'대전모음_{description}.csv', index =False)
    부산모음.to_csv(file_location+f'부산모음_{description}.csv', index =False)
    서울모음.to_csv(file_location+f'서울모음_{description}.csv', index =False)
    세종모음.to_csv(file_location+f'세종모음_{description}.csv', index =False)
    울산모음.to_csv(file_location+f'울산모음_{description}.csv', index =False)
    인천모음.to_csv(file_location+f'인천모음_{description}.csv', index =False)
    전남모음.to_csv(file_location+f'전남모음_{description}.csv', index =False)
    전북모음.to_csv(file_location+f'전북모음_{description}.csv', index =False)
    제주모음.to_csv(file_location+f'제주모음_{description}.csv', index =False)
    충남모음.to_csv(file_location+f'충남모음_{description}.csv', index =False)
    충북모음.to_csv(file_location+f'충북모음_{description}.csv', index =False)
   