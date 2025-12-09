import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import math

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="CMC Semiconductor Portfolio - Đỗ Bảo Khang",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS TÙY CHỈNH CHO GIAO DIỆN ĐẸP ---
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #B22222; /* CMC Red color approximation */
        text-align: center;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .student-info {
        text-align: center;
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 30px;
        font-style: italic;
    }
    .module-header {
        background: linear-gradient(to right, #0056b3, #00c6ff);
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .concept-box {
        background-color: #f0f2f6;
        border-left: 5px solid #0056b3;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .resistor-band {
        height: 100px;
        width: 20px;
        display: inline-block;
        margin: 0 5px;
    }
    .logic-on {
        color: #28a745;
        font-weight: bold;
    }
    .logic-off {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: THÔNG TIN SINH VIÊN ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/chip.png", width=150)
    st.markdown("## Đỗ Bảo Khang")
    st.markdown("**MSSV:** BEC250028")
    st.markdown("**Khoa:** Vi điện tử - Viễn thông")
    st.markdown("**Trường:** Đại học CMC (CMC University)")
    st.markdown("---")
    
    st.markdown("### 📚 Danh mục Modules")
    selected_module = st.radio("Chọn chức năng:", [
        "1. Tra cứu & Tính toán (Basic Calc)",
        "2. Cổng Logic (Logic Gates)",
        "3. Đặc tuyến V-A (I-V Plotter)",
        "4. Wiki Bán dẫn (Semiconductor Wiki)",
        "5. Quy trình Fab (Fabrication)"
    ])
    
    st.markdown("---")
    st.info("Ứng dụng được thiết kế để hỗ trợ học tập và mô phỏng các nguyên lý cơ bản của ngành công nghiệp bán dẫn.")

# --- HEADER CHUNG ---
st.markdown('<div class="main-title">HỆ THỐNG MÔ PHỎNG & TÍNH TOÁN VI MẠCH</div>', unsafe_allow_html=True)
st.markdown('<div class="student-info">Portfolio Học tập - Đỗ Bảo Khang (BEC250028)</div>', unsafe_allow_html=True)

# ==============================================================================
# MODULE 1: TRA CỨU & TÍNH TOÁN CƠ BẢN
# ==============================================================================
if selected_module == "1. Tra cứu & Tính toán (Basic Calc)":
    st.markdown('<div class="module-header"><h3>🛠️ Module 1: Tra cứu & Tính toán Linh kiện Cơ bản</h3></div>', unsafe_allow_html=True)
    
    st.markdown("""
    Trong ngành điện tử, kỹ năng cơ bản nhất là đọc giá trị linh kiện và hiểu các định luật vật lý nền tảng.
    Module này giúp bạn thực hành những kỹ năng "nhập môn" đó.
    """)
    
    tab1, tab2, tab3 = st.tabs(["📟 Đọc Điện Trở (Color Code)", "⚡ Định luật Ohm", "🔄 Chuyển đổi Đơn vị"])
    
    # --- TAB 1: ĐIỆN TRỞ ---
    with tab1:
        st.subheader("Máy tính Vạch màu Điện trở (4 vạch)")
        
        colors = {
            "Đen (0)": (0, "#000000", "white"), "Nâu (1)": (1, "#8B4513", "white"), "Đỏ (2)": (2, "#FF0000", "white"),
            "Cam (3)": (3, "#FFA500", "black"), "Vàng (4)": (4, "#FFFF00", "black"), "Lục (5)": (5, "#008000", "white"),
            "Lam (6)": (6, "#0000FF", "white"), "Tím (7)": (7, "#800080", "white"), "Xám (8)": (8, "#808080", "black"),
            "Trắng (9)": (9, "#FFFFFF", "black")
        }
        multiplier_colors = {
            "Đen (x1)": (1, "#000000"), "Nâu (x10)": (10, "#8B4513"), "Đỏ (x100)": (100, "#FF0000"),
            "Cam (x1k)": (1000, "#FFA500"), "Vàng (x10k)": (10000, "#FFFF00"), "Lục (x100k)": (100000, "#008000"),
            "Lam (x1M)": (1000000, "#0000FF"), "Vàng kim (x0.1)": (0.1, "#FFD700"), "Bạc (x0.01)": (0.01, "#C0C0C0")
        }
        tolerance_colors = {
            "Nâu (±1%)": (1, "#8B4513"), "Đỏ (±2%)": (2, "#FF0000"), "Vàng kim (±5%)": (5, "#FFD700"), 
            "Bạc (±10%)": (10, "#C0C0C0")
        }

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            b1 = st.selectbox("Vạch 1 (Số hàng chục)", list(colors.keys()), index=1)
        with col2:
            b2 = st.selectbox("Vạch 2 (Số hàng đơn vị)", list(colors.keys()), index=0)
        with col3:
            b3 = st.selectbox("Vạch 3 (Hệ số nhân)", list(multiplier_colors.keys()), index=2)
        with col4:
            b4 = st.selectbox("Vạch 4 (Sai số)", list(tolerance_colors.keys()), index=2)

        # Tính toán
        val1 = colors[b1][0]
        val2 = colors[b2][0]
        mul_val = multiplier_colors[b3][0]
        tol_val = tolerance_colors[b4][0]
        
        resistance = (val1 * 10 + val2) * mul_val
        
        # Hiển thị kết quả
        st.markdown("#### Kết quả:")
        
        # Vẽ hình minh họa bằng HTML/CSS
        st.markdown(f"""
        <div style="background: linear-gradient(to bottom, #d2b48c, #f5deb3); padding: 20px; border-radius: 50px; text-align: center; width: 100%; border: 2px solid #8b4513;">
            <span style="display:inline-block; width:30px; height:80px; background-color:{colors[b1][1]}; margin-right:15px;"></span>
            <span style="display:inline-block; width:30px; height:80px; background-color:{colors[b2][1]}; margin-right:15px;"></span>
            <span style="display:inline-block; width:30px; height:80px; background-color:{multiplier_colors[b3][1]}; margin-right:40px;"></span>
            <span style="display:inline-block; width:30px; height:80px; background-color:{tolerance_colors[b4][1]};"></span>
        </div>
        """, unsafe_allow_html=True)
        
        res_formatted = f"{resistance:,.2f}" if resistance < 1000 else f"{resistance/1000:,.2f} k" if resistance < 1000000 else f"{resistance/1000000:,.2f} M"
        st.metric("Giá trị Điện trở:", f"{res_formatted}Ω ±{tol_val}%")

    # --- TAB 2: ĐỊNH LUẬT OHM ---
    with tab2:
        st.subheader("Tính toán Định luật Ohm")
        st.latex(r"V = I \times R")
        st.write("Nhập 2 giá trị bất kỳ để tính giá trị còn lại.")
        
        c1, c2, c3 = st.columns(3)
        v_in = c1.number_input("Điện áp V (Volts)", min_value=0.0, step=0.1, value=0.0)
        i_in = c2.number_input("Dòng điện I (Ampe)", min_value=0.0, step=0.01, value=0.0)
        r_in = c3.number_input("Điện trở R (Ohm)", min_value=0.0, step=1.0, value=0.0)
        
        result_text = ""
        if v_in == 0 and i_in > 0 and r_in > 0:
            result_text = f"Điện áp V = {i_in * r_in:.2f} V"
        elif i_in == 0 and v_in > 0 and r_in > 0:
            result_text = f"Dòng điện I = {v_in / r_in:.4f} A"
        elif r_in == 0 and v_in > 0 and i_in > 0:
            result_text = f"Điện trở R = {v_in / i_in:.2f} Ω"
        elif v_in > 0 and i_in > 0 and r_in > 0:
            result_text = "Bạn đã nhập cả 3 số liệu. Hãy để trống (bằng 0) giá trị cần tìm."
        else:
            result_text = "Vui lòng nhập ít nhất 2 giá trị > 0."
            
        st.info(f"👉 **Kết quả:** {result_text}")

    # --- TAB 3: CHUYỂN ĐỔI ĐƠN VỊ ---
    with tab3:
        st.subheader("Chuyển đổi năng lượng Photon")
        st.markdown("Trong vật lý bán dẫn, chúng ta thường xuyên chuyển đổi giữa bước sóng ánh sáng (nm) và năng lượng dải cấm (eV).")
        st.latex(r"E (eV) = \frac{1240}{\lambda (nm)}")
        
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            nm_val = st.number_input("Nhập bước sóng (nm):", value=550.0)
            ev_result = 1240 / nm_val if nm_val > 0 else 0
            st.write(f"Năng lượng tương ứng: **{ev_result:.2f} eV**")
            
        with col_u2:
            ev_val = st.number_input("Nhập năng lượng (eV):", value=1.12) # Si Gap
            nm_result = 1240 / ev_val if ev_val > 0 else 0
            st.write(f"Bước sóng tương ứng: **{nm_result:.2f} nm**")

# ==============================================================================
# MODULE 2: CỔNG LOGIC
# ==============================================================================
elif selected_module == "2. Cổng Logic (Logic Gates)":
    st.markdown('<div class="module-header"><h3>⚙️ Module 2: Mô phỏng Cổng Logic</h3></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="concept-box">
    <b>Digital Logic</b> là nền tảng của mọi con chip xử lý. Từ hàng tỷ cổng logic nhỏ bé này, chúng ta xây dựng nên CPU, GPU.
    Module này giúp bạn hình dung cách tín hiệu 0 và 1 được xử lý.
    </div>
    """, unsafe_allow_html=True)
    
    col_ctrl, col_viz = st.columns([1, 2])
    
    with col_ctrl:
        gate_type = st.selectbox("Chọn cổng logic:", ["AND", "OR", "NOT", "NAND", "NOR", "XOR"])
        st.write("**Trạng thái đầu vào:**")
        
        # Input A
        input_a = st.toggle("Input A (1=ON, 0=OFF)", value=False)
        val_a = 1 if input_a else 0
        
        # Input B (Ẩn nếu là cổng NOT)
        if gate_type != "NOT":
            input_b = st.toggle("Input B (1=ON, 0=OFF)", value=False)
            val_b = 1 if input_b else 0
        else:
            val_b = None
            st.write("Input B: Không dùng cho cổng NOT")

        # Logic xử lý
        if gate_type == "AND":
            output = val_a & val_b
            formula = "Y = A . B"
        elif gate_type == "OR":
            output = val_a | val_b
            formula = "Y = A + B"
        elif gate_type == "NOT":
            output = 0 if val_a == 1 else 1
            formula = "Y = ~A"
        elif gate_type == "NAND":
            output = 0 if (val_a & val_b) else 1
            formula = "Y = ~(A . B)"
        elif gate_type == "NOR":
            output = 0 if (val_a | val_b) else 1
            formula = "Y = ~(A + B)"
        elif gate_type == "XOR":
            output = val_a ^ val_b
            formula = "Y = A ⊕ B"
            
    with col_viz:
        st.markdown("### Kết quả Mô phỏng")
        
        # Vẽ minh họa đơn giản
        viz_col1, viz_col2, viz_col3 = st.columns([1,1,1])
        
        with viz_col1:
            st.markdown(f"<div style='text-align:center; padding:20px; background-color:{'#28a745' if val_a else '#dc3545'}; color:white; border-radius:10px;'>Input A<br><h1>{val_a}</h1></div>", unsafe_allow_html=True)
            if gate_type != "NOT":
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center; padding:20px; background-color:{'#28a745' if val_b else '#dc3545'}; color:white; border-radius:10px;'>Input B<br><h1>{val_b}</h1></div>", unsafe_allow_html=True)
        
        with viz_col2:
            st.markdown(f"<div style='display:flex; align-items:center; justify-content:center; height:100%; font-size:30px;'>➡ <b>{gate_type}</b> ➡</div>", unsafe_allow_html=True)
            
        with viz_col3:
            st.markdown(f"<div style='text-align:center; padding:40px; background-color:{'#28a745' if output else '#dc3545'}; color:white; border-radius:50%; border: 4px solid #333;'>Output Y<br><h1>{output}</h1></div>", unsafe_allow_html=True)
            
        st.markdown("---")
        st.markdown(f"**Biểu thức Boolean:** :large_blue_circle: **{formula}**")
        
        # Bảng chân trị
        with st.expander(f"Xem Bảng Chân Trị (Truth Table) của {gate_type}"):
            if gate_type == "AND":
                df = pd.DataFrame({'A': [0,0,1,1], 'B': [0,1,0,1], 'Y': [0,0,0,1]})
            elif gate_type == "OR":
                df = pd.DataFrame({'A': [0,0,1,1], 'B': [0,1,0,1], 'Y': [0,1,1,1]})
            elif gate_type == "NOT":
                df = pd.DataFrame({'A': [0,1], 'Y': [1,0]})
            elif gate_type == "NAND":
                df = pd.DataFrame({'A': [0,0,1,1], 'B': [0,1,0,1], 'Y': [1,1,1,0]})
            elif gate_type == "NOR":
                df = pd.DataFrame({'A': [0,0,1,1], 'B': [0,1,0,1], 'Y': [1,0,0,0]})
            elif gate_type == "XOR":
                df = pd.DataFrame({'A': [0,0,1,1], 'B': [0,1,0,1], 'Y': [0,1,1,0]})
            st.table(df)

# ==============================================================================
# MODULE 3: ĐẶC TUYẾN V-A
# ==============================================================================
elif selected_module == "3. Đặc tuyến V-A (I-V Plotter)":
    st.markdown('<div class="module-header"><h3>📈 Module 3: Đặc tuyến V-A (I-V Characteristic)</h3></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="concept-box">
    Để hiểu một linh kiện bán dẫn (Diode, Transistor), ta không nhìn hình dáng, mà nhìn vào <b>Đặc tuyến I-V</b> của nó.
    Biểu đồ này cho biết dòng điện ($I$) chạy qua linh kiện thay đổi thế nào khi điện áp ($V$) thay đổi.
    </div>
    """, unsafe_allow_html=True)
    
    comp_type = st.selectbox("Chọn linh kiện mô phỏng:", ["PN Junction Diode", "MOSFET (Simplified)"])
    
    if comp_type == "PN Junction Diode":
        st.subheader("Mô phỏng Diode (Phương trình Shockley)")
        st.latex(r"I = I_S \left( e^{\frac{V}{n V_T}} - 1 \right)")
        
        col_input, col_plot = st.columns([1, 2])
        with col_input:
            st.write("**Thông số vật lý:**")
            temp_c = st.slider("Nhiệt độ (°C):", -50, 150, 25)
            n_val = st.slider("Hệ số lý tưởng (n):", 1.0, 2.0, 1.0, 0.1)
            material = st.radio("Vật liệu:", ["Silicon (Si)", "Germanium (Ge)"])
            
            # Tính toán tham số
            temp_k = temp_c + 273.15
            k = 1.38e-23 # Boltzmann constant
            q = 1.6e-19  # Electron charge
            Vt = (k * temp_k) / q
            
            # Dòng bão hòa ngược (Is) giả định thay đổi theo vật liệu
            if material == "Silicon (Si)":
                Is = 1e-12 # pA range
                v_threshold_disp = 0.7
            else:
                Is = 1e-6  # uA range (Ge rò nhiều hơn)
                v_threshold_disp = 0.3
                
            st.markdown(f"""
            - **$V_T$ (Thermal Voltage):** {Vt*1000:.2f} mV
            - **$I_S$:** {Is} A
            - **Ngưỡng dẫn dự kiến:** ~{v_threshold_disp} V
            """)

        with col_plot:
            # Tạo dữ liệu
            v = np.linspace(-1.0, 1.0, 500)
            i = Is * (np.exp(v / (n_val * Vt)) - 1)
            
            # Xử lý giới hạn hiển thị để biểu đồ không bị bẹt
            i_display = np.clip(i, -Is*10, 0.1) # Clip dòng để dễ nhìn vùng thuận
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=v, y=i, mode='lines', name=f'Diode {material}'))
            
            fig.update_layout(
                title=f"Đặc tuyến I-V của Diode tại {temp_c}°C",
                xaxis_title="Điện áp V (Volt)",
                yaxis_title="Dòng điện I (Ampe)",
                yaxis_range=[-1e-3, 0.05], # Zoom vào vùng hoạt động
                xaxis_range=[-1, 1],
                template="plotly_white"
            )
            # Thêm đường 0
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            fig.add_vline(x=0, line_dash="dash", line_color="gray")
            
            st.plotly_chart(fig, use_container_width=True)

    elif comp_type == "MOSFET (Simplified)":
        st.subheader("Mô phỏng N-MOSFET (Vùng bão hòa)")
        st.latex(r"I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L} (V_{GS} - V_{th})^2")
        
        col_input, col_plot = st.columns([1, 2])
        with col_input:
            v_th = st.slider("Điện áp ngưỡng Vth (V):", 0.5, 2.0, 0.7)
            k_n = st.slider("Hệ số K (mA/V^2):", 0.1, 5.0, 1.0)
            st.info("Kéo thanh trượt Vgs bên dưới biểu đồ để xem đường cong thay đổi.")

        with col_plot:
            v_gs_list = [1.0, 2.0, 3.0, 4.0] # Vẽ nhiều đường Vgs khác nhau
            v_ds = np.linspace(0, 5, 100)
            
            fig = go.Figure()
            
            for v_gs in v_gs_list:
                # Tính dòng Id đơn giản hóa (Triode -> Saturation transition)
                i_d = []
                for v in v_ds:
                    if v_gs < v_th:
                        val = 0
                    elif v < (v_gs - v_th): # Triode
                        val = k_n * (2*(v_gs - v_th)*v - v**2)
                    else: # Saturation
                        val = k_n * (v_gs - v_th)**2
                    i_d.append(val)
                
                fig.add_trace(go.Scatter(x=v_ds, y=i_d, mode='lines', name=f'Vgs = {v_gs}V'))

            fig.update_layout(
                title="Đặc tuyến đầu ra MOSFET (Id vs Vds)",
                xaxis_title="Vds (Volt)",
                yaxis_title="Id (mA)",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# MODULE 4: WIKI BÁN DẪN
# ==============================================================================
elif selected_module == "4. Wiki Bán dẫn (Semiconductor Wiki)":
    st.markdown('<div class="module-header"><h3>📚 Module 4: Wiki Bán dẫn Cá nhân</h3></div>', unsafe_allow_html=True)
    
    st.write("Tổng hợp các thuật ngữ và kiến thức cốt lõi mà một sinh viên Vi mạch cần nhớ.")
    
    # Tìm kiếm
    search_term = st.text_input("🔍 Tìm kiếm thuật ngữ (ví dụ: Doping, Fermi):")
    
    wiki_data = {
        "Band Gap (Vùng cấm)": {
            "content": """
            Là khoảng năng lượng mà không trạng thái electron nào có thể tồn tại. 
            Nó là sự khác biệt năng lượng giữa đỉnh của dải hóa trị (Valence Band) và đáy của dải dẫn (Conduction Band).
            - **Chất dẫn điện:** Band gap $\\approx 0$ eV.
            - **Chất bán dẫn:** Band gap $0.1 - 3$ eV (Si = 1.12 eV).
            - **Chất cách điện:** Band gap $> 3-4$ eV.
            """,
            "tag": "Vật lý chất rắn"
        },
        "Doping (Pha tạp)": {
            "content": """
            Quá trình thêm các nguyên tử tạp chất vào chất bán dẫn tinh khiết (Intrinsic) để thay đổi độ dẫn điện.
            - **Loại N (Negative):** Pha tạp chất nhóm V (như Phosphor) $\\rightarrow$ dư thừa Electron.
            - **Loại P (Positive):** Pha tạp chất nhóm III (như Boron) $\\rightarrow$ dư thừa Lỗ trống (Holes).
            """,
            "tag": "Quy trình Fab"
        },
        "Fermi Level (Mức Fermi)": {
            "content": """
            Mức năng lượng giả định mà tại đó xác suất tìm thấy electron là 50% ở nhiệt độ tuyệt đối (0K).
            - Trong bán dẫn loại N: Mức Fermi nằm gần dải dẫn.
            - Trong bán dẫn loại P: Mức Fermi nằm gần dải hóa trị.
            """,
            "tag": "Vật lý chất rắn"
        },
        "Wafer (Phiến bán dẫn)": {
            "content": """
            Một lát mỏng vật liệu bán dẫn (thường là Silicon tinh thể) dùng làm nền để chế tạo vi mạch.
            Được cắt ra từ thỏi (Ingot) đơn tinh thể hình trụ.
            Các kích thước phổ biến: 150mm (6 inch), 200mm (8 inch), 300mm (12 inch).
            """,
            "tag": "Sản xuất"
        },
        "Moore's Law (Định luật Moore)": {
            "content": """
            Dự đoán của Gordon Moore (đồng sáng lập Intel) năm 1965:
            "Số lượng bóng bán dẫn trên một vi mạch tích hợp sẽ tăng gấp đôi khoảng hai năm một lần."
            Mặc dù tốc độ đang chậm lại, định luật này vẫn là kim chỉ nam cho ngành công nghiệp.
            """,
            "tag": "Lịch sử"
        }
    }
    
    # Hiển thị wiki
    cols = st.columns(2)
    idx = 0
    for title, info in wiki_data.items():
        if search_term.lower() in title.lower() or search_term.lower() in info["content"].lower():
            with cols[idx % 2]:
                with st.expander(f"📖 {title}", expanded=True):
                    st.badge(info["tag"])
                    st.markdown(info["content"])
            idx += 1

# ==============================================================================
# MODULE 5: QUY TRÌNH FAB
# ==============================================================================
elif selected_module == "5. Quy trình Fab (Fabrication)":
    st.markdown('<div class="module-header"><h3>🏭 Module 5: Mô phỏng Quy trình Sản xuất Chip 3D</h3></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="concept-box">
    Từ hạt cát (Silicon) đến con chip trong máy tính là một hành trình kỳ diệu.
    Tại đây, chúng ta mô phỏng <b>Quy trình Planar</b> - nền tảng của công nghệ chế tạo IC hiện đại dưới góc nhìn 3D.
    </div>
    """, unsafe_allow_html=True)
    
    # Helper tạo hình hộp 3D (Cuboid) cho Plotly Mesh3d
    def make_box(x0, x1, y0, y1, z0, z1, color, opacity=1.0, name=""):
        # 8 đỉnh của hình hộp
        x = [x0, x0, x1, x1, x0, x0, x1, x1]
        y = [y0, y1, y1, y0, y0, y1, y1, y0]
        z = [z0, z0, z0, z0, z1, z1, z1, z1]
        
        # Định nghĩa các mặt tam giác nối các đỉnh (i, j, k)
        return go.Mesh3d(
            x=x, y=y, z=z,
            i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            color=color,
            opacity=opacity,
            name=name,
            showscale=False
        )

    def draw_fab_step_3d(step_index):
        fig = go.Figure()
        
        # Kích thước chung
        W, D = 10, 6 # Width, Depth
        
        # 1. SI SUBSTRATE (Luôn hiện) - Màu xám
        fig.add_trace(make_box(0, W, 0, D, 0, 2, 'lightgray', name="Si Substrate"))
        
        # 2. Xử lý từng bước
        
        # Step 1: Oxidation (Thêm lớp Oxide xanh dương)
        if step_index == 1:
            fig.add_trace(make_box(0, W, 0, D, 2, 3, '#87CEEB', name="SiO2"))
            
        # Step 2: Spin Coat (Thêm lớp PR đỏ hồng)
        elif step_index == 2:
            fig.add_trace(make_box(0, W, 0, D, 2, 3, '#87CEEB', name="SiO2"))
            fig.add_trace(make_box(0, W, 0, D, 3, 4, '#FFB6C1', name="Photoresist"))
            
        # Step 3: Exposure (UV + Mask)
        elif step_index == 3:
            fig.add_trace(make_box(0, W, 0, D, 2, 3, '#87CEEB', name="SiO2"))
            fig.add_trace(make_box(0, W, 0, D, 3, 4, '#FFB6C1', name="Photoresist"))
            # Mask (2 miếng đen lơ lửng)
            fig.add_trace(make_box(0, 3, 0, D, 5, 5.2, 'black', name="Mask Left"))
            fig.add_trace(make_box(7, W, 0, D, 5, 5.2, 'black', name="Mask Right"))
            # Tia UV (Các đường thẳng tím)
            for x_line in np.linspace(3.5, 6.5, 5):
                fig.add_trace(go.Scatter3d(
                    x=[x_line, x_line], y=[D/2, D/2], z=[6, 3],
                    mode='lines', line=dict(color='purple', width=5), name="UV Light"
                ))

        # Step 4: Development (Rửa trôi PR phần giữa)
        elif step_index == 4:
            fig.add_trace(make_box(0, W, 0, D, 2, 3, '#87CEEB', name="SiO2"))
            # PR bị tách đôi (Trái/Phải)
            fig.add_trace(make_box(0, 3, 0, D, 3, 4, '#FFB6C1', name="PR Left"))
            fig.add_trace(make_box(7, W, 0, D, 3, 4, '#FFB6C1', name="PR Right"))
            
        # Step 5: Etching (Ăn mòn Oxide phần giữa)
        elif step_index == 5:
            # PR vẫn còn
            fig.add_trace(make_box(0, 3, 0, D, 3, 4, '#FFB6C1', name="PR Left"))
            fig.add_trace(make_box(7, W, 0, D, 3, 4, '#FFB6C1', name="PR Right"))
            # Oxide bị tách đôi
            fig.add_trace(make_box(0, 3, 0, D, 2, 3, '#87CEEB', name="SiO2 Left"))
            fig.add_trace(make_box(7, W, 0, D, 2, 3, '#87CEEB', name="SiO2 Right"))
            # Plasma (Xanh lá)
            for x_line in np.linspace(3.5, 6.5, 5):
                 fig.add_trace(go.Scatter3d(
                    x=[x_line, x_line], y=[D/2, D/2], z=[5, 2],
                    mode='lines', line=dict(color='green', width=3, dash='dash'), name="Plasma Etch"
                ))

        # Step 6: Stripping (Bỏ PR, chỉ còn Oxide hình cái cốc)
        elif step_index == 6:
            fig.add_trace(make_box(0, 3, 0, D, 2, 3, '#87CEEB', name="SiO2 Left"))
            fig.add_trace(make_box(7, W, 0, D, 2, 3, '#87CEEB', name="SiO2 Right"))
            
        # Step 7: Doping (Bắn Ion vào giữa)
        elif step_index == 7:
            fig.add_trace(make_box(0, 3, 0, D, 2, 3, '#87CEEB', name="SiO2 Left"))
            fig.add_trace(make_box(7, W, 0, D, 2, 3, '#87CEEB', name="SiO2 Right"))
            # Vùng pha tạp N-type (Màu vàng trên bề mặt Si)
            fig.add_trace(make_box(3, 7, 0, D, 1.8, 2, 'yellow', name="N-well"))
            # Tia Ion (Cam)
            for x_line in np.linspace(3.5, 6.5, 5):
                 fig.add_trace(go.Scatter3d(
                    x=[x_line, x_line], y=[D/2, D/2], z=[5, 2],
                    mode='lines', line=dict(color='orange', width=4), name="Ion Beam"
                ))

        # Cấu hình Camera và Khung cảnh
        fig.update_layout(
            title="Mô phỏng 3D Quy trình Fab (Kéo chuột để xoay)",
            scene=dict(
                xaxis=dict(range=[0, 10], showbackground=False, visible=False),
                yaxis=dict(range=[0, 6], showbackground=False, visible=False),
                zaxis=dict(range=[0, 7], showbackground=False, visible=False),
                aspectmode='manual',
                aspectratio=dict(x=1, y=0.5, z=0.5), # Tỉ lệ hình hộp chữ nhật đẹp
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.2) # Góc nhìn Isometric
                )
            ),
            margin=dict(l=0, r=0, t=30, b=0),
            height=500
        )
        return fig

    # Timeline điều khiển
    steps_data = {
        0: {"label": "Silicon Wafer", "desc": "Bắt đầu với phiến Silicon đơn tinh thể sạch."},
        1: {"label": "Oxidation", "desc": "Oxy hóa nhiệt tạo lớp SiO2 (Màu xanh) cách điện."},
        2: {"label": "Spin Coat", "desc": "Phủ lớp chất cảm quang Photoresist (Màu hồng)."},
        3: {"label": "Exposure", "desc": "Chiếu tia UV (Tím) qua mặt nạ để in hình ảnh mạch."},
        4: {"label": "Development", "desc": "Rửa sạch phần PR ở giữa đã bị chiếu sáng."},
        5: {"label": "Etching", "desc": "Ăn mòn lớp Oxide ở giữa bằng Plasma (Xanh lá)."},
        6: {"label": "Stripping", "desc": "Loại bỏ lớp PR, chỉ giữ lại mẫu Oxide đã định hình."},
        7: {"label": "Doping", "desc": "Bắn Ion (Cam) vào vùng hở để tạo vùng bán dẫn N (Vàng)."}
    }
    
    step = st.select_slider("Quy trình dòng chảy (Process Flow):", options=list(steps_data.keys()), format_func=lambda x: steps_data[x]["label"])
    
    st.info(f"👉 **Bước {step}: {steps_data[step]['label']}** - {steps_data[step]['desc']}")
    
    # Hiển thị
    st.plotly_chart(draw_fab_step_3d(step), use_container_width=True)


# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.8rem;">
    © 2025 Đỗ Bảo Khang - BEC250028 | CMC University <br>
    Built with Python & Streamlit for Educational Purpose.
</div>
""", unsafe_allow_html=True)

