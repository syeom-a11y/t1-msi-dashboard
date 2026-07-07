import streamlit as st
import pandas as pd

st.set_page_config(page_title="T1 2026 MSI Dashboard", page_icon="🏆", layout="wide")

st.title("🏆 T1 2026 MSI 실시간 심층 대시보드")
st.caption("최종 업데이트 기준: 2026년 7월 7일 (BLG 5세트 + FURIA 3세트 완벽 반영)")
st.markdown("---")

# 1. 실제 매치 데이터셋
@st.cache_data
def load_match_data():
    raw_data = [
        {"Date": "2026-06-28", "Stage": "플레이-인", "Opponent": "Team Liquid (TL)", "Result": "승리", "Score": "3 : 0"},
        {"Date": "2026-06-29", "Stage": "플레이-인", "Opponent": "Karmine Corp (KC)", "Result": "승리", "Score": "3 : 0"},
        {"Date": "2026-07-01", "Stage": "플레이-인", "Opponent": "Team Liquid (TL)", "Result": "승리", "Score": "3 : 0"},
        {"Date": "2026-07-04", "Stage": "브래킷", "Opponent": "Bilibili Gaming (BLG)", "Result": "패배", "Score": "2 : 3"},
        {"Date": "2026-07-06", "Stage": "브래킷", "Opponent": "FURIA (FUR)", "Result": "승리", "Score": "3 : 0"}
    ]
    return pd.DataFrame(raw_data)

# 2. 브래킷 8세트 및 플레이-인 9세트 기반 누적 데이터
@st.cache_data
def load_player_data():
    player_stats = {
        "Doran (최현준)": {
            "Position": "TOP", "KDA": "3.95",
            "Champs": pd.DataFrame({
                "구분": ["최근 매치업 픽 (7/6)", "대회 주요 기용 픽 (Most)"],
                "챔피언": ["럼블 (Rumble)", "나르 (Gnar)"],
                "설명": ["FURIA전 세트 완승 견인", "브래킷 포함 이번 대회 최다 활용 모스트 픽"]
            })
        },
        "Oner (문현준)": {
            "Position": "JUNGLE", "KDA": "4.21",
            "Champs": pd.DataFrame({
                "구분": ["최근 매치업 픽 (7/6)", "대회 주요 기용 픽 (Most)"],
                "챔피언": ["자르반 4세 (Jarvan IV)", "바이 (Vi)"],
                "설명": ["FURIA전 날카로운 이니시 주도", "총 17세트 중 가장 신뢰도 높은 선픽 카드"]
            })
        },
        "Faker (이상혁)": {
            "Position": "MID", "KDA": "4.08",
            "Champs": pd.DataFrame({
                "구분": ["최근 매치업 픽 (7/6)", "대회 주요 기용 픽 (Most)"],
                "챔피언": ["애니 (Annie)", "탈리야 (Taliyah)"],
                "설명": ["FURIA전 허를 찌르는 조커 픽 성공", "브래킷 스테이지 메인 메이킹 카드"]
            })
        },
        "Peyz (김수환)": {
            "Position": "BOT", "KDA": "5.12",
            "Champs": pd.DataFrame({
                "구분": ["최근 매치업 픽 (7/6)", "대회 주요 기용 픽 (Most)"],
                "챔피언": ["케이틀린 (Caitlyn)", "제리 (Zeri)"],
                "설명": ["FURIA전 압도적인 라인전 파괴", "후반 세트 캐리를 전담한 핵심 캐리 픽"]
            })
        },
        "Keria (류민석)": {
            "Position": "SUPPORT", "KDA": "4.15",
            "Champs": pd.DataFrame({
                "구분": ["최근 매치업 픽 (7/6)", "대회 주요 기용 픽 (Most)"],
                "챔피언": ["럭스 (Lux)", "노틸러스 (Nautilus)"],
                "설명": ["바텀 라인전 주도권을 위한 연계 픽", "단단한 이니시와 앞라인 한타 지원 픽"]
            })
        }
    }
    return player_stats

df_matches = load_match_data()
players_dict = load_player_data()

# 3. 필터링 UI
st.sidebar.header("🔍 데이터 필터 설정")
stage_filter = st.sidebar.selectbox("조회할 스테이지를 선택하세요", options=["통합 보기", "플레이-인 스테이지", "브래킷 스테이지"])

if stage_filter == "플레이-인 스테이지":
    filtered_df = df_matches[df_matches["Stage"] == "플레이-인"]
elif stage_filter == "브래킷 스테이지":
    filtered_df = df_matches[df_matches["Stage"] == "브래킷"]
else:
    filtered_df = df_matches

# 4. 화면 출력
st.subheader(f"📊 {stage_filter} 경기 결과 요약")
st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.subheader("🎯 T1 선수단 실제 인게임 지표 분석 (최근 픽 및 주요 픽 분리)")
selected_player = st.selectbox("분석할 선수를 선택하세요:", list(players_dict.keys()))
p_data = players_dict[selected_player]

col1, col2 = st.columns(2)
with col1: st.metric(label="포지션", value=p_data["Position"])
with col2: st.metric(label="대회 평균 KDA", value=p_data["KDA"])

st.dataframe(p_data["Champs"], use_container_width=True, hide_index=True)
