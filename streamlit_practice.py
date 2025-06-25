#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
메모할 만한 팁
1. st.table은 그냥 표로 보여준다.
  st.write으로 pandas 데이터(열이름 포함)를 출력하면 사용자가 열이름을 클릭하여 정렬할 수 있는 표로 출력된다.
  st.dataframe도 마찬가지
2. 데이터를 pandas로 읽어들일 때 index는 필요없으면 index_col은 0로 두어 표시되지 않게 하자.
  data = pd.read_csv("wooparoo_list_data.csv", index_col=0)
3. 글자 크기: 기본 텍스트 st.write, st.text는 16px
              (st.write 글씨체가 더 둥글둥글, st.text는 공백 여러 칸 유지 가능)
              st.title은 36px, st.header는 24px, st.subheader는 20px
4. csv 파일의 데이터 읽을 때는 str 타입. 자꾸 int, float으로 생각해서 실수함.
'''

import streamlit as st
import csv
import pandas as pd
import glob

st.cache_data.clear()

#st.write("당분간 가상크로스, 다중조합찾기 모드를 중단합니다 ㅜㅜ")
#st.write(" ")
st.write("안내사항: 6/25 업데이트")
st.write("기준: 유저레벨 30 이상, 우파루 레벨 16 이상")
st.write("Update: 2025-06-25")
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
        # ***** row로 읽어들인 데이터들은 모두 str 취급되는 점 주의 *****
        sno, name, time, prop, attrs = row
        name_to_sno_dict[name] = sno
        sno_to_name_dict[sno] = name
        sno_to_time_dict[sno] = time
        sno_to_prop_dict[sno] = prop

# Streamlit 사용자 인터페이스
st.title("우파루 가상 크로스")

# 선택 박스 설정
#option = st.selectbox(
#    "모드 선택",
#    ["가상 크로스", "크로스 조합 찾기 (단일)", "크로스 조합 찾기 (다중)", "우파루 리스트",
#     "참고 사항", "필요 먹이량 메모", "농장 생산량 메모", "옵션 물약 기댓값 계산"]
#)
option = st.selectbox(
    "모드 선택",
    ["가상 크로스", "크로스 조합 찾기 (단일)", "크로스 조합 찾기 (다중)", "우파루 리스트",
     "참고 사항", "필요 먹이량 메모", "농장 생산량 메모", "옵션 물약 기댓값 계산"]
)

###############################################################################################
###############################################################################################
###############################################################################################
if option == "가상 크로스":
    cross_option = st.radio("크로스 옵션",
                        ("일반크로스", "매직크로스 행운업", "매크행업+이벤트"),
                        index=0)  # index=0은 첫 번째를 기본 선택 옵션으로
    
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
        if cross_option == "일반크로스":
            compressed_file = ["wooparoo_all_data_compressed_part_1.csv", "wooparoo_all_data_compressed_part_2.csv"]
            expected_file = "wooparoo_expected.csv"
            st.write("일반크로스")
        elif cross_option == "매직크로스 행운업":
            compressed_file = ["wooparoo_all_data_compressed_lucky_part_1.csv", "wooparoo_all_data_compressed_lucky_part_2.csv"]
            expected_file = "wooparoo_expected_lucky.csv"
            st.write("매직크로스 행운업")
        elif cross_option == "매크행업+이벤트":
            compressed_file = ["wooparoo_all_data_compressed_event_part_1.csv", "wooparoo_all_data_compressed_event_part_2.csv"]
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
                            st.text(f"1회 크로스 시간 기댓값:  {float(expected_time):.2f}시간")
                            found = True
                            break
                    # 해당 조합이 없는 경우 메시지 출력
                    if not found:
                        st.write("해당 조합에 대한 크로스 시간 기댓값이 없습니다.")
            except Exception as e:
                st.error(f"expected 파일 로드 실패: {e}")

            # 선택된 파일에서 [left, right]와 일치하는 [result, rate] 찾기
            try:
                found = False
                prev_left = None
                prev_right = None
                prev_rate = None
                results = []

                for file_path in compressed_file:
                    with open(file_path, "r", encoding="utf-8") as sorted_file:
                        reader = csv.reader(sorted_file)
                        next(reader)  # 헤더 건너뛰기

                        for row in reader:
                            left, right, result, rate = row

                            # 빈 값 처리 (압축 파일 특성)
                            if left != "":
                                prev_left = left
                            else:
                                left = prev_left
                            if right != "":
                                prev_right = right
                            else:
                                right = prev_right
                            if rate != "":
                                prev_rate = rate
                            else:
                                rate = prev_rate

                            if left == left_sno and right == right_sno:
                                result_prop = sno_to_prop_dict.get(result, "Unknown")
                                show_result = False
                                if result_prop == '9' and checkbox1:
                                    show_result = True
                                elif result_prop in ('6', '7') and checkbox2:
                                    show_result = True
                                elif result_prop in ('3', '13') and checkbox3:
                                    show_result = True
                                elif result_prop == '4' and checkbox4:
                                    show_result = True
                                elif result_prop == '5' and (checkbox3 or checkbox4):
                                    show_result = True
                                elif result_prop not in ('3', '4', '5', '6', '7', '9', '13') and checkbox5:
                                    show_result = True

                                if show_result:
                                    result_name = sno_to_name_dict.get(result, "Unknown")
                                    rate_fmt = f"{float(rate):.2f}"
                                    result_time = round(float(sno_to_time_dict.get(result, "Unknown")), 2)
                                    results.append([result_name, rate_fmt, result_time])
                                    found = True

                if found:
                    if sort_option == '소환시간':
                        results = sorted(results, key=lambda x: x[2], reverse=True)
                    df = pd.DataFrame(results, columns=["결과 우파루", "확률 [%]", "소환시간 [시간]"])
                    df.index = df.index + 1
                    st.table(df.style.format({"소환시간 [시간]": "{:.2f}"}))
                else:
                    st.error(f"파일에 우파루 조합이 존재하지 않습니다: {left_name} (left), {right_name} (right).")

            except Exception as e:
                st.error(f"compressed 파일 로드 실패: {e}")

###############################################################################################
###############################################################################################
###############################################################################################
elif option == "크로스 조합 찾기 (단일)":
    cross_option = st.radio("크로스 옵션",
                        ("일반크로스", "매직크로스 행운업", "매크행업+이벤트"),
                        index=0)  # index=0은 첫 번째를 기본 선택 옵션으로
    
    name_option2 = st.text_input("우파루 이름:")
    if st.button("버튼을 누르면 결과창이 출력됩니다."):
        if cross_option == "일반크로스":
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
        
        # 우파루 이름(name)에 대한 식별코드(sno) 산출
        sno_option2 = name_to_sno_dict.get(name_option2, None)
        if sno_option2 is None:
            st.error("입력한 이름의 우파루가 존재하지 않습니다.")
            
        else:
            # 우파루 이름(name)에 대한 소환시간(time) 산출
            time_option2 = sno_to_time_dict.get(sno_option2, "Unknown")
            hour = float(time_option2) // 1
            minute = round((float(time_option2)-hour) * 60, 0)
            if minute == 0:
                st.write(f"{name_option2} 소환시간 : {int(hour)}시간")
            else:
                st.write(f"{name_option2} 소환시간 : {int(hour)}시간 {float(minute):.0f}분")
            
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
                        st.text("확률 %:    이 조합에서 원하는 우파루가 나올 확률")
                        st.text("cross:     원하는 우파루를 얻기 위해 필요한 \"크로스 횟수\"의 기댓값")
                        st.text("get_time:  원하는 우파루 1마리가 나올 때까지 \"걸리는 시간\"의 기댓값")
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
elif option == "크로스 조합 찾기 (다중)":
    st.subheader("***** 결과값 도출까지 시간이 걸립니다. *****")
    cross_option = st.radio("크로스 옵션",
                        ("일반크로스", "매직크로스 행운업", "매크행업+이벤트"),
                        index=0)  # index=0은 첫 번째를 기본 선택 옵션으로
    name_list = st.text_input("이름 목록 입력:")
    st.write("입력 예시: 홀리, 치우, 레오, 클라우, 아르코")
    st.write("(콤마(comma)를 구분자로 여러 우파루를 동시에 입력하십시오.)")
    
    if st.button("버튼을 누르면 결과창이 출력됩니다."):
        if cross_option == "일반크로스":
            compressed_file = ["wooparoo_all_data_compressed_part_1.csv", "wooparoo_all_data_compressed_part_2.csv"]
            expected_file = "wooparoo_expected.csv"
            st.write("일반크로스")
        elif cross_option == "매직크로스 행운업":
            compressed_file = ["wooparoo_all_data_compressed_lucky_part_1.csv", "wooparoo_all_data_compressed_lucky_part_2.csv"]
            expected_file = "wooparoo_expected_lucky.csv"
            st.write("매직크로스 행운업")
        elif cross_option == "매크행업+이벤트":
            compressed_file = ["wooparoo_all_data_compressed_event_part_1.csv", "wooparoo_all_data_compressed_event_part_2.csv"]
            expected_file = "wooparoo_expected_event.csv"
            st.write("매크행업+이벤트")
        else:
            st.write("cross_option 오류")
            st.stop()
            
        ####################################################################################
        # 1단계: 콤마를 기준으로 이름 목록 쪼개기
        splitted_name = [name.strip() for name in name_list.split(",")]
        
        # name을 sno로 치환하고, 올바르지 않은 이름이 존재할 경우, 알림 후 동작 중단
        splitted_sno = []
        for name in splitted_name:
            value = name_to_sno_dict.get(name, None)
            if value is None:
                st.write(f"'{name}'는 존재하지 않습니다.")
                st.stop()
            splitted_sno.append(value)
        
        ####################################################################################
        # 2단계: compressed_file 열고 splitted_sno에 속한 우파루가 모두 나올 수 있는 조합 찾기
        st.write(name_list)
        st.write("선택된 우파루가 모두 나올 수 있는 조합 검색 중...")
        
        # 최종적으로 [left, right, rate_sum, wooparoo_get_time] 형식
        # 결과를 저장할 배열
        all_pairs = []

        # 이전 행의 데이터를 저장할 변수 (compressed 파일의 빈 칸을 처리하기 위함)
        prev_left, prev_right, prev_rate = None, None, None
        
        # compressed_file을 열어서 한 행씩 검증
        for file_path in compressed_file:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # 헤더 건너뛰기

                # 동일한 [left, right] 조합에서 splitted_sno에 속하는 모든 rate의 합
                rate_sum = 0
                # 동일한 [left, right] 조합의 result 목록은 splitted_sno에 속한 요소를 몇 개나 포함하고 있는지
                result_number = 0
                # 원하던 [left, right] 조합이면 True가 되고, 이번 [left, right] 조합 데이터를 빠르게 넘기기 위한 목적
                passing = False

                # 파일의 각 행을 처리
                for row in reader:
                    # 읽어들인 행에 left, right가 둘 다 빈 칸이면 이전과 동일한 [left, right] 조합임
                    is_empty_data = True
                    # 빈 칸 있으면 이전 행 참조해서 메꾸기
                    if row[0]:
                        left = int(row[0])
                        is_empty_data = False
                    else:
                        left = prev_left
                    if row[1]:
                        right = int(row[1])
                        is_empty_data = False
                    else:
                        right = prev_right
                    result = int(row[2])
                    rate   = float(row[3]) if row[3] else prev_rate

                    prev_left, prev_right, prev_rate = left, right, rate

                    # 새로운 [left, right] 조합을 읽기 시작하면 매개변수 초기화
                    if is_empty_data == False:
                        rate_sum = 0
                        result_number = 0
                        passing = False

                    # splitted_sno는 str 타입의 배열이므로, str() 필수!!
                    if str(result) in splitted_sno:
                        rate_sum += rate
                        result_number += 1

                    # 이번 [left, right] 조합이 splitted_sno를 모두 뽑을 수 있는 조합이라면, 이 조합을 선택
                    if result_number == len(splitted_sno) and passing == False:
                        all_pairs.append([left, right, round(rate_sum, 2)])
                        passing = True
                    if result_number > len(splitted_sno):
                        st.write(f"{left}와 {right} 조합에서 오버플로우 발생")
                        st.stop()
        
        length_of_all_pairs = len(all_pairs)
        if length_of_all_pairs == 0:
            st.write("선택된 우파루가 모두 나올 수 있는 조합이 없습니다.")
            st.stop()
            
        ####################################################################################
        # 3단계: expected_file 열고 각 조합별로 wooparoo_get_time 가져오기
        st.write("각 조합별로 get_time 연산 중...")
        
        # all_pairs의 몇 번째 요소를 찾아볼 것인지 뜻하는 포인터
        # all_pairs와 expected_file 모두 left, right 오름차순이므로, all_pairs의 순서대로 찾는 게 가능
        pointer_of_all_pairs = 0
        # expected_file을 열어서 all_pairs에 expected_time을 추가
        with open(expected_file, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 건너뛰기

            for row in reader:
                left, right, expected_time = row
                # all_pairs의 [left, right] 조합을 expected_file로부터 찾은 경우, expected_time을 추가
                # row로 읽은 건 str이니까 int() 잊지 말기
                if int(left) == all_pairs[pointer_of_all_pairs][0]:
                    if int(right) == all_pairs[pointer_of_all_pairs][1]:
                        # wooparoo_get_time = 1회크로스시간기댓값 * 필요한크로스횟수기댓값
                        # 필요한크로스횟수기댓값 = 100 / rate_sum (rate_sum: 원하는 우파루 하나 등장할 확률)
                        wooparoo_get_time = float(expected_time) * (100 / all_pairs[pointer_of_all_pairs][2])
                        all_pairs[pointer_of_all_pairs].append(round(wooparoo_get_time, 4))
                        pointer_of_all_pairs += 1
                # 찾을 거 다 찾았으면 바로 파일 빠져나오자.
                if pointer_of_all_pairs == length_of_all_pairs:
                    break
            # 현재 all_pairs는 [left, right, rate_sum, wooparoo_get_time]로 완성

        ####################################################################################
        # 4단계: 추천 조합 50가지까지 선정
        st.write("추천 조합 최대 50가지 선정 중...")
        
        # 50가지까지 담고 보여줄 배열. [left, right, rate_sum, cross_times, wooparoo_get_time] 형식
        recommend_pairs = []
        # 현재 recommend_pairs에 담은 [left, right] 조합의 목록들
        # [left, right]와 [right, left] 순서만 뒤바뀐 조합은 둘 중 나은 조합만 남기기에 사용
        used_pairs = set()

        # all_pairs_를 wooparoo_get_time을 기준으로 오름차순, 차순위로 rate_sum으로 내림차순 정렬
        sorted_all_pairs = sorted(all_pairs, key=lambda x: (x[3], -x[2]))

        # 50가지 선정하러 sorted_all_pairs 둘러보기
        for pairs in sorted_all_pairs:
            # left == right인 복사 조합은 패스
            if pairs[0] == pairs[1]:
                continue

            # [left, right]와 [right, left] 순서만 뒤바뀐 조합은 둘 중 나은 조합만 남기기
            if (pairs[0], pairs[1]) in used_pairs or (pairs[1], pairs[0]) in used_pairs:
                continue

            # 적합한 조합이면 recomment_pairs에 저장
            left = sno_to_name_dict.get(str(pairs[0]), "Unknown")
            right = sno_to_name_dict.get(str(pairs[1]), "Unknown")
            recommend_pairs.append([left, right, pairs[2], round(100 / pairs[2], 4), pairs[3]])
                                  # left, right, rate_sum, cross_times, woopparoo_get_time
            used_pairs.add((pairs[0], pairs[1]))

            # 50개까지만 담기
            if len(recommend_pairs) == 50:
                break

        st.text(" ")
        st.text("확률 %:    이 조합에서 원하는 우파루 목록 중 하나라도 나올 확률")
        st.text("cross:     원하는 우파루를 얻기 위해 필요한 \"크로스 횟수\"의 기댓값")
        st.text("get_time:  원하는 우파루 1마리가 나올 때까지 \"걸리는 시간\"의 기댓값")
        df = pd.DataFrame(recommend_pairs, columns=["왼쪽","오른쪽", "확률 %", "cross", "get_time"])
        df.index = df.index + 1  # 행 번호를 1부터 시작하도록 설정
        st.table(df)
        
###############################################################################################
###############################################################################################
###############################################################################################
elif option == "우파루 리스트":
    # CSV 파일을 읽어들임
    # 이래도 index 안 사라지는데?
    data = pd.read_csv('wooparoo_list_data.csv') 
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
    data_to_show.index = data_to_show.index * 0    # 그냥 = 0으로 하면 에러남
    
    # 필터 추가
    checkbox_filter = st.checkbox("필터 열기", value=False)
    
    if checkbox_filter == False:
        # 필터링된 데이터 출력 (index 없이, 열너비 조정)
        st.dataframe(data_to_show, width=800)  # 전체 테이블 너비 조정 가능
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
            data_to_show_filtered = data_to_show[data_to_show['속성'].apply(lambda x: all(f in x for f in filters))]
            #for f in filters:      (이 코드는 필터링이 여러 개일 때 뭔가 이상하게 됨)
            #    data_to_show_filtered = data_to_show[data_to_show['속성'].apply(lambda x: f in x)]
        
            # 필터링된 데이터 출력 (index 없이, 열너비 조정)
            st.dataframe(data_to_show_filtered, width=800)  # 전체 테이블 너비 조정 가능
            
        else:
            st.write("필터를 선택해주세요.")

###############################################################################################
###############################################################################################
###############################################################################################
elif option == "참고 사항":
    st.subheader("--- FAQ ---")
    st.write("Q. 쉐도우는 왜 조합이 없나요?")
    st.write("A. 레이와 쉐도우는 조합이 동일하고 크로스 시간에 따라서만 다르게 등장합니다.")
    st.write(". . 이 사이트의 데이터베이스는 오전 9시를 기준으로 두고 있으므로, 쉐도우의 조합은 레이의 조합으로 검색하시면 됩니다.")
    st.text(" ")
    st.write("Q. 우파루 레벨은 크로스에 어떤 영향을 주나요?")
    st.write("A. 아래, 크로스 참고사항 1번 참조")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.subheader("--- 크로스 참고 사항 ---")
    st.write("1. 양쪽 우파루 모두 10레벨 이상으로 크로스해야 온전한 확률을 얻습니다.")
    st.write("1-1. 우파루 레벨이 10 미만이라면, 한정, 별속성과 같은 고급 우파루의 등장 확률이 낮아집니다.")
    st.write("1-2. 11레벨 이상 우파루끼리 조합 시, 클라우처럼 신성 우파루의 등장 가능성이 생깁니다. 취향에 따라 결정하시면 됩니다.")
    st.write("1-3. 왼쪽 우파루, 오른쪽 우파루 중 레벨이 낮은 우파루가 적용 레벨이 됩니다.")
    st.text(" ")
    st.write("2. 왼쪽 우파루의 유전자(?)를 더 잘 물려받는 경향이 있습니다.")
    st.write("2-1. 대체로 왼쪽 우파루를 크로스 시간이 짧은 우파루(단일속성)으로 배치하면 크로스 시간(기댓값)이 짧아집니다.")    
    st.text(" ")
    st.write("3. 별속성, 3속성, 한정, 레어, 드빌 우파루들은 일반적으로 조합에 관계없이 고정 확률을 지닙니다.")
    st.write("3-1. 한정 3속성은 대체로 3%, 한정 2속성은 5%, 레어 우파루는 4%의 고정확률을 지닙니다.")
    st.write("3-2. 특수 우파루 또한 고정 확률을 지닙니다. (토드 3%, 러브럽 5%, 포기사 5%)")
    st.write("3-3. 단, 조합 결과 상 나올 수 있는 고정 확률 우파루가 너무 많아지면, 전체적으로 확률을 낮춤으로써 총합이 100%가 되도록 유지합니다.")
    st.text(" ")
    st.write("4. 따라서 6속성을 섞는 크로스, 레어 속성 조합을 3가지 이상 포함하는 조합은 대체로 확률 너프를 받습니다.")
    st.write("4-1. 레어 속성 조합: 숲+얼음, 불+얼음, 불+매직, 땅+바람, 물+천둥, 물+슈거")
    st.write("4-2. 행운업을 할 때에는 고정확률의 합 또한 높아지므로, 확률 너프를 받을 가능성이 커집니다.")
    st.text(" ")
    st.write("5. 확률업 이벤트 진행 시에는 매직크로스에만 즉시완료+행운업을 시행하는 것이 훨씬 이득입니다.")
    st.write("5-1. 매직크로스 42시간, 우파루크로스 10시간이더라도, 우파루크로스를 포기하고 매직크로스만 즉시완료로 굴리는 게 확률적으로 이득입니다.")
    st.write("5-2. 하지만 한정을 여러 마리 뽑을 시, 심리적으로는 우파루크로스에도 한정 1마리를 띄우는 게 마음이 편안합니다.")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.subheader("--- 별속성(상시) 소환 조건 ---")
    st.write("레이(2.5%, 36시간):   물 혹은 바람 포함 4속성 이상, 레어 미포함 (9:00 ~ 20:59)")
    st.write("쉐도우(2.5%, 36시간): 물 혹은 바람 포함 4속성 이상, 레어 미포함 (21:00 ~ 08:59)")
    st.write("    (팁: 레이, 쉐도우는 물, 천둥, 바람, 얼음을 모두 섞을 시 확률 2배(5%))")
    st.write("고대신룡(0.6%, 35시간 57분): 16레벨 이상끼리 크로스, 5속성 이상")
    st.write("다크닉스(0.6%, 35시간 57분): 16레벨 이상끼리 크로스, 5속성 이상")
    st.write("골디(1.2%, 48시간):     레어 1마리 포함, 4속성 이상")
    st.write("다크골디(0.7%, 48시간): 레어+레어 (2속성 크로스인 바우+보라도루 추천)")
    st.write("루핀(1.5%, 40시간):     레어 1마리 포함, 4속성 이상")
    st.write("크로노(2%, 42시간):     5속성 이상")
    st.write("클라우(1.2%, 50시간):   11레벨 이상끼리 크로스, 5속성 이상")
    st.write("치우(1.2%, 50시간):     11레벨 이상끼리 크로스, 바람, 얼음 포함 4속성 이상")
    st.write("홀리(1.2%, 50시간):     11레벨 이상끼리 크로스, 물, 천둥 포함 4속성 이상")
    st.write("레오(1%, 51시간):       16레벨 이상끼리 크로스, 레어 1마리 포함, 4속성 이상")
    st.write("아르코(1%, 52시간):     16레벨 이상끼리 크로스, 물 포함 5속성 이상")
    st.write("루루(1.5%, 40시간 15분): 불, 바람, 매직 포함 4속성 이상")
    st.text(" ")
    st.write("신성 5종을 모두 노리려면?")
    st.write("16레벨 이상끼리 크로스, 물, 천둥, 바람, 얼음 포함 5속성 크로스")
    st.write("(6속성 크로스할 경우에는 확률 너프 감수)")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.subheader("--- 특수 우파루 소환 조건 ---")
    st.write("러브럽(5%, 10시간 30분): 초코럽 + 코코럽 조합에서만")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.subheader("--- 신성 진화에 필요한 마법석 개수 ---")
    st.write("(순서대로 숲, 땅, 불, 얼음, 번개, 물, 바람, 매직, 별 마법석 개수)")
    st.text("빛:     홀리 -> 세인트 -> 엔젤")
    st.text("세인트: 1, 1, 1, 1, 1, 1, 1, 1, 1")
    st.text("엔젤:   1, 1, 2, 2, 3, 2, 2, 1, 2")
    st.text(" ")
    st.text("어둠:   치우 -> 아수라 -> 라푼타")
    st.text("아수라: 1, 1, 1, 1, 1, 1, 1, 1, 1")
    st.text("라푼타: 1, 2, 2, 3, 2, 2, 1, 1, 2")
    st.text(" ")
    st.text("황금:     레오 -> 발리언트 -> 마르스")
    st.text("발리언트: 1, 1, 1, 1, 1, 1, 1, 1, 1")
    st.text("마르스:   1, 1, 1, 2, 3, 2, 2, 1, 3")
    st.text(" ")
    st.text("구름:     클라우 -> 미스틱 -> 매그너스")
    st.text("미스틱:   1, 1, 1, 1, 1, 1, 1, 1, 1")
    st.text("매그너스: 3, 2, 2, 2, 2, 1, 1, 1, 2")
    st.text(" ")
    st.text("무지개: 아르코 -> 이리스 -> 미라쥬")
    st.text("이리스: 1, 1, 1, 1, 1, 1, 1, 1, 1")
    st.text("미라쥬: 1, 1, 1, 2, 2, 2, 2, 2, 3")
    st.text(" ")
    st.write("아트모스: 매그너스, 라푼타, 마르스, 미라쥬, 엔젤 보유 시 소환 가능")
    st.text("필요 마법석: 3, 3, 3, 3, 3, 2, 2, 2, 4")
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.subheader("--- 루루 마법 진화에서의 마법석 ---")
    st.write("기본 진화확률: 10%")
    st.write("진화 성공 시 등장 확률: 실비아 3%, 루나실 3%, 미쉘 3%, 네로: 91%")
    st.write("마법석을 주어 진화확률이 최소 30% 이상이 되어야 진화 시도가 가능합니다.")
    st.write("(네로는 진화 성공체 중에서도 실패작이라 생각하시면 편합니다.)")
    st.text(" ")
    st.write("숲, 땅, 불, 얼음, 번개, 물, 바람, 매직 마법석을 주면 수당: 진화확률 +3%")
    st.write("별 마법석 1개를 주면: 진화확률 +15%")
    st.write("검은 마법석 1개를 주면: 진화확률 +15%")
    st.write("불 마법석 1개를 주면, 진화 선공 시 등장 확률이 실비아 +3%, 네로 -3%")
    st.write("바람 마법석 1개를 주면, 진화 선공 시 확률이 루나실 +3%, 네로 -3%")
    st.write("매직 마법석 1개를 주면, 진화 선공 시 확률이 미쉘 +3%, 네로 -3%")
    st.write("검은 마법석 1개를 주면, 진화 선공 시 확률이 실비아 +5%, 루나실 +5%, 미쉘 +5%, 네로 -15%")
    st.text(" ")
    st.write("(마법석은 하루에 3개까지만 투입 가능)")
    st.write("불 마법석 30개 지급: 진화확률 100%")
    st.write("=> 실비아 93%, 루나실 3%, 미쉘 3%, 네로 1%")
    st.write("바람 마법석 30개 지급: 진화확률 100%")
    st.write("=> 실비아 3%, 루나실 93%, 미쉘 3%, 네로 1%")
    st.write("매직 마법석 30개 지급: 진화확률 100%")
    st.write("=> 실비아 3%, 루나실 3%, 미쉘 93%, 네로 1%")
    st.write("검은 마법석 6개 지급: 진화확률 100%")
    st.write("=> 실비아 33%, 루나실 33%, 미쉘 33%, 네로 1%")
    st.text(" ")
    st.write("등장 확률이 음수가 되면 0%로 조정.")
    st.write("등장 확률 합이 100%를 초과하면 비중대로 부여하여 100%로 맞춤")
    st.write("예: 불 마법석 30개 지급 후 검은 마법석 1개를 주면,")
    st.write(". .  실비아 93% -> 98%, 루나실 3% -> 8%, 미쉘 3% -> 8%, 네로 1% -> -14%")
    st.write(". .  네로는 -14% -> 0%로 조정")
    st.write(". .  실비아는 98% -> 98/(98+8+8) = 86%로 조정")
    st.write(". .  루나실과 미쉘은 8% -> 8/(98+8+8) = 7%로 조정")
    
###############################################################################################
###############################################################################################
###############################################################################################
elif option == "필요 먹이량 메모":
    feed_option = st.radio("우파루 종류",
                        ("일반 우파루", "별속성 우파루", "1차 신성진화 우파루", "2차 신성진화 우파루"),
                        index=0)  # index=0은 첫 번째를 기본 선택 옵션으로
    if feed_option == "일반 우파루":
        weight = 1
    elif feed_option == "별속성 우파루":
        weight = 2
    elif feed_option == "1차 신성진화 우파루":
        weight = 20
    elif feed_option == "2차 신성진화 우파루":
        weight = 30
    else:
        st.write("feed_option 에러")
        
    # 우파루 먹이량은 wooparoo_feed.csv 파일 안에
    feed_data = pd.read_csv("wooparoo_feed.csv", header=None)
    
    # csv 파일의 열 개수 보기
    # st.write(feed_data.shape[1])
    # csv 파일의 2, 3, 4열은 기본 먹이량이므로, weight을 곱해주자.
    feed_data.iloc[:, 1:] = feed_data.iloc[:, 1:] * weight
    
    # 머리말 정의
    header = ['레벨', '1회 먹이량', '4회 먹이량', '누적 먹이량']
    # 머리말을 추가하여 새로운 데이터프레임 생성
    feed_data.columns = header
    
    # 아래는 왼쪽 정렬로 보여줄 때의 코드
    # 3자리 단위로 콤마 추가
    #comma_feed_data = feed_data.applymap(lambda x: f"{int(x):,}"
    #                                     if isinstance(x, (int, float))
    #                                     else x)
    #comma_feed_data.index = comma_feed_data.index + 1
    #st.dataframe(comma_feed_data)

    # 아래는 오른쪽 정렬로 보여줄 때의 코드
    # streamlit은 글자는 왼쪽 정렬, 숫자는 오른쪽 정렬로 고정. 변경 불가능한 듯
    # 데이터프레임 스타일링
    feed_data.index = feed_data.index + 1
    styled_feed_data = feed_data.style.format({
        # 3자리마다 콤마(comma)로 끊어서 보여주기
        '1회 먹이량': '{:,}',
        '4회 먹이량': '{:,}',
        '누적 먹이량': '{:,}'
    }).set_properties(**{
        'text-align': 'right'  # 모든 셀의 텍스트를 오른쪽 정렬
    }).set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'right')]}  # 헤더도 오른쪽 정렬
    ])
    st.dataframe(styled_feed_data, width=400)
    
    st.text(" ")
    st.text(f"1  -> 10레벨:    {feed_data.iloc[9, 3]:,}")
    st.text(f"10 -> 15레벨:    {feed_data.iloc[14, 3] - feed_data.iloc[9, 3]:,}")
    st.text(f"1  -> 15레벨:    {feed_data.iloc[14, 3]:,}")
    st.text(" ")
    st.text(f"15 -> 20레벨:    {feed_data.iloc[19, 3] - feed_data.iloc[14, 3]:,}")
    st.text(f"10 -> 20레벨:    {feed_data.iloc[19, 3] - feed_data.iloc[9, 3]:,}")
    st.text(f"1  -> 20레벨:    {feed_data.iloc[19, 3]:,}")
    st.text(" ")
    st.text(f"20 -> 25레벨:    {feed_data.iloc[24, 3] - feed_data.iloc[19, 3]:,}")
    st.text(f"25 -> 30레벨:    {feed_data.iloc[29, 3] - feed_data.iloc[24, 3]:,}")
    st.text(f"20 -> 30레벨:    {feed_data.iloc[29, 3] - feed_data.iloc[19, 3]:,}")
    st.text(f"1  -> 30레벨:    {feed_data.iloc[29, 3]:,}")
    st.text(" ")
    st.text(f"30 -> 35레벨:    {feed_data.iloc[34, 3] - feed_data.iloc[29, 3]:,}")
    st.text(f"35 -> 40레벨:    {feed_data.iloc[39, 3] - feed_data.iloc[34, 3]:,}")
    st.text(f"30 -> 40레벨:    {feed_data.iloc[39, 3] - feed_data.iloc[29, 3]:,}")
    st.text(f"1  -> 40레벨:    {feed_data.iloc[39, 3]:,}")
    st.text(" ")
    st.text(f"40 -> 45레벨:    {feed_data.iloc[44, 3] - feed_data.iloc[39, 3]:,}")
    st.text(f"1  -> 45레벨:    {feed_data.iloc[44, 3]:,}")

###############################################################################################
###############################################################################################
###############################################################################################
elif option == "농장 생산량 메모":
    farm_data = [
        ['이름', '먹이량', '경험치', '마나볼', '시간'],
        [' ', ' ', '1먹이당마나볼', '1경험치당마나볼', '시간당먹이량'],
        [' ', ' ', ' ', ' ', ' '],
        ['친구의 딸기', '25', '30', '40', '5분'],
        [' ', ' ', '1.6', '1.33', '300'],
        [' ', ' ', ' ', ' ', ' '],
        ['딸기', '10', '30', '55', '1분'],
        [' ', ' ', '5.5', '1.83', '600'],
        [' ', ' ', ' ', ' ', ' '],
        ['버섯', '25', '250', '275', '5분'],
        [' ', ' ', '11', '1.1', '300'],
        [' ', ' ', ' ', ' ', ' '],
        ['오렌지', '90', '1,400', '1,100', '30분'],
        [' ', ' ', '12.22', '0.79', '180'],
        [' ', ' ', ' ', ' ', ' '],
        ['친구의 포도', '500', '7,000', '3,500', '5분'],
        [' ', ' ', '7', '0.5', '6,000'],
        [' ', ' ', ' ', ' ', ' '],
        ['포도', '400', '7,000', '5,000', '2시간'],
        [' ', ' ', '12.5', '0.71', '200'],
        [' ', ' ', ' ', ' ', ' '],
        ['옥수수', '900', '20,000', '15,000', '6시간'],
        [' ', ' ', '16.67', '0.75', '150'],
        [' ', ' ', ' ', ' ', ' '],
        ['보리', '3,300', '90,000', '80,000', '24시간'],
        [' ', ' ', '24.24', '0.89', '137.5'],
        [' ', ' ', ' ', ' ', ' '],
        ['친구의 선두', '5,000', '100,000' ,'140,000', '5분'],
        [' ', ' ', '28', '1.4', '60,000'],
        [' ', ' ', ' ', ' ', ' '],
        ['선두', '8,800', '100,000', '220,000', '2시간'],
        [' ', ' ', '25', '2.2', '4,400'],
        [' ', ' ', ' ', ' ', ' '],
        ['밀', '33,000', '500,000', '1,100,000', '6시간'],
        [' ', ' ', '33.33', '2.2', '5,500'],
        [' ', ' ', ' ', ' ', ' '],
        ['신비의 꽃', '440,000', '3,000,000', '15,000,000', '24시간'],
        [' ', ' ', '34.09', '5', '18,333'],
        [' ', ' ', ' ', ' ', ' '],
        ['축복의 꽃', '500,000', '3,500,000', '25,000,000', '1시간'],
        [' ', ' ', '50', '7.14', '500,000'],
        [' ', ' ', ' ', ' ', ' '],
        ['루파의 물약', '750물약', '3,000,000', '15,000,000', '6시간'],
        ['먹이 말고', '물약!', '20,000', '5', '125']
    ]
    
    framed_farm_data = pd.DataFrame(farm_data[1:], columns=farm_data[0])
    # streamlit dataframe은 글자는 좌측정렬, 숫자는 우측정렬, 이걸 바꿀 수는 없음
    #styled_farm_data = framed_farm_data.style.set_properties(**{'text-align': 'right'})
    
    st.dataframe(framed_farm_data, width=550)
    
###############################################################################################
###############################################################################################
###############################################################################################
elif option == "옵션 물약 기댓값 계산":    
    # 옵션별 등장 확률
    promotion_option_data = [
        7.5, 7.5, 20, 20,
        1.55, 1.55, 1.45, 1.45, 1.45, 1.45, 1.45, 1.35, 1.35, 1.35, 1.45, 1.35, 1.35, 1.45,
        5, 20
    ]
    
    # 우파루 별 개수
    wooparoo_stars_input = st.radio("우파루의 별 개수를 선택하세요.",
                        ("1성", "2성", "3성", "4성", "5성"),
                        index=4)
    if wooparoo_stars_input == "1성":
        roulette_number = 1
    elif wooparoo_stars_input == "2성":
        roulette_number = 2
    elif wooparoo_stars_input == "3성":
        roulette_number = 3
    elif wooparoo_stars_input == "4성":
        roulette_number = 4
    elif wooparoo_stars_input == "5성":
        roulette_number = 5
    
    # 잠금별 소모 비용
    promotion_cost_input = st.radio("옵션 잠금 개수를 선택하세요.",
                        ("0개 (5물약)", "1개 (10물약)", "2개 (20물약)", "3개 (40물약)", "4개 (80물약)"),
                        index=0)  # index=0은 첫 번째를 기본 선택 옵션으로
    if promotion_cost_input == "0개 (5물약)":
        locked_roulette = 0
        promotion_cost = 5
    elif promotion_cost_input == "1개 (10물약)":
        locked_roulette = 1
        promotion_cost = 10
    elif promotion_cost_input == "2개 (20물약)":
        locked_roulette = 2
        promotion_cost = 20
    elif promotion_cost_input == "3개 (40물약)":
        locked_roulette = 3
        promotion_cost = 40
    elif promotion_cost_input == "4개 (80물약)":
        locked_roulette = 4
        promotion_cost = 80

    # 등급별 등장 확률
    # promotion_level_data = [0.5, 1.5, 3, 10, 20, 30, 35]
    promotion_level_option = st.radio("원하는 등급을 선택하세요.",
                        ("S", "A 이상", "B 이상", "C 이상", "D 이상", "E 이상", "F 이상"),
                        index=0)
    if promotion_level_option == "S":
        promotion_level_data = 0.5
    elif promotion_level_option == "A 이상":
        promotion_level_data = 2
    elif promotion_level_option == "B 이상":
        promotion_level_data = 5
    elif promotion_level_option == "C 이상":
        promotion_level_data = 15
    elif promotion_level_option == "D 이상":
        promotion_level_data = 35
    elif promotion_level_option == "E 이상":
        promotion_level_data = 65
    elif promotion_level_option == "F 이상":
        promotion_level_data = 100
    
    st.write("원하는 옵션들을 체크하세요.")
    st.write("(또는 조건으로 적용됩니다.)")
    checkbox1 = st.checkbox('공격력%: 7.5%', value=True)
    checkbox2 = st.checkbox('생명력%: 7.5%', value=True)
    checkbox3 = st.checkbox('공격력: 20%', value=False)
    checkbox4 = st.checkbox('생명력: 20%', value=False)
    checkbox5 = st.checkbox('숲 스킬 파워: 1.55%', value=False)
    checkbox6 = st.checkbox('땅 스킬 파워: 1.55%', value=False)
    checkbox7 = st.checkbox('불 스킬 파워: 1.45%', value=False)
    checkbox8 = st.checkbox('얼음 스킬 파워: 1.45%', value=False)
    checkbox9 = st.checkbox('천둥 스킬 파워: 1.45%', value=False)
    checkbox10 = st.checkbox('물 스킬 파워: 1.45%', value=False)
    checkbox11 = st.checkbox('바람 스킬 파워: 1.45%', value=False)
    checkbox12 = st.checkbox('빛 스킬 파워: 1.35%', value=False)
    checkbox13 = st.checkbox('어둠 스킬 파워: 1.35%', value=False)
    checkbox14 = st.checkbox('황금 스킬 파워: 1.35%', value=False)
    checkbox15 = st.checkbox('매직 스킬 파워: 1.45%', value=False)
    checkbox16 = st.checkbox('구름 스킬 파워: 1.35%', value=False)
    checkbox17 = st.checkbox('무지개 스킬 파워: 1.35%', value=False)
    checkbox18 = st.checkbox('슈거 스킬 파워: 1.45%', value=False)
    checkbox19 = st.checkbox('피해 감소%: 5%', value=False)
    checkbox20 = st.checkbox('마나볼 생산량%: 20%', value=False)
    
    option_list = [
        checkbox1, checkbox2, checkbox3, checkbox4, checkbox5,
        checkbox6, checkbox7, checkbox8, checkbox9, checkbox10,
        checkbox11, checkbox12, checkbox13, checkbox14, checkbox15,
        checkbox16, checkbox17, checkbox18, checkbox19, checkbox20
    ]
    
    sum_of_option = 0
    for i in range(20):
        sum_of_option += promotion_option_data[i] * option_list[i]
    
    st.text(" ")
    if sum_of_option == 0:
        st.header("옵션을 선택해주세요.")
    elif (roulette_number - locked_roulette) == 0:
        st.subheader("우파루의 모든 옵션이 잠금 설정 되었습니다.")
    elif (roulette_number - locked_roulette) < 0:
        st.subheader("우파루가 가진 옵션 개수보다 많은 옵션이 잠금 설정 되었습니다.")
    else:
        cost_expectation = (promotion_cost / (roulette_number - locked_roulette) * 
                            (100 / promotion_level_data) * (100 / sum_of_option))
        formatted_expectation = f"{int(round(cost_expectation, 0)):,}"
        st.header(f"기댓값 : {formatted_expectation}")
    
    st.text(" ")
    st.text("################################")
    st.write("--- 승급 필요 물약 ---")
    st.text("0성 -> 1성:    100")
    st.text("1성 -> 2성:  1,000")
    st.text("2성 -> 3성:  5,000")
    st.text("3성 -> 4성: 15,000")
    st.text("4성 -> 5성: 30,000")
    st.text(" ")
    st.write("--- 기댓값 계산 공식 ---")
    st.write("기댓값 = (1회당 물약 개수) / (우파루 별 개수 - 스킬 잠금 개수) * (100 / 등급 등장 확률[%]) * (100 / 옵션특성 등장 확률 합[%])")
    st.text(" ")
    st.write("--- 등급 등장 확률 ---")
    st.write("S등급: 0.5%")
    st.write("A등급: 1.5%, A등급 이상: 2%")
    st.write("B등급: 3%, B등급 이상: 5%")
    st.write("C등급: 10%, C등급 이상: 15%")
    st.write("D등급: 20%, D등급 이상: 35%")
    st.write("E등급: 30%, E등급 이상: 65%")
    st.write("F등급: 35%, F등급 이상: 100%")


# In[ ]:




