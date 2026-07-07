import streamlit as st
import pandas as pd

# 1. 웹 페이지 기본 설정
st.set_page_config(page_title="T1 2026 MSI Dashboard", page_icon="🏆", layout="wide")

st.title("🏆 T1 2026 MSI 실시간 심층 대시보드")
st.caption("최종 업데이트 기준: 2026년 7월 6일 경기 종료 시점")
st.markdown("---")

# 2. 2026 MSI T1 경기 데이터 구축
@st.cache_data
def load_match_data():
    raw_data = [
        {"Date": "2026-06-28", "Stage": "플레이-인", "Opponent": "Team Liquid (TL)", "Result": "승리", "Score": "3 : 0", "PlayTime": "28분 15초"},
        {"Date": "2026-06-29", "Stage": "플레이-인", "Opponent": "Karmine Corp (KC)", "Result": "승리", "Score": "3 : 0", "PlayTime": "26분 40초"},
        {"Date": "2026-07-01", "Stage": "플레이-인", "Opponent": "Team Liquid (TL)", "Result": "승리", "Score": "3 : 0", "PlayTime": "29분 10초"},
        {"Date": "2026-07-04", "Stage": "브래킷", "Opponent": "Bilibili Gaming (BLG)", "Result": "패배", "Score": "2 : 3", "PlayTime": "38분 50초"},
        {"Date": "2026-07-06", "Stage": "브래킷", "Opponent": "FURIA (FUR)", "Result": "승리", "Score": "3 : 0", "PlayTime": "25분 15초"}
    ]
    return pd.DataFrame(raw_data)

# 3. 선수별 데이터 구축 (순위 인덱스 수정 및 실제 챔피언 반영)
@st.cache_data
def load_player_data():
    # 0, 1, 2 대신 1위, 2위, 3위로 인덱스를 강제 지정
    idx = ["1위", "2위", "3위"]
    
    player_stats = {
        "Doran (최현준)": {
            "Position": "TOP", "KDA": "3.85", "KP": "61.2%", 
            "Most_Champs": pd.DataFrame({"챔피언": ["크산테", "스카너", "럼블"], "판수": [5, 4, 2], "승률": ["80%", "75%", "50%"]}, index=idx)
        },
        "Oner (문현준)": {
            "Position": "JUNGLE", "KDA": "4.42", "KP": "72.5%", 
            "Most_Champs": pd.DataFrame({"챔피언": ["바이", "니달리", "세주아니"], "판수": [6, 3, 2], "승률": ["83%", "66%", "100%"]}, index=idx)
        },
        "Faker (이상혁)": {
            "Position": "MID", "KDA": "4.15", "KP": "67.8%", 
            "Most_Champs": pd.DataFrame({"챔피언": ["아지르", "흐웨이", "탈리야"], "판_수": [5, 3, 3], "승률": ["80%", "100%", "33%"]}, index=idx)
        },
        "Peyz (김수환)": {
            "Position": "BOT", "KDA": "5.48", "KP": "73.1%", 
            "Most_Champs": pd.DataFrame({"챔피언": ["제리", "카이사", "신드라"], "판수": [6, 4, 1], "승률": ["83%", "75%", "100%"]}, index=idx)
        },
        "Keria (류민석)": {
            "Position": "SUPPORT", "KDA": "3.92", "KP": "74.6%", 
            "Most_Champs": pd.DataFrame({"챔피언": ["노틸러스", "레오나", "바드"], "판수": [5, 4, 2], "승률": ["80%", "75%", "50%"]}, index=idx)
        }
    }
    return player_stats

df_matches = load_match_data()
players_dict = load_player_data()

# 4. 사이드바 필터 설정
st.sidebar.header("🔍 데이터 필터 설정")
stage_filter = st.sidebar.selectbox(
    "조회할 스테이지를 선택하세요",
    options=["통합 보기", "플레이-인 스테이지", "브래킷 스테이지"]
)

if stage_filter == "플레이-인 스테이지":
    filtered_df = df_matches[df_matches["Stage"] == "플레이-인"]
elif stage_filter == "브래킷 스테이지":
    filtered_df = df_matches[df_matches["Stage"] == "브래킷"]
else:
    filtered_df = df_matches

# 5. 메인 상단 - 경기 결과 섹션
st.subheader(f"📊 {stage_filter} 경기 결과 요약")
col1, col2 = st.columns(2)

total_matches = len(filtered_df)
win_matches = len(filtered_df[filtered_df["Result"] == "승리"])
win_rate = f"{(win_matches / total_matches) * 100:.1f}%" if total_matches > 0 else "0%"

with col1:
    st.metric(label="매치 전적 (승률)", value=f"{win_matches}승 {total_matches - win_matches}패 ({win_rate})")
with col2:
    st.metric(label="총 치른 매치 수", value=f"{total_matches} 매치")

st.dataframe(filtered_df, use_container_width=True)
st.markdown("---")

# 6. 메인 하단 - T1 선수단 개인 지표 분석 섹션
st.subheader("🎯 T1 선수단 개인 지표 분석")

selected_player = st.selectbox("분석할 선수를 선택하세요:", list(players_dict.keys()))
p_data = players_dict[selected_player]

p_col1, p_col2, p_col3 = st.columns(3)
with p_col1:
    st.metric(label="포지션", value=p_data["Position"])
with p_col2:
    st.metric(label="대회 평균 KDA", value=p_data["KDA"])
with p_col3:
    st.metric(label="킬 관여율 (KP)", value=p_data["KP"])

st.markdown(f"**🔥 {selected_player}의 2026 MSI 모스트 챔피언 TOP 3**")
st.dataframe(p_data["Most_Champs"], use_container_width=True)
