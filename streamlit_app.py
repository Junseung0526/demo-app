import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="📊 확장된 비즈니스 대시보드",
    layout="wide",
)

st.markdown("<h1 style='color: #6c5ce7;'>💼 비즈니스 대시보드</h1>", unsafe_allow_html=True)

# ------------------- 데이터 생성 -------------------
np.random.seed(42)

dates = pd.date_range(datetime.today() - timedelta(days=29), periods=30)
regions = ['서울', '부산', '대구', '광주', '대전']
categories = ['전자제품', '의류', '식품', '가전', '도서']

data = pd.DataFrame({
    '날짜': np.tile(dates, len(regions)),
    '지역': np.repeat(regions, len(dates)),
    '매출': np.random.randint(1000, 10000, size=len(dates)*len(regions)),
    '방문자': np.random.randint(100, 1000, size=len(dates)*len(regions)),
    '전환율': np.round(np.random.uniform(0.01, 0.2, size=len(dates)*len(regions)), 3)
})

cat_data = pd.DataFrame({
    '카테고리': np.random.choice(categories, 200),
    '판매량': np.random.randint(10, 200, 200)
})

# ------------------- 대시보드 상단 지표 -------------------
col1, col2, col3 = st.columns(3)

col1.metric("📈 총 매출", f"₩{data['매출'].sum():,}")
col2.metric("👥 총 방문자", f"{data['방문자'].sum():,}명")
col3.metric("🔁 평균 전환율", f"{data['전환율'].mean()*100:.2f}%")

st.markdown("---")

# ------------------- 지역 선택 및 필터 -------------------
st.sidebar.header("🔍 필터")
selected_region = st.sidebar.selectbox("지역 선택", ["전체"] + regions)
date_range = st.sidebar.slider("날짜 범위 선택", min_value=dates.min().date(), max_value=dates.max().date(),
                               value=(dates.min().date(), dates.max().date()))

# 필터 적용
filtered_data = data.copy()
if selected_region != "전체":
    filtered_data = filtered_data[filtered_data['지역'] == selected_region]

filtered_data = filtered_data[
    (filtered_data['날짜'].dt.date >= date_range[0]) &
    (filtered_data['날짜'].dt.date <= date_range[1])
]

# ------------------- 추이 차트 -------------------
st.subheader("📊 날짜별 매출 & 방문자 추이")

agg_data = filtered_data.groupby('날짜').agg({
    '매출': 'sum',
    '방문자': 'sum'
}).reset_index()

fig1 = px.line(agg_data, x="날짜", y=["매출", "방문자"], markers=True,
               title="일자별 추이", template="plotly_white")
fig1.update_traces(line=dict(width=2))

st.plotly_chart(fig1, use_container_width=True)

# ------------------- 지역별 매출 -------------------
st.subheader("📍 지역별 총 매출")

region_sales = data.groupby('지역')['매출'].sum().reset_index()
fig2 = px.bar(region_sales, x="지역", y="매출", color="지역", text_auto=True,
              template="plotly_dark", title="지역별 매출 분포")
st.plotly_chart(fig2, use_container_width=True)

# ------------------- 카테고리 판매량 -------------------
st.subheader("🛍️ 카테고리별 판매량")

cat_counts = cat_data.groupby("카테고리")["판매량"].sum().reset_index().sort_values("판매량", ascending=False)
fig3 = px.pie(cat_counts, names="카테고리", values="판매량", title="판매 비율", hole=0.4,
              color_discrete_sequence=px.colors.sequential.Rainbow_r)
st.plotly_chart(fig3, use_container_width=True)

# ------------------- 원본 데이터 확인 -------------------
with st.expander("🔎 원본 데이터 보기"):
    st.dataframe(filtered_data.head(100))

# ------------------- 푸터 -------------------
st.markdown("<hr><center>🚀 Streamlit으로 만든 비즈니스 대시보드 | ⓒ 2025</center>", unsafe_allow_html=True)