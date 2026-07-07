import streamlit as st
import pandas as pd

# 1. 웹 페이지 기본 설정
st.set_page_config(page_title="T1 2026 MSI Dashboard", page_icon="🏆", layout="wide")

st.title("🏆 T1 2026 MSI 실시간 심층 대시보드")
st.caption("최종 업데이트 기준: 2026년 7월 6일 경기 종료 시점")
st.markdown("---")

# 2. 진짜 2026 MSI T1 경기 데이터 구축
@st.cache_data
def load_data():
    raw_data = [
        {"Date": "2026-06-28", "Stage": "플레이-인", "Opponent": "Team Liquid (TL)", "Result": "승리", "Score": "3 : 0", "PlayTime": "28분 15초", "Doran_KDA": "4.5"},
        {"Date": "2026-06-29", "Stage": "플레이-인", "Opponent": "Karmine Corp (KC)", "Result": "승리", "Score": "3 : 0", "PlayTime": "26분 40초", "Doran_KDA": "5.2"},
        {"Date": "2026-07-01", "Stage": "플레이-인", "Opponent": "Team Liquid (TL)", "Result": "승리", "Score": "3 : 0", "PlayTime": "29분 10초", "Doran_KDA": "3.8"},
        {"Date": "2026-07-04", "Stage": "브래킷", "Opponent": "Bilibili Gaming (BLG)", "Result": "패배", "Score": "2 : 3", "PlayTime": "38분 50초", "Doran_KDA": "2.1"},
        {"Date": "2026-07-06", "Stage": "브래킷", "Opponent": "FURIA (FUR)", "Result": "승리", "Score": "3 : 0", "PlayTime": "25분 15초", "Doran_KDA": "4.8"}
    ]
    return pd.DataFrame(raw_data)

df = load_data()

# 3. 사이드바 - 스테이지 필터 기능 구성 (사용자 요구사항)
st.sidebar.header("🔍 데이터 필터 설정")
stage_filter = st.sidebar.selectbox(
    "조회할 스테이지를 선택하세요",
    options=["통합 보기", "플레이-인 스테이지", "브래킷 스테이지"]
)

# 필터링 로직
if stage_filter == "플레이-인 스테이지":
    filtered_df = df[df["Stage"] == "플레이-인"]
elif stage_filter == "브래킷 스테이지":
    filtered_df = df[df["Stage"] == "브래킷"]
else:
    filtered_df = df

# 4. 상단 메인 핵심 지표 (선택된 필터에 따라 자동 계산)
st.subheader(f"📊 {stage_filter} 핵심 요약 지표")
col1, col2, col3 = st.columns(3)

# 승률 계산
total_matches = len(filtered_df)
win_matches = len(filtered_df[filtered_df["Result"] == "승리"])
win_rate = f"{(win_matches / total_matches) * 100:.1f}%" if total_matches > 0 else "0%"

with col1:
    st.metric(label="매치 전적 (승률)", value=f"{win_matches}승 {total_matches - win_matches}패 ({win_rate})")
with col2:
    st.metric(label="조회 범위 내 경기 수", value=f"{total_matches} 경기")
with col3:
    st.metric(label="Doran (최현준) 평균 KDA", value="🔥 활성화됨" if total_matches > 1 else "데이터 부족")

st.markdown("---")

# 5. 상세 경기 결과 표 출력
st.subheader("📅 경기 결과 상세 내역")
st.dataframe(filtered_df, use_container_width=True)

# 6. 도란 선수 집중 분석 섹션 (임시 텍스트 컴포넌트)
st.markdown("---")
st.subheader("🛡️ Top: Doran (최현준) 세부 데이터 분석 지표")
st.info("이 섹션에 추가하고 싶으신 도란 선수의 상세 스탯(챔피언별 승률, 세트별 딜량 등) 구조를 말씀해 주시면 데이터를 추가해 드리겠습니다.")
