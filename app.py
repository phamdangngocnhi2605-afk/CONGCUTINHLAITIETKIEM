import pandas as pd
import streamlit as st
st.image("logo.jpg")

st.set_page_config(page_title="APPCONGCUTINHLAIGUIVAY_NGUYENTHITHUYVY
, page_icon="💰", layout="centered")

st.title("💰 Công Cụ Tính Lãi Gửi Tiết Kiệm")
st.write("Nhập thông tin khoản gửi bên dưới để tính toán tiền lãi chi tiết.")

# --- BẢNG ĐIỀU KHIỂN NHẬP DỮ LIỆU ---
st.header("⚙️ Thông tin khoản gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien_gai = st.number_input(
        "Số tiền gửi (VNĐ):",
        min_value=1_000_000,
        value=100_000_000,
        step=1_000_000,
        format="%d",
    )
    ky_han_thang = st.number_input(
        "Kỳ hạn gửi (tháng):", min_value=1, max_value=120, value=12, step=1
    )
    loai_lai = st.radio("Phương pháp tính lãi:", ["Lãi kép", "Lãi đơn"])

with col2:
    lai_suat_nam = st.number_input(
        "Lãi suất (%/năm):",
        min_value=0.1,
        max_value=20.0,
        value=6.0,
        step=0.1,
        format="%.2f",
    )
    hinh_thuc_nhan = st.selectbox(
        "Hình thức nhận lãi:",
        ["Cuối kỳ", "Hàng tháng", "Hàng quý"],
    )

# --- XỬ LÝ TÍNH TOÁN ---
# Xác định số kỳ trả lãi trong 1 năm và độ dài mỗi kỳ (tính theo tháng)
ky_tra_lai_thang = 1
if hinh_thuc_nhan == "Hàng tháng":
    ky_tra_lai_thang = 1
elif hinh_thuc_nhan == "Hàng quý":
    ky_tra_lai_thang = 3
else:  # Cuối kỳ
    ky_tra_lai_thang = ky_han_thang

# Tổng số kỳ nhận lãi
tong_so_ky = ky_han_thang / ky_tra_lai_thang

# Lãi suất theo từng kỳ nhận lãi
lai_suat_ky = (lai_suat_nam / 100) * (ky_tra_lai_thang / 12)

# Khởi tạo bảng chi tiết
lich_su = []
goc_hien_tai = so_tien_gai
tong_lai = 0.0

if loai_lai == "Lãi đơn" or hinh_thuc_nhan != "Cuối kỳ":
    # Trường hợp Lãi đơn HOẶC Nhận lãi định kỳ (tháng/quý rút lãi ra, gốc giữ nguyên)
    # Lưu ý: Nhận lãi định kỳ rút tiền ra ngoài nên bản chất tiền gốc không tăng hợp trội.
    lai_dinh_ky = so_tien_gai * lai_suat_ky
    tong_lai = lai_dinh_ky * tong_so_ky

    # Tạo lịch trình chi tiết từng tháng
    for t in range(1, ky_han_thang + 1):
        nhan_lai_thang_nay = 0.0
        if t % ky_tra_lai_thang == 0:
            nhan_lai_thang_nay = lai_dinh_ky

        lich_su.append(
            {
                "Tháng": t,
                "Tiền gốc (VNĐ)": so_tien_gai,
                "Tiền lãi nhận (VNĐ)": nhan_lai_thang_nay,
                "Tổng tiền lũy kế (VNĐ)": so_tien_gai
                + (t / ky_tra_lai_thang) * lai_dinh_ky,
            }
        )

else:
    # Trường hợp Lãi kép gửi Cuối kỳ (nhập lãi vào gốc hàng tháng/quý)
    # Mặc định với kỳ hạn ngắn hơn 1 năm, lãi kép tính cộng dồn định kỳ theo tháng/quý
    tong_goc_lai = so_tien_gai * ((1 + lai_suat_ky) ** tong_so_ky)
    tong_lai = tong_goc_lai - so_tien_gai
    lai_dinh_ky = tong_lai / tong_so_ky  # Trung bình mỗi kỳ

    so_ky_da_qua = 0
    goc_tich_luy = so_tien_gai

    for t in range(1, ky_han_thang + 1):
        nhan_lai_thang_nay = 0.0
        if t % ky_tra_lai_thang == 0:
            nhan_lai_thang_nay = goc_tich_luy * lai_suat_ky
            goc_tich_luy += nhan_lai_thang_nay

        lich_su.append(
            {
                "Tháng": t,
                "Tiền gốc (VNĐ)": goc_tich_luy - nhan_lai_thang_nay
                if nhan_lai_thang_nay > 0
                else goc_tich_luy,
                "Tiền lãi nhận (VNĐ)": nhan_lai_thang_nay,
                "Tổng tiền lũy kế (VNĐ)": goc_tich_luy,
            }
        )

tong_goc_va_lai = so_tien_gai + tong_lai

# --- HIỂN THỊ KẾT QUẢ ---
st.markdown("---")
st.header("📊 Kết quả dự tính")

col_res1, col_res2, col_res3 = st.columns(3)

with col_res1:
    st.metric(
        label="Tiền lãi định kỳ",
        value=f"{lai_dinh_ky:,.0f} VNĐ",
        help=f"Mỗi {ky_tra_lai_thang} tháng nhận 1 lần",
    )

with col_res2:
    st.metric(
        label="Tổng tiền lãi",
        value=f"{tong_lai:,.0f} VNĐ",
    )

with col_res3:
    st.metric(
        label="Tổng Tiền Gốc + Lãi",
        value=f"{tong_goc_va_lai:,.0f} VNĐ",
    )

# --- BIỂU ĐỒ & BẢNG CHI TIẾT ---
st.subheader("📈 Lịch trình tăng trưởng khoản tiền")

df = pd.DataFrame(lich_su)

# Hiển thị biểu đồ đường tổng tiền lũy kế
st.line_chart(df, x="Tháng", y="Tổng tiền lũy kế (VNĐ)")

# Bảng chi tiết từng tháng
with st.expander("🔍 Xem lịch nhận lãi chi tiết từng tháng"):
    df_formatted = df.copy()
    for col in [
        "Tiền gốc (VNĐ)",
        "Tiền lãi nhận (VNĐ)",
        "Tổng tiền lũy kế (VNĐ)",
    ]:
        df_formatted[col] = df_formatted[col].map("{:,.0f}".format)
    st.dataframe(df_formatted, use_container_width=True)
