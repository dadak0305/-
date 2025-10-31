import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Gym Analysis", layout="wide")

st.title("🏋️‍♀️ 체육관 운동 데이터 분석 사이트")

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is None:
        # ✅ Streamlit Cloud / GitHub 환경에서도 동작
        return pd.read_csv("gym_members_exercise_tracking.csv")
    else:
        return pd.read_csv(uploaded_file)

uploaded = st.sidebar.file_uploader("CSV 업로드 (옵션)", type=["csv"])
df = load_data(uploaded)

st.sidebar.markdown("### 필터")
# Column auto-detection
gender_col = "Gender" if "Gender" in df.columns else None
exercise_col = "Workout_Type" if "Workout_Type" in df.columns else None
age_col = "Age" if "Age" in df.columns else None
duration_col = "Session_Duration (hours)" if "Session_Duration (hours)" in df.columns else None

# Gender Filter
if gender_col:
    genders = sorted(df[gender_col].dropna().unique())
    chosen_gender = st.sidebar.multiselect("성별 선택", genders, default=genders)
    df = df[df[gender_col].isin(chosen_gender)]

# Exercise Filter
if exercise_col:
    exercises = sorted(df[exercise_col].dropna().unique())
    chosen_ex = st.sidebar.multiselect("운동 종류 선택", exercises, default=exercises[:10])
    df = df[df[exercise_col].isin(chosen_ex)]

st.markdown("## 📊 주요 데이터 개요")

col1, col2, col3, col4 = st.columns(4)
col1.metric("총 데이터 수", len(df))
if exercise_col: col2.metric("운동 종류 수", df[exercise_col].nunique())
if age_col: col3.metric("평균 연령", round(df[age_col].mean(), 2))
if duration_col: col4.metric("평균 운동시간 (시간)", round(df[duration_col].mean(), 2))

st.markdown("### 데이터 미리보기")
st.dataframe(df.head(200))

st.markdown("## 🔥 시각화")

# Top Workout Types
if exercise_col:
    st.markdown("### 운동 종류 빈도")
    top = df[exercise_col].value_counts().head(15)
    fig, ax = plt.subplots()
    ax.bar(top.index, top.values)
    ax.set_xticklabels(top.index, rotation=45)
    st.pyplot(fig)

# Age distribution
if age_col:
    st.markdown("### 연령대 분포")
    fig, ax = plt.subplots()
    ax.hist(df[age_col], bins=10)
    ax.set_xlabel("나이")
    ax.set_ylabel("인원 수")
    st.pyplot(fig)

st.markdown("---")
st.markdown("✅ 이 사이트는 GitHub + Streamlit Cloud로 자동 배포됩니다.")
