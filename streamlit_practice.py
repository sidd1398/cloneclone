#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd

st.title("가상 크로스 e")

left = st.text_input("왼쪽 우파루:")
right = st.text_input("오른쪽 우파루:")

# pandas를 사용해 csv 파일 읽기
df = pd.read_csv('streamlit.csv')

if st.button("크로스"):
    st.write(df)  # DataFrame 전체를 출력
    st.write('ddd')


# In[ ]:




