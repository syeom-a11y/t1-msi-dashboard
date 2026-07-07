import streamlit as st
import pandas as pd

# 1. 웹 페이지 기본 설정 (상단 타이틀 및 아이콘)
st.set_page_config(page_title="T1 2026 MSI Dashboard", page_icon="🏆", layout="wide")

st.title("🏆 T1 2026 MSI 분석 심층 대시보드")
st.markdown("---")

# 2. 임시 데이터 로드 (T1 2026 MSI 가상 결과 스키마)
# 나중에 데이터 파일(CSV)이 준비되면 이 부분을 교체할 수 있습니다.
st.subheader("📊 2026 MSI 매치 기록 요약")

match_data = pd.DataFrame([
    {"Date": "2026-05-02", "Opponent": "G2 Esports", "Result": "승리 (2:0)", "Side": "Blue/Red"},
    {"Date": "2026-05-05", "Opponent": "Bilibili Gaming", "Result": "패배 (1:2)", "Side": "Blue/Red"},
    {"Date": "2026-05-09", "Opponent": "FlyQuest", "Result": "승리 (2:0)", "Side": "Blue/Red"},
    {"Date": "2026-05-10", "Opponent": "Bilibili Gaming", "Result": "승리 (3:1)", "Side": "Blue/Red"}
])
st.dataframe(match_data, use_container_width=True)

st.markdown("---")
st.subheader("🎯 T1 선수단 주요 지표 (Doran 중심 분석)")

# 레이아웃을 분할하여 깔끔하게 지표 배치
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Doran (최현준) 평균 KDA", value="4.25", delta="+0.45 (상승)")
with col2:
    st.metric(label="Peyz (박루한) 분당 데미지", value="738", delta="+24 (최고치)")
with col3:
    st.metric(label="팀 평균 경기 시간", value="31분 45초", delta="-2분 10초 (스노우볼)")

st.info("💡 오른쪽 위에 있는 배포 버튼을 누르면 이 화면 그대로 인터넷에 나만의 웹사이트가 열립니다!")
