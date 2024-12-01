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
'''

import streamlit as st
import csv
import pandas as pd

st.cache_data.clear()

st.write("안내사항: 플로리 업데이트")
st.write("Update: 2024-11-27")
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
    ["가상 크로스", "우파루 조합 찾기", "우파루 리스트", "소환 조건 메모", "필요 먹이량 메모"]
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
    cross_option = st.radio("크로스 옵션",
                        ("일반크로스", "매직크로스 행운업", "매크행업+이벤트"),
                        index=0)  # index=0은 첫 번째를 기본 선택 옵션으로
    
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
elif option == "소환 조건 메모":
    st.write("--- 크로스 참고 사항 ---")
    st.write("1. 양쪽 우파루 모두 10레벨 이상으로 크로스해야 온전한 확률을 얻습니다.")
    st.write("1-1. 우파루 레벨이 10 미만이라면, 한정, 별속성과 같은 고급 우파루의 등장 확률이 낮아집니다.")
    st.write("1-2. 11레벨 이상 우파루끼리 조합 시, 클라우처럼 신성 우파루의 등장 가능성이 생깁니다.    취향에 따라 결정하시면 됩니다.")
    st.write(".")
    st.write("2. 왼쪽 우파루의 유전자(?)를 더 잘 물려받는 경향이 있습니다.")
    st.write("2-1. 대체로 왼쪽 우파루를 크로스 시간이 짧은 우파루(단일속성)으로 배치하면 크로스 시간(기댓값)이 짧아집니다.")    
    st.write(".")
    st.write("3. 별속성, 3속성, 한정, 레어, 드빌 우파루들은 일반적으로 조합에 관계없이 고정 확률을 지닙니다.")
    st.write("3-1. 한정 3속성은 대체로 3%, 한정 2속성은 5%, 레어 우파루는 4%의 고정확률을 지닙니다.")
    st.write("3-2. 특수 우파루 또한 고정 확률을 지닙니다. (토드 3%, 러브럽 5%, 포기사 5%)")
    st.write("3-3. 단, 조합 결과 상 나올 수 있는 고정 확률 우파루가 너무 많아지면,    전체적으로 확률을 낮춤으로써 총합이 100%가 되도록 유지합니다.")
    st.write(".")
    st.write("4. 따라서 6속성을 섞는 크로스, 레어 속성 조합을 3가지 이상 포함하는 조합은 대체로 확률 너프를 받습니다.")
    st.write("4-1. 레어 속성 조합: 숲+얼음, 불+얼음, 불+매직, 땅+바람, 물+천둥, 물+슈거")
    st.write("4-2. 행운업을 할 때에는 고정확률의 합 또한 높아지므로, 확률 너프를 받을 가능성이 커집니다.")
    st.write(".")
    st.write("5. 확률업 이벤트 진행 시에는 매직크로스에만 즉시완료+행운업을 시행하는 것이 훨씬 이득입니다.")
    st.write("5-1. 매직크로스 42시간, 우파루크로스 10시간이더라도, 우파루크로스를 포기하고 매직크로스만 즉시완료로 굴리는 게 확률적으로 이득입니다.")
    st.write("5-2. 하지만 한정을 여러 마리 뽑을 시, 심리적으로는 우파루크로스에도 한정 1마리를 띄우는 게 마음이 편안합니다.")
    st.write(".")
    st.write(".")
    st.write(".")
    st.write("--- 별속성(상시) 소환 조건 ---")
    st.write("레이(2.5%, 36시간): 물 혹은 바람 포함 4속성 이상, 레어 미포함 (9:00 ~ 20:59)")
    st.write("쉐도우(2.5%, 36시간): 물 혹은 바람 포함 4속성 이상, 레어 미포함 (21:00 ~ 08:59)")
    st.write("    (팁: 레이, 쉐도우는 물, 천둥, 바람, 얼음을 모두 섞을 시 확률 2배(5%))")
    st.write("고대신룡(0.6%, 35시간 57분): 16레벨 이상끼리 크로스, 5속성 이상")
    st.write("다크닉스(0.6%, 35시간 57분): 16레벨 이상끼리 크로스, 5속성 이상")
    st.write("골디(1.2%, 48시간): 레어 1마리 포함, 4속성 이상")
    st.write("다크골디(0.7%, 48시간): 레어+레어 (2속성 크로스인 바우+보라도루 추천)")
    st.write("루핀(1.5%, 40시간): 레어 1마리 포함, 4속성 이상")
    st.write("크로노(2%, 42시간): 5속성 이상")
    st.write("클라우(1.2%, 50시간): 11레벨 이상끼리 크로스, 5속성 이상")
    st.write("치우(1.2%, 50시간): 11레벨 이상끼리 크로스, 바람, 얼음 포함 4속성 이상")
    st.write("홀리(1.2%, 50시간): 11레벨 이상끼리 크로스, 물, 천둥 포함 4속성 이상")
    st.write("레오(1%, 51시간): 16레벨 이상끼리 크로스, 레어 1마리 포함, 4속성 이상")
    st.write("아르코(1%, 52시간): 16레벨 이상끼리 크로스, 물 포함 5속성 이상")
    st.write("루루(1.5%, 40시간 15분): 불, 바람, 매직 포함 4속성 이상")
    st.write(".")
    st.write("신성 5종을 모두 노리려면?")
    st.write("16레벨 이상끼리 크로스, 물, 천둥, 바람, 얼음 포함 5속성 크로스")
    st.write("(6속성 크로스할 경우에는 확률 너프 감수)")
    st.write(".")
    st.write(".")
    st.write(".")
    st.write("--- 특수 우파루 소환 조건 ---")
    st.write("러브럽(5%, 10시간 30분): 초코럽 + 코코럽 조합에서만")
    st.write(".")
    st.write(".")
    st.write(".")
    st.write("--- 신성 진화에 필요한 마법석 개수 ---")
    st.write("(순서대로 숲, 땅, 불, 얼음, 번개, 물, 바람, 매직, 별 마법석 개수)")
    st.write("빛: 홀리 -> 세인트 -> 엔젤")
    st.write("세인트: 1, 1, 1, 1, 1, 1, 1, 1, 1")
    st.write("엔젤: 1, 1, 2, 2, 3, 2, 2, 1, 2")
    st.write(".")
    st.write("어둠: 치우 -> 아수라 -> 라푼타")
    st.write("아수라: 1, 1, 1, 1, 1, 1, 1, 1, 1")
    st.write("라푼타: 1, 2, 2, 3, 2, 2, 1, 1, 2")
    st.write(".")
    st.write("황금: 레오 -> 발리언트 -> 마르스")
    st.write("발리언트: 1, 1, 1, 1, 1, 1, 1, 1, 1")
    st.write("마르스: 1, 1, 1, 2, 3, 2, 2, 1, 3")
    st.write(".")
    st.write("구름: 클라우 -> 미스틱 -> 매그너스")
    st.write("미스틱: 1, 1, 1, 1, 1, 1, 1, 1, 1")
    st.write("매그너스: 3, 2, 2, 2, 2, 1, 1, 1, 2")
    st.write(".")
    st.write("무지개: 아르코 -> 이리스 -> 미라쥬")
    st.write("이리스: 1, 1, 1, 1, 1, 1, 1, 1, 1")
    st.write("미라쥬: 1, 1, 1, 2, 2, 2, 2, 2, 3")
    st.write(".")
    st.write("아트모스: 매그너스, 라푼타, 마르스, 미라쥬, 엔젤 보유 시 소환 가능")
    st.write("필요 마법석: 3, 3, 3, 3, 3, 2, 2, 2, 4")
    st.write(".")
    st.write(".")
    st.write(".")
    st.write("--- 루루 마법 진화에서의 마법석 ---")
    st.write("기본 진화확률: 10%")
    st.write("진화 성공 시 등장 확률: 실비아 3%, 루나실 3%, 미쉘 3%, 네로: 91%")
    st.write("마법석을 주어 진화확률이 최소 30% 이상이 되어야 진화 시도가 가능합니다.")
    st.write("(네로는 진화 성공체 중에서도 실패작이라 생각하시면 편합니다.)")
    st.write(".")
    st.write("숲, 땅, 불, 얼음, 번개, 물, 바람, 매직 마법석을 주면 수당: 진화확률 +3%")
    st.write("별 마법석 1개를 주면: 진화확률 +15%")
    st.write("검은 마법석 1개를 주면: 진화확률 +15%")
    st.write("불 마법석 1개를 주면, 진화 선공 시 등장 확률이 실비아 +3%, 네로 -3%")
    st.write("바람 마법석 1개를 주면, 진화 선공 시 확률이 루나실 +3%, 네로 -3%")
    st.write("매직 마법석 1개를 주면, 진화 선공 시 확률이 미쉘 +3%, 네로 -3%")
    st.write("검은 마법석 1개를 주면, 진화 선공 시 확률이 실비아 +5%, 루나실 +5%, 미쉘 +5%, 네로 -15%")
    st.write(".")
    st.write("(마법석은 하루에 3개까지만 투입 가능)")
    st.write("불 마법석 30개 지급: 진화확률 100%")
    st.write("=> 실비아 93%, 루나실 3%, 미쉘 3%, 네로 1%")
    st.write("바람 마법석 30개 지급: 진화확률 100%")
    st.write("=> 실비아 3%, 루나실 93%, 미쉘 3%, 네로 1%")
    st.write("매직 마법석 30개 지급: 진화확률 100%")
    st.write("=> 실비아 3%, 루나실 3%, 미쉘 93%, 네로 1%")
    st.write("검은 마법석 6개 지급: 진화확률 100%")
    st.write("=> 실비아 33%, 루나실 33%, 미쉘 33%, 네로 1%")
    st.write(".")
    st.write("등장 확률이 음수가 되면 0%로 조정.")
    st.write("등장 확률 합이 100%를 초과하면 비중대로 부여하여 100%로 맞춤")
    st.write("예: 불 마법석 30개 지급 후 검은 마법석 1개를 주면,")
    st.write(". 실비아 93% -> 98%, 루나실 3% -> 8%, 미쉘 3% -> 8%, 네로 1% -> -14%")
    st.write(". 네로는 -14% -> 0%로 조정")
    st.write(". 실비아는 98% -> 98/(98+8+8) = 86%로 조정")
    st.write(". 루나실과 미쉘은 8% -> 8/(98+8+8) = 7%로 조정")
    
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
    
    # 3자리 단위로 콤마 추가
    comma_feed_data = feed_data.applymap(lambda x: f"{int(x):,}"
                                         if isinstance(x, (int, float))
                                         else x)
    # 데이터를 HTML로 변환 (인덱스 제거)
    html_table = comma_feed_data.to_html(index=False, escape=False)

    # Streamlit에 HTML 출력
    st.markdown(f"""
        <style>
        table {{ margin: 0 auto; }}
        </style>
        {html_table}
    """, unsafe_allow_html=True)
    


# In[ ]:




