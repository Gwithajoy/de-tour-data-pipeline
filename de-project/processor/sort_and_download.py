import os
import pandas as pd

LOCATION_MAP = {
    "강원": "강원도", "경기": "경기도", "경남": "경상남도", "경북": "경상북도",
    "광주": "광주광역시", "대구": "대구광역시", "대전": "대전광역시", "부산": "부산광역시",
    "서울": "서울특별시", "세종시": "세종특별자치시", "울산": "울산광역시", "인천": "인천광역시",
    "전남": "전라남도", "전북": "전라북도", "제주": "제주특별자치도",
    "충남": "충청남도", "충북": "충청북도"
}

def sort_by_location_year_month(folder: str, description: str):
    """다운로드된 엑셀들을 읽어, 지역별로 합쳐 CSV로 저장"""
    buffers = {v: [] for v in LOCATION_MAP.values()}

    for fname in os.listdir(folder):
        if not fname.endswith(".xlsx"):
            continue
        path = os.path.join(folder, fname)
        df = pd.read_excel(path)
        period = fname.rstrip(".xlsx").split("_")[-1]
        df['기준연월'] = period
        df['지역명'] = df['도로명주소'].apply(
            lambda x: LOCATION_MAP[x.split()[0]]
        )
        df.drop(columns=['도로명주소'], inplace=True)

        region = df['지역명'].iloc[0]
        buffers[region].append(df)

    # 병합 후 CSV로 출력
    for region, frames in buffers.items():
        if frames:
            merged = pd.concat(frames, ignore_index=True)
            out_csv = os.path.join(folder, f"{region}_모음_{description}.csv")
            merged.to_csv(out_csv, index=False)
