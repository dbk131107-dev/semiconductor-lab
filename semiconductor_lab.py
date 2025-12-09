import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Phòng Lab Bán Dẫn - Đại học CMC",
    page_icon="💾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Tùy chỉnh để làm đẹp giao diện ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0056b3;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        border-bottom: 2px solid #0056b3;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0056b3;
    }
    .formula-box {
        background-color: #fff0f5;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.image("https://img.icons8.com/color/96/000000/microchip.png", width=80)
st.sidebar.title("CMC Semiconductor Lab")
st.sidebar.markdown("**Sinh viên thực hiện:** [Tên Của Bạn]")
st.sidebar.markdown("**Đơn vị:** Đại học CMC (CMC University)")
st.sidebar.markdown("---")
page = st.sidebar.radio("Chọn quy trình:", 
    ["Giới thiệu chung", "Oxy hóa (Oxidation)", "Quang khắc (Lithography)", "Ăn mòn (Etching)", "Mô phỏng Fab (Simulation)"])

# --- Hàm vẽ Wafer (Đã sửa lỗi và nâng cấp) ---
def draw_wafer(step, params=None):
    """
    Hàm vẽ mặt cắt ngang của Wafer dựa trên bước quy trình.
    """
    fig = go.Figure()
    
    # Cấu hình trục
    fig.update_xaxes(range=[0, 10], showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(range=[0, 8], showgrid=False, zeroline=False, visible=False)
    
    # 1. Silicon Substrate (Luôn có)
    fig.add_shape(type="rect", x0=1, y0=0, x1=9, y1=2, 
                  fillcolor="lightgray", line=dict(color="gray"), name="Silicon Substrate")
    fig.add_annotation(x=5, y=1, text="Si Substrate", showarrow=False)

    # Xử lý từng bước
    if step >= 1: # Oxidation
        oxide_thickness = params.get('oxide_h', 0.5) if params else 1.0
        fig.add_shape(type="rect", x0=1, y0=2, x1=9, y1=2+oxide_thickness, 
                      fillcolor="#a8dbf0", line=dict(color="blue"), name="SiO2")
        fig.add_annotation(x=8.5, y=2+oxide_thickness/2, text="SiO2", showarrow=False, font=dict(size=10))

    if step >= 2: # Spin Coat Photoresist
        pr_thickness = 1.0
        base_y = 2 + (params.get('oxide_h', 0.5) if params else 1.0)
        fig.add_shape(type="rect", x0=1, y0=base_y, x1=9, y1=base_y+pr_thickness, 
                      fillcolor="#ffcccb", line=dict(color="red"), name="Photoresist")
        fig.add_annotation(x=2, y=base_y+pr_thickness/2, text="PR", showarrow=False, font=dict(size=10))

    if step == 3: # Exposure (UV Light) - KHẮC PHỤC LỖI TẠI ĐÂY
        base_y = 2 + (params.get('oxide_h', 0.5) if params else 1.0) + 1.0
        # Mask
        fig.add_shape(type="rect", x0=1, y0=base_y+1, x1=3, y1=base_y+1.2, fillcolor="black")
        fig.add_shape(type="rect", x0=7, y0=base_y+1, x1=9, y1=base_y+1.2, fillcolor="black")
        
        # UV Arrows (Đã sửa arrowheader -> arrowhead)
        for x in [4, 5, 6]:
            fig.add_annotation(
                x=x, y=base_y+0.2, ax=x, ay=base_y+2,
                arrowhead=2, # Đã sửa từ arrowheader
                arrowcolor="purple", arrowsize=1.5,
                text="UV Light" if x==5 else ""
            )

    if step >= 4: # Developed (Removed exposed PR)
        base_y = 2 + (params.get('oxide_h', 0.5) if params else 1.0)
        # Vẽ lại PR nhưng bị khuyết ở giữa
        fig.add_shape(type="rect", x0=1, y0=base_y, x1=3, y1=base_y+1, fillcolor="#ffcccb", line=dict(color="red"))
        fig.add_shape(type="rect", x0=7, y0=base_y, x1=9, y1=base_y+1, fillcolor="#ffcccb", line=dict(color="red"))
        # Clear vùng giữa (chỉ là không vẽ gì hoặc vẽ background đè lên nếu cần, ở đây không vẽ là đủ)

    if step >= 5: # Etching (Etched Oxide)
        ox_h = params.get('oxide_h', 0.5) if params else 1.0
        # Vẽ lại Oxide nhưng bị khuyết
        # Thay vì vẽ 1 cục lớn, vẽ 2 cục nhỏ 2 bên
        fig.data = [] # Xóa hết vẽ lại cho dễ xử lý lớp oxide bị cắt
        # Base
        fig.add_shape(type="rect", x0=1, y0=0, x1=9, y1=2, fillcolor="lightgray", line=dict(color="gray"))
        fig.add_annotation(x=5, y=1, text="Si Substrate", showarrow=False)
        
        # Etched Oxide
        fig.add_shape(type="rect", x0=1, y0=2, x1=3, y1=2+ox_h, fillcolor="#a8dbf0", line=dict(color="blue"))
        fig.add_shape(type="rect", x0=7, y0=2, x1=9, y1=2+ox_h, fillcolor="#a8dbf0", line=dict(color="blue"))
        
        if step == 5: # Vẫn còn PR
            fig.add_shape(type="rect", x0=1, y0=2+ox_h, x1=3, y1=2+ox_h+1, fillcolor="#ffcccb", line=dict(color="red"))
            fig.add_shape(type="rect", x0=7, y0=2+ox_h, x1=9, y1=2+ox_h+1, fillcolor="#ffcccb", line=dict(color="red"))
            # Mũi tên Plasma
            for x in [4, 5, 6]:
                 fig.add_annotation(x=x, y=2.5, ax=x, ay=5, arrowhead=2, arrowcolor="green", text="Plasma" if x==5 else "")

    if step == 6: # Strip PR (Hoàn thành)
        # Chỉ còn Si và Oxide đã bị ăn mòn
        pass # Code ở step 5 đã vẽ oxide bị ăn mòn, chỉ cần không vẽ PR là được (logic ở trên đã xử lý)

    fig.update_layout(
        title=f"Mô phỏng mặt cắt Wafer - Bước {step}",
        plot_bgcolor="white",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# --- NỘI DUNG CHÍNH ---

st.markdown('<div class="main-header">Phòng Thí Nghiệm Công Nghệ Bán Dẫn</div>', unsafe_allow_html=True)
st.write("Chào mừng đến với hệ thống mô phỏng quy trình chế tạo IC. Ứng dụng được phát triển bởi sinh viên **Đại học CMC**.")

if page == "Giới thiệu chung":
    st.markdown("### Quy trình chế tạo IC cơ bản")
    st.markdown("""
    Chế tạo chất bán dẫn là quy trình sản xuất các thiết bị MOS (Metal Oxide Semiconductor) và chip máy tính.
    Quy trình bao gồm 4 bước lặp đi lặp lại chính:
    1.  **Oxy hóa (Oxidation/Deposition):** Tạo lớp vật liệu mỏng (SiO2).
    2.  **Quang khắc (Lithography):** Chuyển mẫu thiết kế từ mặt nạ (mask) sang wafer.
    3.  **Ăn mòn (Etching):** Loại bỏ vật liệu không mong muốn.
    4.  **Cấy Ion/Khuếch tán (Doping):** Thay đổi tính chất điện của vật liệu.
    """)
    st.info("Hãy chọn các mục bên menu trái để tìm hiểu chi tiết từng bước và thực hiện tính toán.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Czochralski_Process.svg/1200px-Czochralski_Process.svg.png", caption="Quy trình Czochralski tạo tinh thể Si", width=400)

elif page == "Oxy hóa (Oxidation)":
    st.markdown('<div class="sub-header">Quá trình Oxy hóa Nhiệt (Thermal Oxidation)</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Lý thuyết")
        st.write("""
        Oxy hóa nhiệt là quá trình tạo ra lớp Silicon Dioxide ($SiO_2$) trên bề mặt phiến Silicon ở nhiệt độ cao (800°C - 1200°C).
        Lớp $SiO_2$ đóng vai trò là lớp cách điện hoặc lớp mặt nạ cho quá trình cấy ion.
        
        Có hai phương pháp chính:
        * **Oxy hóa khô (Dry Oxidation):** $Si + O_2 \\rightarrow SiO_2$ (Chậm, chất lượng cao).
        * **Oxy hóa ướt (Wet Oxidation):** $Si + 2H_2O \\rightarrow SiO_2 + 2H_2$ (Nhanh, xốp hơn).
        """)
        
        st.markdown("#### Mô hình Deal-Grove")
        st.latex(r"x_0^2 + A x_0 = B(t + \tau)")
        st.write("""
        Trong đó:
        * $x_0$: Độ dày oxide cần tạo.
        * $t$: Thời gian oxy hóa.
        * $B$: Hằng số tốc độ parabol (Parabolic rate constant).
        * $B/A$: Hằng số tốc độ tuyến tính (Linear rate constant).
        * $\\tau$: Thời gian hiệu chỉnh ban đầu.
        """)

    with col2:
        st.markdown("#### Tính toán Độ dày Oxide")
        method = st.selectbox("Phương pháp", ["Oxy hóa Khô (1000°C)", "Oxy hóa Ướt (1000°C)"])
        time_min = st.slider("Thời gian (phút)", 0, 300, 60)
        
        # Giả định hằng số (đơn vị: um^2/hr và um/hr) tại 1000 độ C
        if "Khô" in method:
            B = 0.0117 
            BA = 0.057 # B/A
        else:
            B = 0.287
            BA = 1.63 # B/A (Nhanh hơn nhiều)
            
        # Tính toán Deal-Grove đơn giản hóa: t = x^2/B + x/(B/A) -> Giải phương trình bậc 2 tìm x theo t
        # Ax^2 + Bx - C = 0 (Chuyển đổi đơn vị cẩn thận)
        # Ở đây dùng xấp xỉ tuyến tính + parabol đơn giản để minh họa
        t_hours = time_min / 60.0
        # Giải pt: x^2 + Ax = Bt (bỏ qua tau cho đơn giản)
        # x^2 + (B/ (B/A)) * x - B*t = 0
        A_const = B / BA
        delta = A_const**2 + 4 * 1 * (B * t_hours)
        thickness = (-A_const + np.sqrt(delta)) / 2 # micromet
        
        thickness_nm = thickness * 1000
        
        st.success(f"Độ dày lớp Oxide dự kiến: **{thickness_nm:.2f} nm**")
        st.progress(min(thickness_nm/1000, 1.0))
        
        # Vẽ biểu đồ tăng trưởng
        t_range = np.linspace(0, 5, 50) # 5 giờ
        x_range = (-A_const + np.sqrt(A_const**2 + 4 * B * t_range)) / 2 * 1000
        
        fig_chart = go.Figure()
        fig_chart.add_trace(go.Scatter(x=t_range*60, y=x_range, mode='lines', name=method))
        fig_chart.update_layout(title="Độ dày Oxide theo thời gian", xaxis_title="Thời gian (phút)", yaxis_title="Độ dày (nm)")
        st.plotly_chart(fig_chart, use_container_width=True)

elif page == "Quang khắc (Lithography)":
    st.markdown('<div class="sub-header">Quang khắc (Photolithography)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    Quang khắc là quá trình sử dụng ánh sáng để chuyển một mẫu hình học từ mặt nạ quang (photomask) sang lớp chất cảm quang (photoresist) trên bề mặt wafer.
    Đây là bước quan trọng nhất quyết định kích thước nhỏ nhất (CD - Critical Dimension) của chip.
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["Quy trình", "Độ phân giải (Resolution)"])
    
    with tabs[0]:
        st.write("1. **Spin Coating:** Phủ lớp chất cảm quang (PR).")
        st.write("2. **Exposure:** Chiếu tia UV qua mặt nạ.")
        st.write("3. **Development:** Loại bỏ phần PR đã bị chiếu sáng (với Positive PR).")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Photolithography_process_steps.svg/800px-Photolithography_process_steps.svg.png", caption="Các bước quang khắc")
        
    with tabs[1]:
        st.markdown("#### Tiêu chuẩn Rayleigh")
        st.latex(r"R = k_1 \frac{\lambda}{NA}")
        st.write("""
        Để tạo ra chip nhỏ hơn (R nhỏ), chúng ta cần:
        * Giảm bước sóng ánh sáng ($\lambda$): UV (365nm) -> DUV (193nm) -> EUV (13.5nm).
        * Tăng khẩu độ số ($NA$): Dùng thấu kính lớn hơn hoặc ngâm trong nước (Immersion).
        """)
        
        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            wavelength = st.selectbox("Bước sóng ánh sáng (nm)", [365, 248, 193, 13.5])
            na = st.slider("Khẩu độ số (NA)", 0.5, 1.35, 0.9)
            k1 = st.number_input("Hệ số quy trình (k1)", 0.25, 0.8, 0.4)
        with col_calc2:
            res = k1 * wavelength / na
            st.metric(label="Độ phân giải tối thiểu (Critical Dimension)", value=f"{res:.2f} nm")
            if res < 20:
                st.success("Công nghệ siêu cao cấp (High-end Node)")
            elif res < 100:
                st.warning("Công nghệ tiên tiến")
            else:
                st.info("Công nghệ cũ")

elif page == "Ăn mòn (Etching)":
    st.markdown('<div class="sub-header">Ăn mòn (Etching)</div>', unsafe_allow_html=True)
    st.write("Sau khi quang khắc, chúng ta cần loại bỏ lớp vật liệu bên dưới (ví dụ SiO2) tại các vùng không được che chắn bởi Photoresist.")
    
    col_etch1, col_etch2 = st.columns(2)
    with col_etch1:
        st.subheader("Wet Etching (Ăn mòn ướt)")
        st.write("- Sử dụng dung dịch hóa chất (VD: HF để ăn mòn SiO2).")
        st.write("- **Isotropic (Đẳng hướng):** Ăn mòn theo mọi hướng, tạo ra undercut.")
        st.write("- Rẻ, nhanh, nhưng độ chính xác thấp.")
        
    with col_etch2:
        st.subheader("Dry Etching (Ăn mòn khô / Plasma)")
        st.write("- Sử dụng khí ion hóa (Plasma).")
        st.write("- **Anisotropic (Dị hướng):** Ăn mòn chủ yếu theo chiều thẳng đứng.")
        st.write("- Độ chính xác cao, dùng cho các node công nghệ nhỏ.")

    st.markdown("#### Tính toán tốc độ ăn mòn")
    thickness_to_etch = st.number_input("Độ dày cần ăn mòn (nm)", value=500)
    etch_rate = st.number_input("Tốc độ ăn mòn (nm/phút)", value=50)
    over_etch = st.slider("Over-etch (%)", 0, 50, 10, help="Ăn mòn thêm để đảm bảo sạch hoàn toàn")
    
    total_time = (thickness_to_etch / etch_rate) * (1 + over_etch/100)
    st.write(f"Thời gian ăn mòn cần thiết: **{total_time:.2f} phút**")

elif page == "Mô phỏng Fab (Simulation)":
    st.markdown('<div class="sub-header">Mô phỏng Quy trình Fab (Interactive)</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Điều khiển Mô phỏng")
    
    # Trạng thái mô phỏng
    step_mapping = {
        0: "Bắt đầu (Substrate)",
        1: "1. Oxy hóa (Tạo SiO2)",
        2: "2. Phủ PR (Spin Coating)",
        3: "3. Chiếu xạ (Exposure - UV)",
        4: "4. Hiện hình (Development)",
        5: "5. Ăn mòn (Etching)",
        6: "6. Loại bỏ PR (Stripping)"
    }
    
    selected_step_idx = st.sidebar.slider("Chọn bước quy trình:", 0, 6, 0)
    st.subheader(step_mapping[selected_step_idx])
    
    # Hiển thị mô phỏng hình ảnh
    # Truyền tham số giả định oxide height để vẽ cho đẹp
    fig = draw_wafer(selected_step_idx, params={'oxide_h': 1.0})
    st.plotly_chart(fig, use_container_width=True)
    
    # Giải thích ngữ cảnh theo từng bước
    if selected_step_idx == 0:
        st.info("Bắt đầu với phiến Silicon (Si Wafer) tinh khiết đã được làm sạch.")
    elif selected_step_idx == 1:
        st.info("Lớp SiO2 màu xanh được mọc lên bề mặt Si để bảo vệ hoặc cách điện.")
    elif selected_step_idx == 2:
        st.info("Phủ một lớp Photoresist (PR - màu đỏ) nhạy sáng lên trên lớp Oxide.")
    elif selected_step_idx == 3:
        st.error("Chiếu tia UV qua mặt nạ (Mask). Phần PR bị chiếu sáng sẽ thay đổi tính chất hóa học.")
        st.markdown("**Lưu ý:** Đây là bước bạn gặp lỗi trước đó. Tôi đã sửa lại mã lệnh vẽ mũi tên (UV) để không bị lỗi `arrowheader`.")
    elif selected_step_idx == 4:
        st.info("Rửa wafer trong dung dịch Developer. Phần PR bị chiếu sáng tan đi, lộ ra lớp Oxide bên dưới.")
    elif selected_step_idx == 5:
        st.warning("Dùng Plasma hoặc Axit để ăn mòn lớp Oxide lộ ra. Lớp PR còn lại bảo vệ phần Oxide bên dưới nó.")
    elif selected_step_idx == 6:
        st.success("Loại bỏ lớp PR còn lại. Kết quả là mẫu thiết kế đã được chuyển sang lớp Oxide thành công!")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>© 2025 Đại học CMC. Ứng dụng hỗ trợ học tập môn Công nghệ Bán dẫn.</div>", 
    unsafe_allow_html=True
)
    page_fab()


