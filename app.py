import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Cấu hình trang (bắt buộc đặt ở dòng đầu tiên)
st.set_page_config(
    page_title="Big Data Customer Segmentation", page_icon="📊", layout="wide"
)

# 2. Khởi tạo dữ liệu tổng hợp 6 phân khúc
data = {
    "cluster": [0, 1, 2, 3, 4, 5],
    "segment_name": [
        "Khách hàng có nguy cơ rời bỏ",
        "Khách hàng mua lặp lại",
        "Khách hàng thông thường",
        "Khách hàng chi tiêu cao",
        "Khách hàng mua thường xuyên",
        "Khách hàng hoạt động gần đây",
    ],
    "customer_count": [20815, 2545, 33449, 2368, 228, 33953],
    "avg_recency": [458.00, 221.51, 254.64, 237.06, 201.79, 86.85],
    "avg_frequency": [1.00, 2.00, 1.00, 1.01, 3.40, 1.00],
    "avg_monetary": [133.55, 271.95, 132.00, 1169.26, 506.03, 136.91],
}
df_summary = pd.DataFrame(data)

# 3. Bảng màu đồng bộ cho 6 phân khúc
COLOR_MAP = {
    "Khách hàng chi tiêu cao": "#FFD700",  # Vàng VIP
    "Khách hàng mua thường xuyên": "#2CA02C",  # Xanh lá
    "Khách hàng mua lặp lại": "#1F77B4",  # Xanh dương
    "Khách hàng hoạt động gần đây": "#17BECF",  # Xanh ngọc
    "Khách hàng thông thường": "#7F7F7F",  # Xám
    "Khách hàng có nguy cơ rời bỏ": "#D62728",  # Đỏ
}

# 4. Đề xuất chiến lược Marketing
MARKETING_ACTION = {
    "Khách hàng chi tiêu cao": (
        "Mời tham gia VIP Club, chăm sóc cá nhân hóa 1-1, gửi quà tri ân độc"
        " quyền."
    ),
    "Khách hàng mua thường xuyên": (
        "Nhân đôi điểm thưởng tích lũy, mời trải nghiệm sản phẩm mới sớm nhất."
    ),
    "Khách hàng mua lặp lại": (
        "Gợi ý sản phẩm mua kèm (Cross-sell), tặng Voucher giảm giá đơn tiếp"
        " theo."
    ),
    "Khách hàng hoạt động gần đây": (
        "Gửi chuỗi Email chăm sóc, hướng dẫn đánh giá sản phẩm để tăng tương"
        " tác."
    ),
    "Khách hàng thông thường": (
        "Tạo chiến dịch Flash Sale theo đợt để thúc đẩy tái mua hàng."
    ),
    "Khách hàng có nguy cơ rời bỏ": (
        "Gửi Email/SMS Re-engagement kèm Mã giảm giá 20-30% để kích hoạt lại."
    ),
}

# 5. Sidebar - Bộ lọc & Tải file
with st.sidebar:
  st.title("🎛️ Bộ Lọc Phân Khúc")
  segment_list = ["Tất cả"] + list(COLOR_MAP.keys())
  selected_segment = st.selectbox("Chọn phân khúc khách hàng:", segment_list)

  st.divider()
  st.markdown("### 📥 Tải Dữ Liệu")
  st.download_button(
      label="Tải file CSV Phân Khúc",
      data=df_summary.to_csv(index=False).encode("utf-8"),
      file_name="segment_summary.csv",
      mime="text/csv",
  )
  st.caption("⚡ Môi trường tính toán: PySpark MLlib")

# Lọc dữ liệu theo Lựa chọn
if selected_segment != "Tất cả":
  filtered_df = df_summary[df_summary["segment_name"] == selected_segment]
else:
  filtered_df = df_summary

# 6. Tiêu đề và Các Tabs giao diện
st.title("📊 Phân Khúc Khách Hàng Thương Mại Điện Tử (Big Data)")

tab1, tab2, tab3 = st.tabs([
    "📈 Tổng Quan KPI",
    "🔍 Biểu Đồ Hành Vi (RFM)",
    "💡 Đề Xuất Chiến Lược",
])

# --- TAB 1: TỔNG QUAN ---
with tab1:
  c1, c2, c3 = st.columns(3)
  c1.metric("Tổng số khách hàng", f"{filtered_df['customer_count'].sum():,}")
  c2.metric("Số phân khúc", "6" if selected_segment == "Tất cả" else "1")
  c3.metric(
      "Phân khúc lớn nhất",
      f"{df_summary.loc[df_summary['customer_count'].idxmax()]['segment_name']}",
  )

  st.divider()

  fig_pie = px.pie(
      filtered_df,
      names="segment_name",
      values="customer_count",
      title="Tỷ trọng khách hàng theo Phân khúc",
      color="segment_name",
      color_discrete_map=COLOR_MAP,
      hole=0.4,
  )
  st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 2: CHI TIẾT RFM ---
with tab2:
  st.subheader("📊 Biểu Đồ Phân Tích Chỉ Số RFM")

  col_a, col_b, col_c = st.columns(3)

  with col_a:
    fig_r = px.bar(
        filtered_df,
        x="segment_name",
        y="avg_recency",
        color="segment_name",
        color_discrete_map=COLOR_MAP,
        title="Recency Trung Bình (Ngày)",
        text_auto=".1f",
    )
    fig_r.update_layout(showlegend=False, xaxis_title="", yaxis_title="Ngày")
    st.plotly_chart(fig_r, use_container_width=True)

  with col_b:
    fig_f = px.bar(
        filtered_df,
        x="segment_name",
        y="avg_frequency",
        color="segment_name",
        color_discrete_map=COLOR_MAP,
        title="Frequency Trung Bình (Lần)",
        text_auto=".2f",
    )
    fig_f.update_layout(showlegend=False, xaxis_title="", yaxis_title="Lần")
    st.plotly_chart(fig_f, use_container_width=True)

  with col_c:
    fig_m = px.bar(
        filtered_df,
        x="segment_name",
        y="avg_monetary",
        color="segment_name",
        color_discrete_map=COLOR_MAP,
        title="Monetary Trung Bình (R$)",
        text_auto=".2f",
    )
    fig_m.update_layout(showlegend=False, xaxis_title="", yaxis_title="R$")
    st.plotly_chart(fig_m, use_container_width=True)

  st.divider()
  st.subheader("📋 Bảng Tổng Hợp Thông Tin Phân Khúc")
  st.dataframe(filtered_df, use_container_width=True)

# --- TAB 3: ĐỀ XUẤT MARKETING ---
with tab3:
  st.subheader("🎯 Kịch Bản Hành Động Chi Tiết")
  for segment, action in MARKETING_ACTION.items():
    if selected_segment == "Tất cả" or selected_segment == segment:
      with st.expander(f"📌 Phân khúc: **{segment}**", expanded=True):
        st.write(f"👉 **Hành động đề xuất:** {action}")
