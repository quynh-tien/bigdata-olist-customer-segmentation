import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình trang Dashboard
st.set_page_config(
    page_title="Phân khúc khách hàng Big Data",
    page_icon="📊",
    layout="wide"
)

# Tiêu đề ứng dụng
st.title("📊 Phân khúc khách hàng thương mại điện tử bằng Big Data")
st.markdown("---")

# Đọc dữ liệu từ file CSV
@st.cache_data
def load_data():
    df = pd.read_csv("segment_summary.csv")
    return df

df = load_data()

# Bộ lọc Phân khúc ở Thanh bên (Sidebar)
st.sidebar.header("🔍 Bộ Lọc Phân Khúc")
segment_options = ["Tất cả"] + list(df['segment_name'].unique())
selected_segment = st.sidebar.selectbox("Chọn phân khúc khách hàng:", segment_options)

# Lọc dữ liệu theo lựa chọn
if selected_segment != "Tất cả":
    filtered_df = df[df['segment_name'] == selected_segment]
else:
    filtered_df = df

# Hiển thị chỉ số KPI
col1, col2, col3 = st.columns(3)
total_customers = df['customer_count'].sum()
selected_customers = filtered_df['customer_count'].sum()

col1.metric("Tổng số khách hàng", f"{total_customers:,}")
col2.metric("Số phân khúc", f"{len(df)}")
col3.metric("Số KH trong lựa chọn", f"{selected_customers:,}")

st.markdown("---")

# Khu vực Biểu đồ
st.subheader("📈 Biểu Đồ Phân Tích Hành Vi Khách Hàng")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    fig_pie = px.pie(
        df,
        values='customer_count',
        names='segment_name',
        title='Tỷ trọng khách hàng theo Phân khúc',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    fig_monetary = px.bar(
        filtered_df,
        x='segment_name',
        y='avg_monetary',
        color='segment_name',
        title='Chi tiêu trung bình (Monetary - R$)',
        text_auto='.2f',
        labels={'segment_name': 'Phân khúc', 'avg_monetary': 'Monetary (R$)'}
    )
    fig_monetary.update_layout(showlegend=False)
    st.plotly_chart(fig_monetary, use_container_width=True)

col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    fig_recency = px.bar(
        filtered_df,
        x='segment_name',
        y='avg_recency',
        color='segment_name',
        title='Số ngày mua hàng gần nhất (Recency - Ngày)',
        text_auto='.2f',
        labels={'segment_name': 'Phân khúc', 'avg_recency': 'Recency (Ngày)'}
    )
    fig_recency.update_layout(showlegend=False)
    st.plotly_chart(fig_recency, use_container_width=True)

with col_chart4:
    fig_freq = px.bar(
        filtered_df,
        x='segment_name',
        y='avg_frequency',
        color='segment_name',
        title='Tần suất mua hàng trung bình (Frequency - Lần)',
        text_auto='.2f',
        labels={'segment_name': 'Phân khúc', 'avg_frequency': 'Frequency (Lần)'}
    )
    fig_freq.update_layout(showlegend=False)
    st.plotly_chart(fig_freq, use_container_width=True)

st.markdown("---")

# Bảng dữ liệu chi tiết
st.subheader("📋 Bảng Tổng Hợp Thông Tin Phân Khúc")

display_df = filtered_df.rename(columns={
    'cluster': 'Cluster',
    'segment_name': 'Tên Phân khúc',
    'customer_count': 'Số lượng KH',
    'avg_recency': 'Recency trung bình (ngày)',
    'avg_frequency': 'Frequency trung bình (lần)',
    'avg_monetary': 'Monetary trung bình (R$)'
})

st.dataframe(display_df, use_container_width=True)
