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

# --- CSS Tùy chỉnh (Giao diện đẹp) ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #0056b3;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px #d0e4f5;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #333;
        border-bottom: 3px solid #0056b3;
        padding-bottom: 8px;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #0056b3;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .calc-box {
        background-color: #fdf5e6;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #f0e68c;
    }
    .stButton>button {
        width: 100%;
        background-color: #0056b3;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.image("https://img.icons8.com/color/96/000000/microchip.png", width=80)
st.sidebar.title("CMC Semiconductor Lab")
st.sidebar.markdown("**Sinh viên thực hiện:** [Tên Của Bạn]")
st.sidebar.markdown("**Đơn vị:** Đại học CMC (CMC University)")
st.sidebar.info("Hệ thống mô phỏng và tính toán thông số quy trình chế tạo IC.")
st.sidebar.markdown("---")

# Menu điều hướng
menu_options = [
    "Giới thiệu chung", 
    "1. Oxy hóa (Oxidation)", 
    "2. Quang khắc (Lithography)", 
    "3. Ăn mòn (Etching)", 
    "4. Cấy Ion (Implantation)", 
    "5. Mô phỏng Fab (Simulation)"
]
page = st.sidebar.radio("Chọn quy trình:", menu_options)

# --- Hàm vẽ Wafer (Visualization) ---
def draw_wafer(step, params=None):
    """Vẽ mặt cắt ngang của Wafer tại các bước khác nhau"""
    fig = go.Figure()
    
    # Cấu hình trục ẩn
    fig.update_xaxes(range=[0, 10], showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(range=[0, 8], showgrid=False, zeroline=False, visible=False)
    
    # 1. Silicon Substrate (Nền tảng)
    fig.add_shape(type="rect", x0=1, y0=0, x1=9, y1=2, 
                  fillcolor="lightgray", line=dict(color="gray"), name="Silicon Substrate")
    fig.add_annotation(x=5, y=1, text="Si Substrate (P-type)", showarrow=False)

    # Xử lý hình ảnh theo từng bước
    if step >= 1: # Oxidation
        oxide_h = params.get('oxide_h', 0.5) if params else 1.0
        fig.add_shape(type="rect", x0=1, y0=2, x1=9, y1=2+oxide_h, 
                      fillcolor="#a8dbf0", line=dict(color="blue"), name="SiO2")
        if step == 1:
            fig.add_annotation(x=5, y=2+oxide_h/2, text="SiO2 Layer", showarrow=False)

    if step >= 2: # Spin Coat Photoresist (PR)
        pr_h = 1.0
        base_y = 2 + (params.get('oxide_h', 0.5) if params else 1.0)
        fig.add_shape(type="rect", x0=1, y0=base_y, x1=9, y1=base_y+pr_h, 
                      fillcolor="#ffcccb", line=dict(color="red"), name="Photoresist")
        if step == 2:
            fig.add_annotation(x=5, y=base_y+pr_h/2, text="Photoresist (PR)", showarrow=False)

    if step == 3: # Exposure (UV)
        base_y = 2 + (params.get('oxide_h', 0.5) if params else 1.0) + 1.0
        # Mask (Mặt nạ)
        fig.add_shape(type="rect", x0=1, y0=base_y+1, x1=3, y1=base_y+1.2, fillcolor="black")
        fig.add_shape(type="rect", x0=7, y0=base_y+1, x1=9, y1=base_y+1.2, fillcolor="black")
        fig.add_annotation(x=2, y=base_y+1.5, text="Mask", showarrow=False)
        
        # Tia UV
        for x in [4, 5, 6]:
            fig.add_annotation(
                x=x, y=base_y+0.2, ax=x, ay=base_y+2,
                arrowhead=2, arrowcolor="purple", arrowsize=1.5,
                text="UV Light" if x==5 else ""
            )

    if step >= 4: # Development (Rửa PR)
        base_y = 2 + (params.get('oxide_h', 0.5) if params else 1.0)
        # Vẽ lại PR nhưng bị mất phần giữa
        fig.add_shape(type="rect", x0=1, y0=base_y, x1=3, y1=base_y+1, fillcolor="#ffcccb", line=dict(color="red"))
        fig.add_shape(type="rect", x0=7, y0=base_y, x1=9, y1=base_y+1, fillcolor="#ffcccb", line=dict(color="red"))

    if step >= 5: # Etching (Ăn mòn Oxide)
        ox_h = params.get('oxide_h', 0.5) if params else 1.0
        # Xóa lớp oxide cũ đi để vẽ lớp bị cắt
        fig.layout.shapes = [s for s in fig.layout.shapes if s['fillcolor'] != "#a8dbf0"]
        
        # Vẽ oxide bị cắt
        fig.add_shape(type="rect", x0=1, y0=2, x1=3, y1=2+ox_h, fillcolor="#a8dbf0", line=dict(color="blue"))
        fig.add_shape(type="rect", x0=7, y0=2, x1=9, y1=2+ox_h, fillcolor="#a8dbf0", line=dict(color="blue"))
        
        if step == 5: # Đang ăn mòn (vẫn còn PR)
            # Mũi tên Plasma
            for x in [4, 5, 6]:
                 fig.add_annotation(x=x, y=2.5, ax=x, ay=5, arrowhead=2, arrowcolor="green", text="Plasma Etch" if x==5 else "")

    if step >= 6: # Stripping (Bỏ PR)
        # Chỉ còn Si và Oxide đã định hình. PR (màu đỏ) không được vẽ lại.
        pass

    if step == 7: # Doping (Cấy Ion)
        # Vẽ các ion bay vào vùng hở
        for x in [4, 4.5, 5, 5.5, 6]:
            fig.add_annotation(x=x, y=1.8, ax=x, ay=4, arrowhead=2, arrowcolor="orange", arrowwidth=1)
        # Vùng N-well được tạo ra trong Si
        fig.add_shape(type="path", path="M 3.5 2 Q 5 0.5 6.5 2 Z", fillcolor="#ffff99", line_width=0, opacity=0.6)
        fig.add_annotation(x=5, y=1.5, text="N-type Well", showarrow=False)

    fig.update_layout(
        title=f"Mô hình mặt cắt Wafer - {params.get('title', '') if params else ''}",
        plot_bgcolor="white",
        height=350,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

# --- NỘI DUNG CHÍNH ---

st.markdown('<div class="main-header">PHÒNG THÍ NGHIỆM CÔNG NGHỆ BÁN DẪN</div>', unsafe_allow_html=True)

if page == "Giới thiệu chung":
    st.markdown("""
    <div class="info-box">
    Chào mừng đến với hệ thống mô phỏng <b>Fab Lab</b>. Tại đây, chúng ta sẽ tìm hiểu quy trình biến một phiến Silicon (Sand) thành các con chip vi xử lý (Silicon Chips).
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### Tổng quan quy trình")
        st.write("Quy trình Planar (Planar Process) bao gồm 4 bước lặp đi lặp lại:")
        st.markdown("""
        1.  **Oxy hóa (Oxidation):** Tạo lớp bảo vệ.
        2.  **Quang khắc (Lithography):** Tạo mẫu in.
        3.  **Ăn mòn (Etching):** Khắc mẫu vào vật liệu.
        4.  **Cấy Ion (Doping):** Tạo tính chất điện (p-type/n-type).
        """)
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Wafer_2_inches_to_8_inches.jpg/640px-Wafer_2_inches_to_8_inches.jpg", caption="Silicon Wafer các kích thước")

elif page == "1. Oxy hóa (Oxidation)":
    st.markdown('<div class="sub-header">1. Oxy hóa Nhiệt (Thermal Oxidation)</div>', unsafe_allow_html=True)
    
    st.write("Quá trình tạo lớp SiO2 chất lượng cao trên bề mặt wafer ở nhiệt độ cao.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Mô hình Deal-Grove")
        st.latex(r"x_0^2 + A x_0 = B(t + \tau)")
        st.markdown("""
        - **Oxy hóa khô:** Chậm, lớp oxit đặc, dùng cho cổng transistor (Gate Oxide).
        - **Oxy hóa ướt:** Nhanh, lớp oxit xốp, dùng làm lớp cách điện trường (Field Oxide).
        """)
    
    with col2:
        st.markdown('<div class="calc-box">', unsafe_allow_html=True)
        st.write("**Công cụ tính độ dày Oxide**")
        method = st.radio("Phương pháp:", ["Khô (Dry O2)", "Ướt (Wet H2O)"], horizontal=True)
        temp = st.slider("Nhiệt độ (°C):", 800, 1200, 1000)
        time_min = st.number_input("Thời gian (phút):", value=60, min_value=1)
        
        # Giả lập tính toán đơn giản hóa
        rate = 0.05 if method == "Khô (Dry O2)" else 0.5 # Tốc độ giả định nm/phút tại chuẩn
        temp_factor = (temp - 800) / 400 + 0.5 # Hệ số nhiệt độ
        thickness = rate * time_min * temp_factor * 10 # ra nm
        
        st.metric("Độ dày SiO2 dự kiến:", f"{thickness:.2f} nm")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "2. Quang khắc (Lithography)":
    st.markdown('<div class="sub-header">2. Quang khắc (Photolithography)</div>', unsafe_allow_html=True)
    
    st.info("Bước quan trọng nhất để định hình kích thước linh kiện (Critical Dimension - CD).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Tiêu chuẩn Rayleigh về độ phân giải")
        st.latex(r"CD = k_1 \frac{\lambda}{NA}")
        st.write("""
        - **$\lambda$:** Bước sóng ánh sáng (càng nhỏ càng tốt).
        - **NA:** Khẩu độ số của thấu kính (càng to càng tốt).
        - **$k_1$:** Hệ số quy trình (phụ thuộc vào chất lượng phòng Lab).
        """)
        
    with col2:
        st.markdown('<div class="calc-box">', unsafe_allow_html=True)
        st.write("**Tính độ phân giải (CD)**")
        wl = st.selectbox("Nguồn sáng:", [365, 248, 193, 13.5], format_func=lambda x: f"{x} nm ({'EUV' if x==13.5 else 'DUV' if x<250 else 'UV'})")
        na = st.slider("Khẩu độ số (NA):", 0.5, 1.35, 0.85)
        k1 = 0.4 # Giả định
        
        res = k1 * wl / na
        st.metric("Kích thước nhỏ nhất (Feature Size):", f"{res:.1f} nm")
        if res < 20:
            st.success("Công nghệ: High-end (EUV)")
        else:
            st.warning("Công nghệ: Tiêu chuẩn (DUV/UV)")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "3. Ăn mòn (Etching)":
    st.markdown('<div class="sub-header">3. Ăn mòn (Etching)</div>', unsafe_allow_html=True)
    st.write("Loại bỏ vật liệu tại các vùng không được che chắn bởi Photoresist.")
    
    tab1, tab2 = st.tabs(["Wet Etching", "Dry Etching (Plasma)"])
    with tab1:
        st.write("**Ăn mòn ướt:** Dùng hóa chất lỏng. Ăn mòn theo mọi hướng (Isotropic).")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Isotropic_etching.svg/400px-Isotropic_etching.svg.png", width=300)
    with tab2:
        st.write("**Ăn mòn khô:** Dùng Plasma. Ăn mòn thẳng đứng (Anisotropic). Quan trọng cho chip hiện đại.")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Anisotropic_etching.svg/400px-Anisotropic_etching.svg.png", width=300)

elif page == "4. Cấy Ion (Implantation)":
    st.markdown('<div class="sub-header">4. Cấy Ion (Ion Implantation)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    Quá trình bắn các ion năng lượng cao (Dopants: Boron, Phosphorus, Arsenic) vào phiến Silicon để thay đổi tính dẫn điện, tạo ra các vùng bán dẫn loại P hoặc loại N.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("#### Nguyên lý")
        st.write("Liều lượng (Dosage) quyết định nồng độ tạp chất. Năng lượng bắn quyết định độ sâu ($R_p$).")
        st.latex(r"D = \frac{I \times t}{q \times A}")
        st.write("""
        Trong đó:
        - **D:** Liều lượng ($ions/cm^2$)
        - **I:** Dòng điện chùm ion (Amps)
        - **t:** Thời gian bắn (s)
        - **q:** Điện tích ($1.6 \times 10^{-19} C$)
        - **A:** Diện tích wafer ($cm^2$)
        """)
        
    with col2:
        st.markdown('<div class="calc-box">', unsafe_allow_html=True)
        st.write("**Tính toán Liều lượng (Dosage)**")
        
        current_ua = st.number_input("Dòng điện (µA):", value=100.0)
        time_sec = st.number_input("Thời gian bắn (giây):", value=60)
        wafer_diam = st.selectbox("Đường kính Wafer (inch):", [6, 8, 12])
        
        # Tính toán
        current = current_ua * 1e-6 # Convert to Amps
        radius_cm = (wafer_diam * 2.54) / 2
        area = np.pi * (radius_cm ** 2)
        q = 1.6e-19
        
        dosage = (current * time_sec) / (q * area)
        
        st.write(f"Diện tích Wafer: **{area:.1f} cm²**")
        st.metric("Liều lượng (Dosage):", f"{dosage:.2e} ions/cm²")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "5. Mô phỏng Fab (Simulation)":
    st.markdown('<div class="sub-header">Mô phỏng Toàn trình (Full Flow)</div>', unsafe_allow_html=True)
    
    # Timeline slider
    steps = {
        0: "1. Silicon Wafer (Start)",
        1: "2. Thermal Oxidation",
        2: "3. Spin Coating (PR)",
        3: "4. Exposure (UV Mask)",
        4: "5. Development",
        5: "6. Etching (SiO2 Removal)",
        6: "7. PR Stripping",
        7: "8. Ion Implantation (Doping)"
    }
    
    step_val = st.select_slider("Kéo thanh trượt để xem quy trình:", options=list(steps.keys()), format_func=lambda x: steps[x])
    
    # Vẽ
    st.plotly_chart(draw_wafer(step_val, params={'title': steps[step_val]}), use_container_width=True)
    
    # Giải thích
    explanations = {
        0: "Chuẩn bị phiến Silicon loại P (P-type Substrate).",
        1: "Tạo lớp SiO2 cách điện trên bề mặt.",
        2: "Phủ lớp cảm quang (Photoresist) màu đỏ.",
        3: "Chiếu tia UV qua mặt nạ. Phần hở sáng sẽ thay đổi tính chất.",
        4: "Rửa sạch phần PR bị chiếu sáng (Positive PR).",
        5: "Ăn mòn lớp SiO2 tại vị trí không có PR che chắn.",
        6: "Loại bỏ lớp PR còn lại. Ta có lớp SiO2 đã được định hình.",
        7: "Bắn các ion (màu cam) vào vùng Silicon hở để tạo vùng N-well (màu vàng)."
    }
    st.info(f"👉 **Bước hiện tại:** {explanations[step_val]}")

# Footer
st.markdown("---")
st.markdown("<center>© 2025 Đại học CMC - Khoa Vi mạch Bán dẫn</center>", unsafe_allow_html=True)



