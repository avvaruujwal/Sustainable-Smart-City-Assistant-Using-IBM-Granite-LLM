import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from streamlit_option_menu import option_menu
from ui.summary_card import summary_card
from ui.feedback_form import render_feedback_form
from ui.chat_assistant import render_chat_assistant
from ui.eco_tips import render_eco_tips
from ui.policy_summarizer import render_policy_summarizer
from ui.report_generator import render_report_generator
from ui.document_uploader import render_document_uploader
from ui.policy_search import render_policy_search
from ui.kpi_forecasting import render_kpi_forecasting
from ui.anomaly_checker import render_anomaly_checker

# Page configuration
st.set_page_config(
    page_title="Smart City Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        color: #333;
    }
    .metric-card h4 {
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-good { background-color: #28a745; }
    .status-warning { background-color: #ffc107; }
    .status-critical { background-color: #dc3545; }
    .real-time-clock {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        padding: 0.5rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 8px;
        border: 2px solid #667eea;
    }
    /* Make all text darker for better readability */
    .stMarkdown, .stText {
        color: #8afff3 !important;
    }
    /* Dashboard text styling */
    .dashboard-text {
        color: #8afff3;
        font-weight: 500;
    }
</style>

<script>
// JavaScript for real-time clock updates
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour12: false, 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    const dateString = now.toLocaleDateString();
    const dayString = now.toLocaleDateString('en-US', { weekday: 'long' });
    
    const clockElement = document.getElementById('real-time-clock');
    if (clockElement) {
        clockElement.innerHTML = `
            <div style="font-size: 1.5rem; font-weight: bold; color: #8afff3;">🕐 ${timeString}</div>
            <div style="font-size: 1rem; color: #34495e;">${dayString}, ${dateString}</div>
        `;
    }
}

// Update clock every second
setInterval(updateClock, 1000);
updateClock(); // Initial call
</script>
""", unsafe_allow_html=True)

def generate_sample_data():
    """Generate sample data for dynamic charts with realistic dates"""
    # Use recent dates for more realistic data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Last 30 days
    
    # Energy consumption data - daily for last 30 days
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    base_energy = 1200
    energy_data = pd.DataFrame({
        'Date': dates,
        'Energy_Consumption': [
            base_energy + np.random.normal(0, 100) + 
            50 * np.sin(i * 0.2) +  # Weekly pattern
            30 * np.cos(i * 0.1)    # Daily variation
            for i in range(len(dates))
        ],
        'Renewable_Energy': [
            400 + np.random.normal(0, 30) + 
            20 * np.sin(i * 0.15) +  # Weekly pattern
            15 * np.cos(i * 0.08)    # Daily variation
            for i in range(len(dates))
        ],
        'Peak_Demand': [
            1500 + np.random.normal(0, 150) + 
            100 * np.sin(i * 0.25)   # Weekly pattern
            for i in range(len(dates))
        ]
    })
    
    # Air quality data - hourly for last 7 days
    hourly_dates = pd.date_range(start=end_date - timedelta(days=7), end=end_date, freq='h')
    aqi_data = pd.DataFrame({
        'Date': hourly_dates,
        'AQI': [
            45 + np.random.normal(0, 10) + 
            8 * np.sin(i * 0.1) +     # Daily pattern
            5 * np.cos(i * 0.05)      # Hourly variation
            for i in range(len(hourly_dates))
        ],
        'PM2_5': [
            12 + np.random.normal(0, 3) + 
            2 * np.sin(i * 0.08)      # Daily pattern
            for i in range(len(hourly_dates))
        ],
        'PM10': [
            25 + np.random.normal(0, 5) + 
            3 * np.sin(i * 0.06)      # Daily pattern
            for i in range(len(hourly_dates))
        ]
    })
    
    # Traffic data - hourly for today
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    traffic_hours = pd.date_range(start=today_start, end=today_start + timedelta(days=1), freq='h')[:-1]
    
    # Realistic traffic patterns (rush hours, etc.)
    traffic_data = pd.DataFrame({
        'Hour': [h.hour for h in traffic_hours],
        'Traffic_Flow': [
            # Morning rush (7-9 AM), Evening rush (5-7 PM), Low traffic at night
            800 + 400 * np.exp(-((h - 8) ** 2) / 2) +  # Morning peak
            600 * np.exp(-((h - 18) ** 2) / 2) +       # Evening peak
            200 * np.exp(-((h - 2) ** 2) / 4) +        # Night low
            np.random.normal(0, 50)                    # Random variation
            for h in range(24)
        ],
        'Congestion_Level': [
            # Higher congestion during rush hours
            0.3 + 0.4 * np.exp(-((h - 8) ** 2) / 2) +   # Morning rush
            0.3 * np.exp(-((h - 18) ** 2) / 2) +        # Evening rush
            0.1 * np.exp(-((h - 2) ** 2) / 4) +         # Night low
            np.random.uniform(0, 0.1)                   # Random variation
            for h in range(24)
        ]
    })
    
    return energy_data, aqi_data, traffic_data

def render_real_time_clock():
    """Render a real-time clock with JavaScript updates"""
    current_time = datetime.now()
    time_str = current_time.strftime("%H:%M")
    date_str = current_time.strftime("%Y-%m-%d")
    day_str = current_time.strftime("%A")
    
    st.markdown(f"""
    <div class="real-time-clock" id="real-time-clock">
        <div>🕐 {time_str}</div>
        <div style="font-size: 1rem; color: #666;">{day_str}, {date_str}</div>
    </div>
    """, unsafe_allow_html=True)

def render_dynamic_dashboard():
    """Render the main dynamic dashboard"""
    
    # Initialize session state for auto-refresh
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    
    # Auto-refresh logic
    current_time = datetime.now()
    time_diff = (current_time - st.session_state.last_refresh).total_seconds()
    
    # Auto-refresh every 5 seconds if on dashboard
    if time_diff > 5:
        st.session_state.last_refresh = current_time
        st.rerun()
    
    # Header with real-time clock
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="main-header"><h1>🏙️ Smart City Dashboard</h1></div>', unsafe_allow_html=True)
    with col2:
        # Real-time clock with JavaScript updates
        render_real_time_clock()
    
    # Real-time status indicators
    st.subheader("🚦 Real-Time City Status")
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.markdown("""
        <div class="metric-card">
            <h4>⚡ Power Grid</h4>
            <span class="status-indicator status-good"></span>Stable
        </div>
        """, unsafe_allow_html=True)
    
    with status_col2:
        st.markdown("""
        <div class="metric-card">
            <h4>💧 Water Supply</h4>
            <span class="status-indicator status-good"></span>Normal
        </div>
        """, unsafe_allow_html=True)
    
    with status_col3:
        st.markdown("""
        <div class="metric-card">
            <h4>🌬️ Air Quality</h4>
            <span class="status-indicator status-good"></span>Good
        </div>
        """, unsafe_allow_html=True)
    
    # Key Performance Indicators
    st.subheader("📊 Key Performance Indicators")
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
    with kpi_col1:
        summary_card("Energy Consumption", "1.2 MWh", delta="2%", delta_color="inverse")
    with kpi_col2:
        summary_card("Water Usage", "8M Gallons", delta="-5%", delta_color="normal")
    with kpi_col3:
        summary_card("Air Quality (AQI)", "45", delta="0")
    
    # Generate sample data
    energy_data, aqi_data, traffic_data = generate_sample_data()
    
    # Interactive Charts Section
    st.subheader("📈 Real-Time Analytics")
    
    # Energy Consumption Chart
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_energy = go.Figure()
        fig_energy.add_trace(go.Scatter(
            x=energy_data['Date'], 
            y=energy_data['Energy_Consumption'],
            mode='lines',
            name='Total Energy',
            line=dict(color='#667eea', width=2)
        ))
        fig_energy.add_trace(go.Scatter(
            x=energy_data['Date'], 
            y=energy_data['Renewable_Energy'],
            mode='lines',
            name='Renewable Energy',
            line=dict(color='#28a745', width=2)
        ))
        fig_energy.update_layout(
            title="Energy Consumption Trends (Last 30 Days)",
            xaxis_title="Date",
            yaxis_title="Energy (MWh)",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_energy, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Air Quality Chart
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_aqi = go.Figure()
        fig_aqi.add_trace(go.Scatter(
            x=aqi_data['Date'], 
            y=aqi_data['AQI'],
            mode='lines+markers',
            name='Air Quality Index',
            line=dict(color='#ff6b6b', width=2),
            marker=dict(size=4)
        ))
        fig_aqi.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Good")
        fig_aqi.add_hline(y=100, line_dash="dash", line_color="orange", annotation_text="Moderate")
        fig_aqi.update_layout(
            title="Air Quality Index Over Time (Last 7 Days)",
            xaxis_title="Date & Time",
            yaxis_title="AQI",
            height=400
        )
        st.plotly_chart(fig_aqi, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Smart City Initiatives
    st.subheader("🌱 Smart City Initiatives")
    init_col1, init_col2, init_col3 = st.columns(3)
    
    with init_col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🌞 Solar Panel Installation</h4>
            <p>Progress: 75% Complete</p>
            <div style="background: #e9ecef; height: 10px; border-radius: 5px;">
                <div style="background: #28a745; height: 10px; border-radius: 5px; width: 75%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with init_col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🚌 Electric Bus Fleet</h4>
            <p>Progress: 60% Complete</p>
            <div style="background: #e9ecef; height: 10px; border-radius: 5px;">
                <div style="background: #007bff; height: 10px; border-radius: 5px; width: 60%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with init_col3:
        st.markdown("""
        <div class="metric-card">
            <h4>🌳 Urban Forest Project</h4>
            <p>Progress: 85% Complete</p>
            <div style="background: #e9ecef; height: 10px; border-radius: 5px;">
                <div style="background: #28a745; height: 10px; border-radius: 5px; width: 85%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Sidebar with enhanced styling
    with st.sidebar:
        st.markdown("## 🏙️ Smart City")
        st.markdown("### Navigation")
        
        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard", "Policy Search", "Chat", "Eco Tips", 
                "KPI Forecasting", "Anomaly Checker", "Report Generator", "Feedback"
            ],
            icons=[
                'house', 'search', 'chat-dots', 'lightbulb', 
                'graph-up-arrow', 'exclamation-triangle', 'journal-richtext', 'chat-left-text'
            ],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#2c3e50", "font-size": "18px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee", "color": "#2c3e50"},
                "nav-link-selected": {"background-color": "#02ab21", "color": "white"},
            }
        )
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        st.metric("Population", "2.3M")
        st.metric("Area", "1,200 km²")
        st.metric("GDP", "$45B")

    # Main content area
    if selected == "Dashboard":
        render_dynamic_dashboard()
    elif selected == "Policy Search":
        render_document_uploader()
        st.divider()
        render_policy_search()
        st.divider()
        render_policy_summarizer()
    elif selected == "Chat":
        render_chat_assistant()
    elif selected == "Eco Tips":
        render_eco_tips()
    elif selected == "KPI Forecasting":
        render_kpi_forecasting()
    elif selected == "Anomaly Checker":
        render_anomaly_checker()
    elif selected == "Report Generator":
        render_report_generator()
    elif selected == "Feedback":
        render_feedback_form()

if __name__ == "__main__":
    main() 