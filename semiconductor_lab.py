import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# CẤU HÌNH TRANG (PAGE CONFIG)
# ==========================================
st.set_page_config(
    page_title="Virtual Semiconductor Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CSS TÙY CHỈNH (CHO GIAO DIỆN ĐẸP HƠN)
# ==========================================
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #4F8BF9; font-weight: bold;}
    .sub-header {font-size: 1.5rem; color: #333;}
    .highlight {background-color: #f0f2f6; padding: 10px; border-radius: 10px;}
    .stButton>button {width: 100%;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# MODULE 1: CALCULATOR (CÔNG CỤ TÍNH TOÁN)
# ==========================================
def page_calculator():
    st.markdown('<p class="main-header">🧮 Web Tính Toán Linh Kiện</p>', unsafe_allow_html=True)
    st.write("Công cụ tính toán nhanh cho các định luật cơ bản.")

    tab1, tab2 = st.tabs(["Định luật Ohm", "Mã màu điện trở"])

    with tab1:
        st.subheader("Tính toán Định luật Ohm (V = I * R)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            cal_type = st.selectbox("Bạn muốn tính gì?", ["Điện áp (V)", "Dòng điện (I)", "Điện trở (R)"])
        
        with col2:
            if cal_type == "Điện áp (V)":
                i_val = st.number_input("Dòng điện I (Ampe)", value=1.0)
                r_val = st.number_input("Điện trở R (Ohm)", value=100.0)
                result = i_val * r_val
                unit = "V"
            elif cal_type == "Dòng điện (I)":
                v_val = st.number_input("Điện áp V (Volt)", value=5.0)
                r_val = st.number_input("Điện trở R (Ohm)", value=100.0)
                result = v_val / r_val if r_val != 0 else 0
                unit = "A"
            else:
                v_val = st.number_input("Điện áp V (Volt)", value=5.0)
                i_val = st.number_input("Dòng điện I (Ampe)", value=0.05)
                result = v_val / i_val if i_val != 0 else 0
                unit = "Ω"
        
        with col3:
            st.markdown("### Kết quả:")
            st.markdown(f"<h2 style='color: green;'>{result:.4f} {unit}</h2>", unsafe_allow_html=True)

    with tab2:
        st.subheader("Tra cứu mã màu điện trở (4 vạch)")
        colors = {
            "Đen (0)": 0, "Nâu (1)": 1, "Đỏ (2)": 2, "Cam (3)": 3, "Vàng (4)": 4,
            "Lục (5)": 5, "Lam (6)": 6, "Tím (7)": 7, "Xám (8)": 8, "Trắng (9)": 9
        }
        multiplier = {
            "Đen (x1)": 1, "Nâu (x10)": 10, "Đỏ (x100)": 100, "Cam (x1k)": 1000, 
            "Vàng (x10k)": 10000, "Lục (x100k)": 100000, "Lam (x1M)": 1000000
        }
        
        c1, c2, c3 = st.columns(3)
        with c1: band1 = st.selectbox("Vạch 1", options=list(colors.keys()), index=1)
        with c2: band2 = st.selectbox("Vạch 2", options=list(colors.keys()), index=0)
        with c3: band3 = st.selectbox("Vạch 3 (Hệ số nhân)", options=list(multiplier.keys()), index=2)
        
        res_val = (colors[band1] * 10 + colors[band2]) * multiplier[band3]
        
        st.success(f"Giá trị điện trở: **{res_val:,} Ω** (hoặc {res_val/1000} kΩ)")

# ==========================================
# MODULE 2: LOGIC SIMULATOR (MÔ PHỎNG LOGIC)
# ==========================================
def page_logic_sim():
    st.markdown('<p class="main-header">🔌 Mô phỏng Cổng Logic</p>', unsafe_allow_html=True)
    st.write("Trực quan hóa hoạt động của các cổng logic số cơ bản.")

    col_control, col_display = st.columns([1, 2])

    with col_control:
        st.markdown("### Cấu hình")
        gate_type = st.selectbox("Chọn cổng Logic", ["AND", "OR", "NAND", "NOR", "XOR"])
        input_a = st.toggle("Input A (0/1)", value=False)
        input_b = st.toggle("Input B (0/1)", value=False)

    # Xử lý Logic
    a = 1 if input_a else 0
    b = 1 if input_b else 0
    out = 0
    
    if gate_type == "AND": out = a & b
    elif gate_type == "OR": out = a | b
    elif gate_type == "NAND": out = not (a & b)
    elif gate_type == "NOR": out = not (a | b)
    elif gate_type == "XOR": out = a ^ b
    
    out = 1 if out else 0

    with col_display:
        st.markdown("### Kết quả Mô phỏng")
        
        # Vẽ sơ đồ đơn giản bằng columns và emoji
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            st.metric("Input A", value=a)
            st.metric("Input B", value=b)
        with c2:
            st.markdown(f"<div style='text-align:center; padding-top:20px; font-size:40px;'>➡️ {gate_type} ➡️</div>", unsafe_allow_html=True)
        with c3:
            st.metric("Output Y", value=out, delta="High" if out else "Low")
            
        # Hiển thị bảng chân trị (Truth Table)
        st.markdown("#### Bảng chân trị (Truth Table):")
        data = []
        for ia in [0, 1]:
            for ib in [0, 1]:
                res = 0
                if gate_type == "AND": res = ia & ib
                elif gate_type == "OR": res = ia | ib
                elif gate_type == "NAND": res = int(not(ia & ib))
                elif gate_type == "NOR": res = int(not(ia | ib))
                elif gate_type == "XOR": res = ia ^ ib
                
                # Highlight dòng hiện tại
                status = "👈 Hiện tại" if (ia == a and ib == b) else ""
                data.append([ia, ib, res, status])
                
        df = pd.DataFrame(data, columns=["A", "B", "Y (Out)", "Trạng thái"])
        st.dataframe(df, use_container_width=True)

# ==========================================
# MODULE 3: I-V PLOTTER (ĐẶC TUYẾN V-A)
# ==========================================
def page_iv_plotter():
    st.markdown('<p class="main-header">📈 Vẽ Đặc Tuyến V-A (I-V Plotter)</p>', unsafe_allow_html=True)
    st.markdown("Mô phỏng đặc tuyến Volt-Ampe của tiếp giáp P-N (Diode).")

    # Sidebar điều khiển tham số
    with st.expander("🛠️ Điều chỉnh thông số vật lý", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            temp_c = st.slider("Nhiệt độ (Celsius)", -50, 150, 27)
            is_sat = st.slider("Dòng bão hòa ngược Is (pA)", 1.0, 100.0, 10.0) * 1e-12
        with col2:
            n_factor = st.slider("Hệ số lý tưởng (Ideality Factor n)", 1.0, 2.0, 1.5)
            v_max = st.slider("Điện áp tối đa (V)", 0.5, 2.0, 1.0)

    # Tính toán vật lý
    k = 1.380649e-23  # Boltzmann constant
    q = 1.60217663e-19 # Elementary charge
    temp_k = temp_c + 273.15
    vt = (k * temp_k) / q # Thermal voltage

    # Tạo dữ liệu
    v_range = np.linspace(-1.0, v_max, 500)
    # Phương trình Shockley Diode: I = Is * (exp(V / (n*Vt)) - 1)
    i_range = is_sat * (np.exp(v_range / (n_factor * vt)) - 1)

    # Vẽ biểu đồ bằng Matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(v_range, i_range * 1000, color='blue', linewidth=2, label=f'Diode @ {temp_c}°C')
    ax.set_title("Đặc tuyến I-V của Diode")
    ax.set_xlabel("Điện áp V (Volt)")
    ax.set_ylabel("Dòng điện I (mA)")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.legend()

    # Hiển thị trên Streamlit
    st.pyplot(fig)
    
    st.info(f"""
    **Thông số tính toán:**
    - Nhiệt độ T = {temp_k:.2f} K
    - Điện áp nhiệt Vt = {vt:.4f} V
    """)

# ==========================================
# MODULE 4: WIKI (KHO TRI THỨC)
# ==========================================
def page_wiki():
    st.markdown('<p class="main-header">📚 Wiki Bán Dẫn Cá Nhân</p>', unsafe_allow_html=True)
    
    topics = {
        "Chất bán dẫn (Semiconductor)": """
        **Định nghĩa:** Là vật liệu có độ dẫn điện nằm giữa chất dẫn điện (như đồng) và chất cách điện (như thủy tinh).
        
        **Đặc điểm:** Độ dẫn điện có thể thay đổi nhờ:
        * Nhiệt độ
        * Ánh sáng
        * Pha tạp chất (Doping)
        
        **Ví dụ:** Silicon (Si), Germanium (Ge), Gallium Arsenide (GaAs).
        """,
        "Vùng năng lượng (Band Theory)": r"""
        Trong vật lý chất rắn, các trạng thái năng lượng của electron hình thành các vùng:
        
        1. **Valence Band (Vùng hóa trị):** Chứa các electron liên kết.
        2. **Conduction Band (Vùng dẫn):** Chứa các electron tự do dẫn điện.
        3. **Band Gap ($E_g$):** Khoảng cách năng lượng giữa vùng hóa trị và vùng dẫn.
        
        $$ E_g(\text{Si}) \approx 1.12 \text{ eV} $$
        """,
        "Pha tạp (Doping)": """
        Quá trình thêm tạp chất vào mạng tinh thể tinh khiết để thay đổi tính chất điện.
        
        * **Loại n (n-type):** Pha tạp chất nhóm V (P, As) $\rightarrow$ dư Electron.
        * **Loại p (p-type):** Pha tạp chất nhóm III (B, Ga) $\rightarrow$ dư Lỗ trống (Holes).
        """
    }

    selection = st.selectbox("Chọn chủ đề cần tra cứu:", list(topics.keys()))
    
    st.markdown("---")
    st.markdown(f"## {selection}")
    st.markdown(topics[selection])
    
    if selection == "Vùng năng lượng (Band Theory)":
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Band_structure_filling_diagram.svg/440px-Band_structure_filling_diagram.svg.png", caption="Cấu trúc vùng năng lượng")

# ==========================================
# MODULE 5: FAB PROCESS (QUY TRÌNH SẢN XUẤT)
# ==========================================
def page_fab_process():
    st.markdown('<p class="main-header">🏭 Quy trình Sản xuất Chip (Fab)</p>', unsafe_allow_html=True)
    st.write("Mô phỏng quy trình Photolithography cơ bản.")

    steps = ["1. Chuẩn bị Wafer", "2. Oxi hóa (Oxidation)", "3. Phủ quang trở (Photoresist)", 
             "4. Chiếu sáng (Exposure)", "5. Ăn mòn (Etching)", "6. Loại bỏ quang trở"]
    
    selected_step = st.radio("Chọn bước trong quy trình:", steps)

    st.markdown("---")
    
    col_img, col_desc = st.columns([1, 1])
    
    with col_desc:
        st.subheader(f"Chi tiết: {selected_step}")
        if "1" in selected_step:
            st.write("Wafer Silicon tinh khiết được cắt ra từ thanh đơn tinh thể (Ingot). Bề mặt được đánh bóng như gương.")
        elif "2" in selected_step:
            st.write("Tạo một lớp $SiO_2$ mỏng trên bề mặt wafer để cách điện và bảo vệ.")
            st.latex(r"Si + O_2 \xrightarrow{Heat} SiO_2")
        elif "3" in selected_step:
            st.write("Phủ một lớp hóa chất nhạy sáng (Photoresist) lên bề mặt wafer bằng phương pháp quay (Spin coating).")
        elif "4" in selected_step:
            st.write("Ánh sáng UV chiếu qua mặt nạ (Mask) xuống wafer. Phần quang trở tiếp xúc ánh sáng sẽ thay đổi tính chất hóa học.")
        elif "5" in selected_step:
            st.write("Dùng hóa chất hoặc plasma để ăn mòn lớp $SiO_2$ tại những nơi không được quang trở bảo vệ.")
        elif "6" in selected_step:
            st.write("Loại bỏ lớp quang trở còn thừa, để lại mẫu mạch in trên lớp $SiO_2$.")

    with col_img:
        # Trong thực tế bạn sẽ dùng ảnh thật, ở đây dùng placeholder minh họa
        st.info(f"Đang hiển thị mô phỏng bước: {selected_step}")
        st.progress((steps.index(selected_step) + 1) / len(steps))
        st.warning("Imagine a simplified animation of the cross-section here.")


# ==========================================
# TRANG CHỦ & ĐIỀU HƯỚNG
# ==========================================
def main():
    # Sidebar Menu
    st.sidebar.title("Virtual Lab 🔬")
    st.sidebar.info("Sinh viên: Năm Nhất Bán Dẫn")
    
    menu = ["Trang chủ", "1. Calculator 🧮", "2. Wiki Kiến thức 📚", 
            "3. I-V Plotter 📈", "4. Fab Process 🏭", "5. Logic Sim 🔌"]
    choice = st.sidebar.radio("Điều hướng Modules", menu)

    # Router logic
    if choice == "Trang chủ":
        st.markdown('<p class="main-header">Chào mừng đến với Virtual Semiconductor Lab 🚀</p>', unsafe_allow_html=True)
        st.markdown("""
        Đây là dự án học tập tích hợp các công cụ hỗ trợ ngành Kỹ thuật Bán dẫn.
        
        ### Các phân khu chức năng:
        1.  **Utilities:** Tính toán nhanh điện trở, định luật Ohm.
        2.  **Knowledge Base:** Wiki cá nhân lưu trữ kiến thức.
        3.  **Visualization:** Vẽ đặc tuyến I-V của Diode/Transistor.
        4.  **Process:** Mô phỏng quy trình sản xuất Chip.
        5.  **Simulation:** Mô phỏng mạch số Digital Logic.
        
        👈 **Hãy chọn một module bên menu trái để bắt đầu!**
        """)
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Semiconductor_production_line.jpg/640px-Semiconductor_production_line.jpg", caption="Phòng sạch sản xuất bán dẫn")
        
    elif "1" in choice:
        page_calculator()
    elif "2" in choice:
        page_wiki()
    elif "3" in choice:
        page_iv_plotter()
    elif "4" in choice:
        page_fab_process()
    elif "5" in choice:
        page_logic_sim()

if __name__ == "__main__":
    main()