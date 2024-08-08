#!/usr/bin/env python
# coding: utf-8

# In[2]:


'''
import json
import streamlit as st
import pandas as pd

# JSON 파일을 읽어옵니다.
with open('sorted_wooparoo_all_data.json', 'r', encoding='utf-8') as file:
    sorted_data = json.load(file)

# 애플리케이션 제목
st.title("가상 크로스")

# 사용자 입력 받기
left = st.text_input("왼쪽 우파루:")
right = st.text_input("오른쪽 우파루:")


# 버튼을 눌렀을 때 실행되는 코드
if st.button("Submit"):
    # 일치하는 url_index를 찾고, 해당 data를 출력합니다.
    found = False
    for item in sorted_data:
        if item['url_index'] == input_array:
            found = True
            #st.write(f"왼쪽 우파루: {input_array[0]}, 오른쪽 우파루: {input_array[1]}")                
            break

    if not found:
        print(f"입력한 이름의 우파루가 없습니다: {input_array}")
    else:
        # pandas DataFrame으로 변환하고 열 이름 설정
        df = pd.DataFrame(item['data'], columns=["결과 우파루", "확률(%)"])
        df.index = df.index + 1
        print(df)
'''
print(" ", end='')


# In[2]:


'''
import csv
f = open('streamlit.csv', 'w')
data = [['가나다라','12345'],['마바사아','678910']]
writer = csv.writer(f)
writer.writerows(data)
f.close()
'''
print(" ", end='')


# In[3]:


'''
f = open('streamlit.csv', 'r')
data = csv.reader(f)
for line in data:
    print(line)
f.close()
'''
print(" ", end='')


# In[ ]:


import streamlit as st
import csv

st.title("가상 크로스")

left = st.text_input("왼쪽 우파루:")
right = st.text_input("오른쪽 우파루:")

f = open('streamlit.csv', 'r')
data = csv.reader(f)

if st.button("Submit"):
    st.write(data)
#    st.write(data[1])

