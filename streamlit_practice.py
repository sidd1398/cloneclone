#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import csv
import pandas as pd

st.cache_data.clear()

# CSV 파일 불러오기 시도
try:
    name_data = pd.read_csv("wooparoo_list_data.csv", encoding="utf-8")
    compressed_data = pd.read_csv("wooparoo_all_data_compressed.csv", encoding="utf-8")
    st.write("Update: 2024-08-10")
    st.write("Made By 시드드#0001")
except Exception as e:
    st.error(f"파일 로드 실패: {e}")
    st.stop()

# 이름을 sno로 변환하는 함수
def name_to_sno(name, name_to_sno_dict):
    return name_to_sno_dict.get(name, None)

# sno를 이름으로 변환하는 함수
def sno_to_name(sno, sno_to_name_dict):
    return sno_to_name_dict.get(sno, "Unknown")

# wooparoo_list_data.csv 파일을 읽어 sno와 name 매핑 생성
name_to_sno_dict = {}
sno_to_name_dict = {}
with open("wooparoo_list_data.csv", "r", encoding="utf-8") as name_file:
    reader = csv.reader(name_file)
    next(reader)  # 헤더 건너뛰기
    for row in reader:
        sno, name = row
        name_to_sno_dict[name] = sno
        sno_to_name_dict[sno] = name

# Streamlit을 사용한 사용자 인터페이스
st.title("우파루 가상 크로스")

left_name = st.text_input("왼쪽 우파루:")
right_name = st.text_input("오른쪽 우파루:")

if st.button("버튼을 누르면 결과창이 출력됩니다."):
    left_sno = name_to_sno(left_name, name_to_sno_dict)
    right_sno = name_to_sno(right_name, name_to_sno_dict)

    if left_sno is None or right_sno is None:
        st.error("입력하신 이름의 우파루가 존재하지 않습니다.")
    else:
        # wooparoo_all_data_sorted.csv 파일에서 [left, right]와 일치하는 [result, rate] 찾기
        with open("wooparoo_all_data_compressed.csv", "r", encoding="utf-8") as sorted_file:
            reader = csv.reader(sorted_file)
            next(reader)  # 헤더 건너뛰기
            
            found = False
            prev_left = None
            prev_right = None
            
            results = []
            
            for row in reader:
                left, right, result, rate = row
                
                # 이전 값을 사용하여 빈 값을 채움
                if left != "":
                    prev_left = left
                else:
                    left = prev_left
                
                if right != "":
                    prev_right = right
                else:
                    right = prev_right
                
                # left와 right가 일치하는지 확인
                if left == left_sno and right == right_sno:
                    result_name = sno_to_name(result, sno_to_name_dict)
                    rate = f"{float(rate):.2f}"  # 소수점 둘째자리까지 확률 표기
                    results.append([result_name, rate])
                    found = True
            
            if found:
                df = pd.DataFrame(results, columns=["결과 우파루", "확률 (%)"])
                df.index = df.index + 1  # 행 번호를 1부터 시작하도록 설정
                st.table(df)
            else:
                st.error(f"파일에 우파루 조합이 존재하지 않습니다. {left_name} (left), {right_name} (right).")


# In[ ]:




