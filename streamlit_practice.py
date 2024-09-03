#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import csv
import pandas as pd

st.cache_data.clear()

st.write("안내사항: 확업이벤트 확률은 이벤트 당일에 나옵니다.")
st.write("Update: 2024-08-28")
st.write("Made by 시드드#0001")
st.write("Thanks to kjeok00, replica, yskunn")

# wooparoo_list_data.csv 파일을 읽어 sno, name, time, prop 매핑 생성
name_to_sno_dict = {}
sno_to_name_dict = {}
sno_to_time_dict = {}
sno_to_prop_dict = {}
with open("wooparoo_list_data.csv", "r", encoding="utf-8") as name_file:
    reader = csv.reader(name_file)
    next(reader)  # 헤더 건너뛰기 -> 필수!!
    for row in reader:
        sno, name, time, prop, attrs = row
        name_to_sno_dict[name] = sno
        sno_to_name_dict[sno] = name
        sno_to_time_dict[sno] = time
        sno_to_prop_dict[sno] = prop

# Streamlit 사용자 인터페이스
st.title("우파루 가상 크로스")

# 선택 박스 설정
option = st.selectbox(
    "모드 선택",
    ["가상 크로스", "우파루 조합 찾기", "우파루 정보 보기"]
)
cross_option = st.radio('크로스 옵션',
                        ('일반크로스', '매직크로스 행운업', '매크행업+이벤트'),
                        index=0)  # index=0은 첫 번째를 기본 선택 옵션으로
###############################################################################################
###############################################################################################
###############################################################################################
if option == "가상 크로스":
    sort_option = st.radio('정렬 기준', ('확률', '소환시간'), index=0)
    left_name = st.text_input("왼쪽 우파루:")
    right_name = st.text_input("오른쪽 우파루:")
    checkbox1 = st.checkbox('별속성 보기', value=True)
    checkbox2 = st.checkbox('한정 보기', value=True)
    checkbox3 = st.checkbox('상시 3속성 보기', value=True)
    checkbox4 = st.checkbox('레어 보기', value=True)
    checkbox5 = st.checkbox('기타 등등 보기', value=True)

    if st.button("버튼을 누르면 결과창이 출력됩니다."):
        # 옵션에 따라 파일 선택
        if cross_option == '일반크로스':
            compressed_file = "wooparoo_all_data_compressed.csv"
            expected_file = "wooparoo_expected.csv"
            st.write("일반크로스")
        elif cross_option == "매직크로스 행운업":
            compressed_file = "wooparoo_all_data_compressed_lucky.csv"
            expected_file = "wooparoo_expected_lucky.csv"
            st.write("매직크로스 행운업")
        elif cross_option == "매크행업+이벤트":
            compressed_file = "wooparoo_all_data_compressed_event.csv"
            expected_file = "wooparoo_expected_event.csv"
            st.write("매크행업+이벤트")
        else:
            st.write("cross_option 오류")
            st.stop()

        st.write(f"{left_name} + {right_name}")

        left_sno = name_to_sno_dict.get(left_name, None)
        right_sno = name_to_sno_dict.get(right_name, None)

        if left_sno is None or right_sno is None:
            st.error("입력한 이름의 우파루가 존재하지 않습니다.")
        else:
            # [left, right]에 해당하는 expected_time(크로스 소환 시간 기댓값)을 출력하기
            try:
                with open(expected_file, 'r', encoding='utf-8') as sorted_file:
                    reader = csv.reader(sorted_file)
                    next(reader)  # 헤더 건너뛰기
                    found = False

                    # CSV 파일의 각 행(row)을 순회
                    for row in reader:
                        left, right, expected_time = row

                        # left_name과 right_name이 일치하는지 확인
                        if left == left_sno and right == right_sno:
                            st.write(f"1회 크로스 시간 기댓값: {float(expected_time):.2f}시간")
                            found = True
                            break
                    # 해당 조합이 없는 경우 메시지 출력
                    if not found:
                        st.write("해당 조합에 대한 크로스 시간 기댓값이 없습니다.")
            except Exception as e:
                st.error(f"expected 파일 로드 실패: {e}")

            # 선택된 파일에서 [left, right]와 일치하는 [result, rate] 찾기
            try:
                with open(compressed_file, "r", encoding="utf-8") as sorted_file:
                    reader = csv.reader(sorted_file)
                    next(reader)  # 헤더 건너뛰기

                    found = False
                    prev_left = None
                    prev_right = None

                    results = []

                    for row in reader:
                        left, right, result, rate = row

                        # 이전 값을 사용하여 빈 값을 채움 (compressed 버전 파일이라 필요)
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
                            # 우파루 구분(prop)에 따라 보여줄지 말지 결정
                            result_prop = sno_to_prop_dict.get(result, "Unknown")
                            show_result = False
                            if result_prop == '9':
                                if checkbox1 == True:
                                    show_result = True
                            elif result_prop == '6' or result_prop == '7':
                                if checkbox2 == True:
                                    show_result = True
                            elif result_prop == '3' or result_prop == '13':
                                if checkbox3 == True:
                                    show_result = True
                            elif result_prop == '4':
                                if checkbox4 == True:
                                    show_result = True
                            elif result_prop == '5':
                                if checkbox3 == True or checkbox4 == True:
                                    show_result = True
                            else:
                                if checkbox5 == True:
                                    show_result = True

                            # 보여줄 데이터라면 표에 추가하기
                            if show_result:
                                result_name = sno_to_name_dict.get(result, "Unknown")
                                rate = f"{float(rate):.2f}"  # 소수점 둘째자리까지 확률 표기
                                result_time = round(float(sno_to_time_dict.get(result, "Unknown")), 2)
                                results.append([result_name, rate, result_time])
                                found = True

                    if found:
                        if sort_option == '소환시간':
                            # result_time을 기준으로 내림차순 정렬
                            results = sorted(results, key=lambda x: x[2], reverse=True)
                        df = pd.DataFrame(results, columns=["결과 우파루", "확률 [%]", "소환시간 [시간]"]) 
                        df.index = df.index + 1  # 행 번호를 1부터 시작하도록 설정
                        # 표 출력 (float_format 적용 -> 소수점 둘째자리까지만 표기되도록)
                        st.table(df.style.format({"소환시간 [시간]": "{:.2f}"}))
                    else:
                        st.error(f"파일에 우파루 조합이 존재하지 않습니다.                                 {left_name} (left), {right_name} (right).")
            except Exception as e:
                st.error(f"compressed 파일 로드 실패: {e}")
###############################################################################################
###############################################################################################
###############################################################################################
elif option == "우파루 조합 찾기":
    name_option2 = st.text_input("우파루 이름:")
    if st.button("버튼을 누르면 결과창이 출력됩니다."):
        # 옵션에 따라 파일 선택
        if cross_option == '일반크로스':
            finding_file = "finding_combination.csv"
            st.write("일반크로스")
        elif cross_option == "매직크로스 행운업":
            finding_file = "finding_combination_lucky.csv"
            st.write("매직크로스 행운업")
        elif cross_option == "매크행업+이벤트":
            finding_file = "finding_combination_event.csv"
            st.write("매크행업+이벤트")
        else:
            st.write("cross_option 오류")
            st.stop()
        
        # 우파루 이름(name)에 대한 식별코드(sno)와 소환시간(time) 산출
        sno_option2 = name_to_sno_dict.get(name_option2, None)
        time_option2 = sno_to_time_dict.get(sno_option2, "Unknown")
        hour = float(time_option2) // 1
        minute = round((float(time_option2)-hour) * 60, 0)
        if minute == 0:
            st.write(f"{name_option2} 소환시간 : {int(hour)}시간")
        else:
            st.write(f"{name_option2} 소환시간 : {int(hour)}시간 {float(minute):.0f}분")
            
        if sno_option2 is None:
            st.error("입력한 이름의 우파루가 존재하지 않습니다.")
        else:
            # [left, right]에 해당하는 expected_time을 출력하기
            try:
                with open(finding_file, 'r', encoding='utf-8') as find_file:
                    reader = csv.reader(find_file)
                    next(reader)  # 헤더 건너뛰기
                    found = False
                    
                    results = []

                    # CSV 파일의 각 행(row)을 순회
                    for row in reader:
                        result, left, right, rate, cross_times, wooparoo_get_time = row

                        # result(크로스 결과 우파루)와 sno_option2(사용자 입력 우파루)이 일치하는지 확인
                        if result == sno_option2:
                            left_n = sno_to_name_dict.get(left, "Unknown")
                            right_n = sno_to_name_dict.get(right, "Unknown")
                            results.append([left_n, right_n, rate,                                            round(float(cross_times), 2),                                            round(float(wooparoo_get_time), 2)])
                            found = True
                    
                    if found:
                        st.write("확률 %:    이 조합에서 원하는 우파루가 나올 확률")
                        st.write("cross:    원하는 우파루를 얻기 위해 필요한 \"크로스 횟수\"의 기댓값")
                        st.write("get_time:    원하는 우파루 1마리가 나올 때까지 \"걸리는 시간\"의 기댓값")
                        df = pd.DataFrame(results, columns=["왼쪽","오른쪽", "확률 %", "cross", "get_time"])
                        df.index = df.index + 1  # 행 번호를 1부터 시작하도록 설정
                        st.table(df)
                    else:
                        st.write("해당 우파루에 대한 추천 조합이 없습니다.")
            except Exception as e:
                st.error(f"finding combination 파일 로드 실패: {e}")
