st.title("📊 Phân Khúc Khách Hàng Thương Mại Điện Tử (Big Data)")

# Tạo 3 Tab chính
tab1, tab2, tab3 = st.tabs([
    "📈 Tổng Quan KPI",
    "🔍 Chi Tiết Phân Khúc",
    "💡 Đề Xuất Chiến Lược",
])

# --- TAB 1: TỔNG QUAN ---
with tab1:
  col1, col2, col3 = st.columns(3)
  col1.metric("Tổng số khách hàng", f"{df_summary['customer_count'].sum():,}")
  col2.metric("Số phân khúc", "6")
  col3.metric(
      "Phân khúc lớn nhất",
      f"{df_summary.loc[df_summary['customer_count'].idxmax()]['segment_name']}",
  )

  st.divider()

  # Biểu đồ tròn tỷ trọng dùng COLOR_MAP
  fig_pie = px.pie(
      df_summary,
      names="segment_name",
      values="customer_count",
      title="Tỷ trọng khách hàng theo Phân khúc",
      color="segment_name",
      color_discrete_map=COLOR_MAP,
      hole=0.4,
  )
  st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 2: CHI TIẾT ---
with tab2:
  # Biểu đồ Bar Monetary có định dạng tiền tệ R$ và đồng bộ màu
  fig_monetary = px.bar(
      df_summary,
      x="segment_name",
      y="avg_monetary",
      color="segment_name",
      color_discrete_map=COLOR_MAP,
      title="Chi tiêu trung bình (Monetary - R$)",
      text_auto=".2f",
  )
  fig_monetary.update_layout(showlegend=False)
  st.plotly_chart(fig_monetary, use_container_width=True)

  # Hiển thị bảng dữ liệu sạch
  st.dataframe(df_summary, use_container_width=True)

# --- TAB 3: ĐỀ XUẤT MARKETING ---
with tab3:
  st.subheader("🎯 Kịch Bản Hành Động Chi Tiết")
  for segment, action in MARKETING_ACTION.items():
    with st.expander(f"📌 Phân khúc: **{segment}**"):
      st.write(f"👉 **Hành động đề xuất:** {action}")
