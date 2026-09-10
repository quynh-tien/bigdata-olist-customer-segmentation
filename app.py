import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Cấu hình trang (bắt buộc đặt ở dòng đầu tiên)
st.set_page_config(
    page_title="Phân khúc khách hàng", page_icon="📊", layout="wide"
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

# Tính tổng số KH toàn hệ thống & Thứ hạng từng phân khúc (1 đến 6)
TOTAL_CUSTOMERS = df_summary["customer_count"].sum()
df_summary["rank"] = (
    df_summary["customer_count"].rank(ascending=False, method="min").astype(int)
)

# 3. Bảng màu đồng bộ cho 6 phân khúc khi chọn "Tất cả"
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
st.title("📊 Phân khúc khách hàng")

tab1, tab2, tab3 = st.tabs([
    "📈 Tổng Quan KPI",
    "🔍 Biểu Đồ Hành Vi (RFM)",
    "💡 Đề Xuất Chiến Lược",
])

# --- TAB 1: TỔNG QUAN / CHI TIẾT THEO PHÂN KHÚC ---
with tab1:
  if selected_segment == "Tất cả":
    # GIAO DIỆN TỔNG QUAN (Chỉ hiện khi chọn "Tất cả")
    c1, c2, c3 = st.columns(3)
    c1.metric("Tổng số khách hàng", f"{TOTAL_CUSTOMERS:,}")
    c2.metric("Số phân khúc", "6")

    largest_seg = df_summary.loc[df_summary["customer_count"].idxmax()][
        "segment_name"
    ]
    with c3:
      st.markdown(
          "<p style='font-size: 14px; color: #31333F; opacity: 0.8;"
          " margin-bottom: 0px;'>Phân khúc lớn nhất</p>",
          unsafe_allow_html=True,
      )
      st.markdown(
          f"<p style='font-size: 20px; font-weight: 600; color: #31333F;"
          f" margin-top: 4px;'>{largest_seg}</p>",
          unsafe_allow_html=True,
      )

    st.divider()

    fig_pie = px.pie(
        df_summary,
        names="segment_name",
        values="customer_count",
        title="Tỷ trọng khách hàng theo 6 Phân khúc",
        color="segment_name",
        color_discrete_map=COLOR_MAP,
        hole=0.4,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

  else:
    # GIAO DIỆN KHI CHỌN 1 PHÂN KHÚC CỤ THỂ (Không hiện Tổng quan)
    seg_info = filtered_df.iloc[0]
    seg_count = seg_info["customer_count"]
    seg_rank = seg_info["rank"]
    seg_pct = (seg_count / TOTAL_CUSTOMERS) * 100

    # Hiển thị 3 chỉ số riêng biệt cho phân khúc được chọn
    c1, c2, c3 = st.columns(3)
    c1.metric("Số lượng khách hàng", f"{seg_count:,}")
    c2.metric("Tỷ trọng so với toàn bộ", f"{seg_pct:.2f}%")
    c3.metric("Thứ hạng quy mô", f"Đứng thứ {seg_rank} / 6")

    st.divider()

    # Tạo dữ liệu biểu đồ tròn 2 phần: Phân khúc chọn (Màu Xanh) vs Các phân khúc còn lại (Màu Vàng)
    pie_data = pd.DataFrame({
        "Phân loại": [selected_segment, "Các phân khúc còn lại"],
        "Số lượng": [seg_count, TOTAL_CUSTOMERS - seg_count],
    })

    # Đặt màu cố định: Xanh dương cho phân khúc chọn, Vàng cho phần còn lại
    custom_colors = {
        selected_segment: "#1F77B4",  # Xanh dương
        "Các phân khúc còn lại": "#FFD700",  # Vàng
    }

    fig_pie = px.pie(
        pie_data,
        names="Phân loại",
        values="Số lượng",
        title=(
            f"Tỷ trọng phân khúc '{selected_segment}' so với Tổng hệ thống"
        ),
        color="Phân loại",
        color_discrete_map=custom_colors,
        hole=0.4,
    )
    fig_pie.update_traces(
        textinfo="percent+label",
        hovertemplate="%{label}: %{value:,} KH (%{percent})",
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
        color_discrete_map=COLOR_MAP if selected_segment == "Tất cả" else None,
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
        color_discrete_map=COLOR_MAP if selected_segment == "Tất cả" else None,
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
        color_discrete_map=COLOR_MAP if selected_segment == "Tất cả" else None,
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