###############################################################################################
###############################################################################################
###############################################################################################
elif option == "우파루 정보 보기":
    # CSV 파일을 읽어들임
    data = pd.read_csv("wooparoo_list_data.csv")
    # 'time'을 기준으로 오름차순 정렬
    data = data.sort_values(by='time')
    
    # 시간 형식을 "n시간" 또는 "n시간 m분"으로 변환
    data['formatted_time'] = data['time'].apply(lambda t: f"{int(t)}시간" 
                                                if int((t - int(t)) * 60) == 0 
                                                else f"{int(t)}시간 {int((t - int(t)) * 60)}분") 
    # attrs의 숫자를 대응하는 글자 속성으로 변환
    attr_mapping = {1: "숲", 2: "땅", 3: "불", 4: "얼음", 5: "천둥", 6: "물", 7: "바람", 
                    8: "빛", 9: "어둠", 10: "황금", 11: "보석", 12: "매직", 
                    13: "구름", 14: "무지개", 15: "슈거"}
    data['formatted_attrs'] = data['attrs'].apply(lambda x: [attr_mapping[i] for i in eval(x)])

    # 필요한 데이터만 선택
    data_to_show = data[['name', 'formatted_time', 'formatted_attrs']]
    data_to_show.columns = ['이름', '소환시간', '속성']
    
    # 필터 추가
    checkbox_filter = st.checkbox("필터 열기", value=False)
    
    if checkbox_filter == False:
        st.write(data_to_show)
    else:
        # 필터 체크박스
        checkbox_filter1 = st.checkbox("숲", value=False)
        checkbox_filter2 = st.checkbox("땅", value=False)
        checkbox_filter3 = st.checkbox("불", value=False)
        checkbox_filter4 = st.checkbox("얼음", value=False)
        checkbox_filter5 = st.checkbox("천둥", value=False)
        checkbox_filter6 = st.checkbox("물", value=False)
        checkbox_filter7 = st.checkbox("바람", value=False)
        checkbox_filter12 = st.checkbox("매직", value=False)
        checkbox_filter13 = st.checkbox("슈거", value=False)
        checkbox_filter8 = st.checkbox("빛", value=False)
        checkbox_filter9 = st.checkbox("어둠", value=False)
        checkbox_filter10 = st.checkbox("황금", value=False)
        checkbox_filter14 = st.checkbox("구름", value=False)
        checkbox_filter15 = st.checkbox("무지개", value=False)

        # 필터링 조건 생성
        filters = []
        if checkbox_filter1:
            filters.append("숲")
        if checkbox_filter2:
            filters.append("땅")
        if checkbox_filter3:
            filters.append("불")
        if checkbox_filter4:
            filters.append("얼음")
        if checkbox_filter5:
            filters.append("천둥")
        if checkbox_filter6:
            filters.append("물")
        if checkbox_filter7:
            filters.append("바람")
        if checkbox_filter8:
            filters.append("빛")
        if checkbox_filter9:
            filters.append("어둠")
        if checkbox_filter10:
            filters.append("황금")
        if checkbox_filter12:
            filters.append("매직")
        if checkbox_filter13:
            filters.append("슈거")
        if checkbox_filter14:
            filters.append("구름")
        if checkbox_filter15:
            filters.append("무지개")

        # 필터 적용
        if filters:
            for f in filters:
                data_to_show_filtered = data_to_show[data_to_show['속성'].apply(lambda x: f in x)]
            
        # 필터링된 데이터 출력
        st.write(data_to_show_filtered)


# In[ ]:




