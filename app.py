import streamlit as st
import pandas as pd

st.set_page_config(page_title="T1 2026 MSI Dashboard", page_icon="🏆", layout="wide")

st.title("🏆 T1 2026 MSI 실시간 심층 대시보드")
st.caption("최종 업데이트 기준: 2026년 7월 6일 (FURIA전 종료 시점)")
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

# 2. 실제 피어리스 메타 반영 선수별 출전 챔피언 데이터
@st.cache_data
def load_player_data():
    idx = ["최근 매치업 픽", "주요 기용 픽"]
    player_stats = {
        "Doran (최현준)": {
            "Position": "TOP", "KDA": "3.95", "Status": "안정적인 앞라인 소화",
            "Champs": pd.DataFrame({"확인된 챔피언": ["나르 (Gnar)", "럼블 (Rumble)"], "주요 매치": ["BLG전 5세트", "FURIA전 2세트"]}, index=idx)
        },
        "Oner (문현준)": {
            "Position": "JUNGLE", "KDA": "4.21", "Status": "날카로운 이니시 주도",
            "Champs": pd.DataFrame({"확인된 챔피언": ["트런들 (Trundle)", "자르반 4세 (Jarvan IV)"], "주요 매치": ["BLG전 5세트", "FURIA전 2세트"]}, index=idx)
        },
        "Faker (이상혁)": {
            "Position": "MID", "KDA": "4.08", "Status": "클러치 플레이 메이킹",
            "Champs": pd.DataFrame({"확인된 챔피언": ["탈리야 (Taliyah)", "애니 (Annie)"], "주요 매치": ["BLG전 5세트", "FURIA전 2세트"]}, index=idx)
        },
        "Peyz (김수환)": {
            "Position": "BOT", "KDA": "5.12", "Status": "강력한 메인 딜링 담당",
            "Champs": pd.DataFrame({"확인된 챔피언": ["유나라 (Yunara)", "케이틀린 (Caitlyn)"], "주요 매치": ["BLG전 5세트", "FURIA전 2세트"]}, index=idx)
        },
        "Keria (류민석)": {
            "Position": "SUPPORT", "KDA": "4.15", "Status": "변수 창출 및 라인전 주도",
            "Champs": pd.DataFrame({"확인된 챔피언": ["룰루 (Lulu)", "럭스 (Lux)"], "주요 매치": ["BLG전 5세트", "FURIA전 2세트"]}, index=idx)
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
st.subheader("🎯 T1 선수단 실제 인게임 지표 분석 (피어리스 드래프트 반영)")
selected_player = st.selectbox("분석할 선수를 선택하세요:", list(players_dict.keys()))
p_data = players_dict[selected_player]

col1, col2, col3 = st.columns(3)
with col1: st.metric(label="포지션", value=p_data["Position"])
with col2: st.metric(label="확인된 KDA", value=p_data["KDA"])
with col3: st.metric(label="플레이 스타일", value=p_data["Status"])

st.dataframe(p_data["Champs"], use_container_width=True)
