import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy.constants import k, e  # Boltzmann constant, elementary charge

# ==========================================
# CẤU HÌNH TRANG & CSS
# ==========================================
st.set_page_config(
    page_title="BK Semiconductor Lab",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện đẹp hơn
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem; 
        color: #0066cc; 
        font-weight: 800; 
        text-align: center;
        padding-bottom: 20px;
        border-bottom: 2px solid #eee;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 1.5rem; 
        color: #333; 
        border-left: 5px solid #0066cc; 
        padding-left: 10px;
        margin-top: 20px;
    }
    .info-box {
        background-color: #f0f8ff; 
        padding: 15px; 
        border-radius: 8px; 
        border: 1px solid #cce5ff;
        margin-bottom: 15px;
    }
    .formula-box {
        background-color: #fff;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR: THÔNG TIN SINH VIÊN
# ==========================================
with st.sidebar:
    st.markdown("## 👨‍🎓 Hồ sơ sinh viên")
    st.info("""
    **Họ tên:** Bảo Khang  
    **MSV:** BEC250028  
    **Ngành:** Công nghệ Bán dẫn  
    **Trường:** Đại học Bách Khoa (Ví dụ)
    """)
    
    st.markdown("---")
    st.markdown("### 🧭 Điều hướng")
    page = st.radio("Chọn Module học tập:", 
        ["Trang chủ", 
         "1. Cấu trúc Tinh thể (3D)", 
         "2. Vật lý Bán dẫn (Fermi)", 
         "3. Phân tích Mạch Diode (Q-point)", 
         "4. Quy trình Fab (Chi tiết)"])

# ==========================================
# HELPER FUNCTIONS (HÀM HỖ TRỢ VẼ 3D)
# ==========================================
def plot_crystal_structure(structure_type):
    """Hàm vẽ cấu trúc tinh thể 3D sử dụng Plotly"""
    
    # Định nghĩa toạ độ nguyên tử cho các cấu trúc cơ bản
    atoms_x, atoms_y, atoms_z = [], [], []
    
    if structure_type == "Simple Cubic (SC)":
        # 8 đỉnh của hình lập phương
        points = [[0,0,0], [1,0,0], [0,1,0], [0,0,1], 
                  [1,1,0], [1,0,1], [0,1,1], [1,1,1]]
        
    elif structure_type == "Body-Centered Cubic (BCC)":
        # SC + 1 điểm ở tâm
        points = [[0,0,0], [1,0,0], [0,1,0], [0,0,1], 
                  [1,1,0], [1,0,1], [0,1,1], [1,1,1], [0.5, 0.5, 0.5]]
                  
    elif structure_type == "Face-Centered Cubic (FCC)":
        # SC + 6 tâm các mặt
        points = [[0,0,0], [1,0,0], [0,1,0], [0,0,1], 
                  [1,1,0], [1,0,1], [0,1,1], [1,1,1],
                  [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
                  [0.5, 0.5, 1], [0.5, 1, 0.5], [1, 0.5, 0.5]]
    
    # Silicon structure (Diamond) is complex, representing via text explanation in V1, 
    # but here let's stick to basics for clarity.
    
    for p in points:
        atoms_x.append(p[0])
        atoms_y.append(p[1])
        atoms_z.append(p[2])

    fig = go.Figure(data=[go.Scatter3d(
        x=atoms_x, y=atoms_y, z=atoms_z,
        mode='markers',
        marker=dict(
            size=12,
            color=atoms_z,                # Set color to z axis
            colorscale='Viridis',   # Choose a colorscale
            opacity=0.9
        )
    )])

    # Vẽ khung hình lập phương
    lines = [
        [[0,0,0], [1,0,0]], [[0,0,0], [0,1,0]], [[0,0,0], [0,0,1]],
        [[1,0,0], [1,1,0]], [[1,0,0], [1,0,1]],
        [[0,1,0], [1,1,0]], [[0,1,0], [0,1,1]],
        [[0,0,1], [1,0,1]], [[0,0,1], [0,1,1]],
        [[1,1,0], [1,1,1]], [[1,0,1], [1,1,1]], [[0,1,1], [1,1,1]]
    ]
    
    for line in lines:
        fig.add_trace(go.Scatter3d(
            x=[line[0][0], line[1][0]],
            y=[line[0][1], line[1][1]],
            z=[line[0][2], line[1][2]],
            mode='lines',
            line=dict(color='black', width=2),
            showlegend=False
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X', showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(title='Y', showgrid=False, zeroline=False, showticklabels=False),
            zaxis=dict(title='Z', showgrid=False, zeroline=False, showticklabels=False),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=500
    )
    return fig

# ==========================================
# MODULE 1: CẤU TRÚC TINH THỂ 3D
# ==========================================
def page_crystal():
    st.markdown('<div class="main-header">Mô Phỏng Mạng Tinh Thể 3D</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="sub-header">Lý thuyết</div>', unsafe_allow_html=True)
        st.write("""
        Vật liệu bán dẫn (như Silicon) có cấu trúc tinh thể sắp xếp có trật tự. Hiểu về mạng tinh thể giúp giải thích tính chất điện của vật liệu.
        """)
        
        type_struct = st.selectbox(
            "Chọn kiểu mạng tinh thể:", 
            ["Simple Cubic (SC)", "Body-Centered Cubic (BCC)", "Face-Centered Cubic (FCC)"]
        )
        
        st.info(f"""
        **Đang hiển thị: {type_struct}**
        
        * **SC:** Đơn giản nhất, nguyên tử chỉ ở góc. (Hiếm gặp).
        * **BCC:** Có thêm 1 nguyên tử ở tâm khối. (Ví dụ: Na, K).
        * **FCC:** Có thêm nguyên tử ở tâm các mặt. (Ví dụ: Al, Cu, Au).
        * **Lưu ý:** Silicon có cấu trúc **Kim cương (Diamond Cubic)**, là biến thể của 2 mạng FCC lồng vào nhau.
        """)
        
    with col2:
        st.markdown("**Tương tác: Dùng chuột để xoay, lăn chuột để phóng to/thu nhỏ**")
        fig = plot_crystal_structure(type_struct)
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MODULE 2: VẬT LÝ BÁN DẪN (FERMI)
# ==========================================
def page_physics():
    st.markdown('<div class="main-header">Phân bố Fermi-Dirac & Nồng độ Hạt tải</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Trong vật lý bán dẫn, xác suất tìm thấy một electron ở mức năng lượng $E$ được xác định bởi hàm phân bố Fermi-Dirac $f(E)$.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="formula-box">$$ f(E) = \\frac{1}{1 + e^{\\frac{E - E_F}{k_B T}}} $$</div>', unsafe_allow_html=True)
        
        st.write("**Điều chỉnh tham số:**")
        temp_k = st.slider("Nhiệt độ T (Kelvin)", 0, 1000, 300, step=50)
        ef_pos = st.slider("Mức Fermi ($E_F$) so với $E_i$ (eV)", -0.5, 0.5, 0.0, step=0.01)
        
        st.markdown("""
        * **T = 0K:** Xác suất là hàm bậc thang (Step function).
        * **T tăng:** Electron có xác suất cao hơn nhảy lên mức năng lượng cao.
        * **Ef:** Mức năng lượng mà tại đó xác suất tìm thấy electron là 50%.
        """)

    with col2:
        # Tính toán
        E = np.linspace(-1, 1, 500) # Energy range from -1eV to 1eV
        kb_eV = 8.617e-5 # Boltzmann constant in eV/K
        
        if temp_k == 0:
            f_E = np.where(E < ef_pos, 1, 0)
        else:
            f_E = 1 / (1 + np.exp((E - ef_pos) / (kb_eV * temp_k)))
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=f_E, y=E, mode='lines', name='f(E)', line=dict(color='firebrick', width=3)))
        
        # Thêm đường tham chiếu
        fig.add_hline(y=ef_pos, line_dash="dash", line_color="green", annotation_text="Fermi Level (Ef)")
        fig.add_hline(y=0.55, line_dash="dot", line_color="blue", annotation_text="Conduction Band (Ec)")
        fig.add_hline(y=-0.55, line_dash="dot", line_color="blue", annotation_text="Valence Band (Ev)")
        
        fig.update_layout(
            title=f"Hàm phân bố Fermi-Dirac tại T={temp_k}K",
            xaxis_title="Xác suất f(E)",
            yaxis_title="Năng lượng E (eV)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# MODULE 3: PHÂN TÍCH MẠCH (LOAD LINE)
# ==========================================
def page_circuit():
    st.markdown('<div class="main-header">Phân tích Điểm làm việc (Q-Point)</div>', unsafe_allow_html=True)
    
    st.write("""
    Kỹ sư bán dẫn không chỉ cần hiểu linh kiện mà còn phải hiểu cách nó hoạt động trong mạch. 
    Phương pháp **Đường tải (Load Line)** giúp tìm điểm làm việc tĩnh (Q-point) của Diode.
    """)
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Diode_load_line_circuit.svg/320px-Diode_load_line_circuit.svg.png", caption="Mạch Diode nối tiếp điện trở tải")
        st.markdown("### Thông số mạch:")
        v_source = st.number_input("Nguồn DC ($V_{DD}$)", value=5.0, min_value=1.0)
        r_load = st.number_input("Điện trở tải $R$ ($\Omega$)", value=220.0, min_value=10.0)
        
    with c2:
        # 1. Vẽ đặc tuyến Diode (Shockley equation)
        vt = 0.026 # Thermal voltage at 300K ~ 26mV
        Is = 1e-12 # Saturation current
        n = 1.5    # Ideality factor
        
        v_diode = np.linspace(0, 1.5, 200)
        i_diode = Is * (np.exp(v_diode / (n * vt)) - 1) * 1000 # convert to mA
        
        # 2. Vẽ đường tải (Load Line): V_DD = I*R + V_D => I = (V_DD - V_D)/R
        i_loadline = (v_source - v_diode) / r_load * 1000 # convert to mA
        
        # 3. Tìm giao điểm (Q-point) - Giải gần đúng
        idx = np.argwhere(np.diff(np.sign(i_diode - i_loadline))).flatten()
        if len(idx) > 0:
            q_v = v_diode[idx[0]]
            q_i = i_diode[idx[0]]
        else:
            q_v, q_i = 0, 0

        fig = go.Figure()
        
        # Plot Diode Curve
        fig.add_trace(go.Scatter(x=v_diode, y=i_diode, name='Đặc tuyến Diode', line=dict(color='blue')))
        
        # Plot Load Line
        fig.add_trace(go.Scatter(x=v_diode, y=i_loadline, name='Đường tải (Load Line)', line=dict(color='red', dash='dash')))
        
        # Plot Q-point
        fig.add_trace(go.Scatter(x=[q_v], y=[q_i], mode='markers+text', 
                                 text=[f'Q-point ({q_v:.2f}V, {q_i:.2f}mA)'], 
                                 textposition="top left",
                                 marker=dict(size=12, color='green', symbol='x'),
                                 name='Điểm làm việc Q'))

        fig.update_layout(
            title="Biểu đồ xác định điểm làm việc Q",
            xaxis_title="Điện áp Diode $V_D$ (V)",
            yaxis_title="Dòng điện $I_D$ (mA)",
            yaxis_range=[0, v_source/r_load*1000*1.2],
            xaxis_range=[0, 1.5]
        )
        st.plotly_chart(fig, use_container_width=True)
        
        if len(idx) > 0:
            st.success(f"📌 **Kết luận:** Tại mạch này, Diode sẽ ghim áp ở **{q_v:.2f} V** và dòng điện chạy qua là **{q_i:.2f} mA**.")

# ==========================================
# MODULE 4: QUY TRÌNH FAB (VISUAL TIMELINE)
# ==========================================
def page_fab():
    st.markdown('<div class="main-header">Quy trình Sản xuất Chip (Photolithography)</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["1. Oxidation", "2. Photoresist", "3. Exposure", "4. Etching", "5. Stripping"])
    
    # Hàm vẽ mô phỏng mặt cắt ngang wafer đơn giản bằng Plotly Shapes
    def draw_wafer(step):
        fig = go.Figure()
        
        # Silicon Substrate (Base)
        fig.add_shape(type="rect", x0=0, y0=0, x1=10, y1=2, 
                      fillcolor="gray", line=dict(color="black"), name="Silicon")
        fig.add_annotation(x=5, y=1, text="Silicon Substrate", showarrow=False, font=dict(color="white"))
        
        # Oxide Layer
        if step >= 1:
            fig.add_shape(type="rect", x0=0, y0=2, x1=10, y1=2.5, 
                          fillcolor="blue", line=dict(color="black"), opacity=0.5)
            fig.add_annotation(x=1, y=2.25, text="SiO2", showarrow=False, font=dict(color="white"))
            
        # Photoresist
        if step == 2 or step == 3:
            fig.add_shape(type="rect", x0=0, y0=2.5, x1=10, y1=3.0, 
                          fillcolor="red", line=dict(color="black"), opacity=0.6)
            fig.add_annotation(x=5, y=2.75, text="Photoresist (PR)", showarrow=False)
            
        # Exposure Mask
        if step == 3:
            # Mask blocking light
            fig.add_shape(type="rect", x0=3, y0=3.5, x1=7, y1=3.6, fillcolor="black") 
            fig.add_annotation(x=5, y=3.8, text="Mask", showarrow=False)
            # UV Light arrows
            for x in [1, 2, 8, 9]:
                fig.add_annotation(x=x, y=3.5, ax=x, ay=4.5, arrowheader=2, arrowcolor="purple", text="UV")
            # Exposed PR changes color
            fig.add_shape(type="rect", x0=0, y0=2.5, x1=3, y1=3.0, fillcolor="pink", line_width=0)
            fig.add_shape(type="rect", x0=7, y0=2.5, x1=10, y1=3.0, fillcolor="pink", line_width=0)

        # Etching (After developing PR and etching Oxide)
        if step == 4:
            # Remaining PR in center (Positive PR assumption)
            fig.add_shape(type="rect", x0=3, y0=2.5, x1=7, y1=3.0, fillcolor="red", line=dict(color="black"))
            # Oxide etched away on sides
            fig.add_shape(type="rect", x0=3, y0=2, x1=7, y1=2.5, fillcolor="blue", opacity=0.5)
        
        # Stripping
        if step == 5:
            # Only Oxide pattern remains
            fig.add_shape(type="rect", x0=3, y0=2, x1=7, y1=2.5, fillcolor="blue", opacity=0.5)

        fig.update_xaxes(visible=False, range=[-1, 11])
        fig.update_yaxes(visible=False, range=[0, 5])
        fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor="rgba(0,0,0,0)")
        return fig

    with tabs[0]:
        st.markdown("### 1. Oxi hóa nhiệt (Thermal Oxidation)")
        st.write("Tạo lớp $SiO_2$ cách điện trên bề mặt Si.")
        st.latex(r"Si (rắn) + O_2 (khí) \xrightarrow{900-1200^\circ C} SiO_2 (rắn)")
        st.plotly_chart(draw_wafer(1), use_container_width=True)
        
    with tabs[1]:
        st.markdown("### 2. Phủ quang trở (Spin Coating)")
        st.write("Phủ một lớp chất nhạy sáng (Photoresist - PR) lên bề mặt.")
        st.plotly_chart(draw_wafer(2), use_container_width=True)

    with tabs[2]:
        st.markdown("### 3. Chiếu sáng (Exposure)")
        st.write("Chiếu tia UV qua mặt nạ (Mask). Phần PR tiếp xúc UV sẽ bị biến đổi hóa học (trở nên dễ tan hoặc khó tan tùy loại PR).")
        st.plotly_chart(draw_wafer(3), use_container_width=True)
        
    with tabs[3]:
        st.markdown("### 4. Ăn mòn (Etching)")
        st.write("Dùng axit (Wet etching) hoặc Plasma (Dry etching) để ăn mòn lớp $SiO_2$ tại những vị trí không được PR bảo vệ.")
        st.plotly_chart(draw_wafer(4), use_container_width=True)

    with tabs[4]:
        st.markdown("### 5. Loại bỏ PR (Stripping)")
        st.write("Loại bỏ lớp PR còn sót lại, để lại mẫu $SiO_2$ mong muốn trên đế Si.")
        st.plotly_chart(draw_wafer(5), use_container_width=True)

# ==========================================
# MAIN ROUTER
# ==========================================
if page == "Trang chủ":
    st.markdown('<div class="main-header">SEMICONDUCTOR ENGINEERING PORTFOLIO</div>', unsafe_allow_html=True)
    
    col_intro, col_img = st.columns([1.5, 1])
    
    with col_intro:
        st.markdown(f"""
        ### Xin chào, tôi là Bảo Khang 👋
        **Mã sinh viên:** BEC250028
        
        Chào mừng đến với "Phòng thí nghiệm ảo" của tôi. Đây là nơi tôi tổng hợp, trực quan hóa và mô phỏng các kiến thức chuyên ngành **Công nghệ Bán dẫn**.
        
        #### Mục tiêu dự án:
        1.  **Trực quan hóa:** Biến các công thức vật lý khô khan thành mô hình 3D.
        2.  **Tính toán:** Hỗ trợ giải bài tập chuyên ngành nhanh chóng.
        3.  **Lưu trữ:** Xây dựng kho tri thức cá nhân (Second Brain).
        """)
        
        st.info("💡 **Mẹo:** Truy cập menu bên trái để trải nghiệm các mô phỏng 3D!")

    with col_img:
        # Placeholder image for a futuristic chip
        st.image("https://images.unsplash.com/photo-1555664424-778a1e5e1b48?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80", 
                 caption="Chip Design Visualization", use_column_width=True)

elif page == "1. Cấu trúc Tinh thể (3D)":
    page_crystal()
elif page == "2. Vật lý Bán dẫn (Fermi)":
    page_physics()
elif page == "3. Phân tích Mạch Diode (Q-point)":
    page_circuit()
elif page == "4. Quy trình Fab (Chi tiết)":
    page_fab()

