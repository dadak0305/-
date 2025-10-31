import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- THEME ----------------------
st.set_page_config(page_title="Gym Analysis Dashboard", layout="wide")

GYM_COLOR = "#00FF6A"   # 형광 라임 포인트 컬러
BG_COLOR = "#0D0D0D"    # 진한 다크 배경

st.markdown(
    f"""
    <style>
        body {{
            background-color: {BG_COLOR};
            color: white;
        }}
        .sidebar .sidebar-content {{
            background-color: #111111 !important;
        }}
        .stMetric label {{
            color: white !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------- DATA ----------------------
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is None:
        return pd.read_csv("gym_members_exercise_tracking.csv")
    return pd.read_csv(uploaded_file)

st.title("💪 GYM PERFORMANCE DASHBOARD")

uploaded = st.sidebar.file_uploader("CSV 업로드 (옵션)", type=["csv"])
df = load_data(uploaded)

gender_col = "Gender" if "Gender" in df.columns else None
exercise_col = "Workout_Type" if "Workout_Type" in df.columns else None
age_col = "Age" if "Age" in df.columns else None
duration_col = "Session_Duration (hours)" if "Session_Duration (hours)" in df.columns else None

st.sidebar.markdown("### 🎚 필터")

if gender_col:
    genders = sorted(df[gender_col].dropna().unique())
    chosen_gender = st.sidebar.multiselect("성별", genders, default=genders)
    df = df[df[gender_col].isin(chosen_gender)]

if exercise_col:
    exercises = sorted(df[exercise_col].dropna().unique())
    chosen_ex = st.sidebar.multiselect("운동 종류", exercises, default=exercises[:10])
    df = df[df[exercise_col].isin(chosen_ex)]

# ---------------------- METRICS ----------------------
st.markdown(f"<h3 style='color:{GYM_COLOR}'>🏋️ 요약 지표</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("데이터 수", len(df))
if exercise_col: col2.metric("운동 종류", df[exercise_col].nunique())
if age_col: col3.metric("평균 연령", round(df[age_col].mean(), 1))
if duration_col: col4.metric("평균 세션시간 (hr)", round(df[duration_col].mean(), 2))

# ---------------------- TABLE ----------------------
st.markdown("---")
st.markdown(f"<h3 style='color:{GYM_COLOR}'>📋 데이터 미리보기</h3>", unsafe_allow_html=True)
st.dataframe(df.head(200))

# ---------------------- VISUALS ----------------------
plt.style.use("dark_background")  # ✅ 차트 다크모드

st.markdown("---")
st.markdown(f"<h3 style='color:{GYM_COLOR}'>🔥 시각화 분석</h3>", unsafe_allow_html=True)

if exercise_col:
    st.markdown("### 운동 종류 빈도")
    top = df[exercise_col].value_counts().head(15)
    fig, ax = plt.subplots()
    ax.bar(top.index, top.values, color=GYM_COLOR)
    ax.set_xticklabels(top.index, rotation=45, ha="right")
    st.pyplot(fig)

if age_col:
    st.markdown("### 연령대 분포")
    fig, ax = plt.subplots()
    ax.hist(df[age_col], bins=10, color=GYM_COLOR, edgecolor="white")
    ax.set_xlabel("나이")
    ax.set_ylabel("인원 수")
    st.pyplot(fig)

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>Made for Gym Performance Analytics 🏆</p>", unsafe_allow_html=True)
