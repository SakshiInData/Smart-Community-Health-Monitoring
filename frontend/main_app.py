import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Community Health Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
    }
    .risk-high {
        background-color: #ff4b4b;
        color: white;
        padding: 5px;
        border-radius: 5px;
        text-align: center;
    }
    .risk-medium {
        background-color: #ffa64b;
        color: white;
        padding: 5px;
        border-radius: 5px;
        text-align: center;
    }
    .risk-low {
        background-color: #4bff4b;
        color: black;
        padding: 5px;
        border-radius: 5px;
        text-align: center;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
if 'submissions' not in st.session_state:
    st.session_state.submissions = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Mock data generation functions
def generate_sample_data():
    # Generate sample health reports
    symptoms = ["Fever", "Diarrhea", "Vomiting", "Dehydration", "Stomach pain"]
    villages = ["Village A", "Village B", "Village C", "Village D"]
    
    reports = []
    for i in range(50):
        date = datetime.now() - timedelta(days=np.random.randint(0, 30))
        reports.append({
            "date": date.date(),
            "village": np.random.choice(villages),
            "symptom": np.random.choice(symptoms),
            "cases": np.random.randint(1, 10),
            "water_quality": np.random.choice(["Good", "Fair", "Poor"]),
            "reported_by": f"ASHA {np.random.randint(1, 10)}"
        })
    
    return pd.DataFrame(reports)

def generate_water_quality_data():
    # Generate sample water quality data
    locations = ["Location A", "Location B", "Location C", "Location D", "Location E"]
    
    water_data = []
    for loc in locations:
        for i in range(10):
            date = datetime.now() - timedelta(days=np.random.randint(0, 30))
            water_data.append({
                "date": date.date(),
                "location": loc,
                "ftk_test_result": np.random.choice(["Safe", "Contaminated"]),
                "contamination_level": np.random.randint(0, 100),
                "water_source": np.random.choice(["Well", "Tap", "Pond", "River"])
            })
    
    return pd.DataFrame(water_data)

def generate_environmental_data():
    # Generate sample environmental data
    locations = ["Village A", "Village B", "Village C", "Village D"]
    
    env_data = []
    for loc in locations:
        for i in range(30):
            date = datetime.now() - timedelta(days=30-i)
            env_data.append({
                "date": date.date(),
                "location": loc,
                "rainfall": np.random.randint(0, 50),
                "temperature": np.random.randint(20, 40),
                "flood_risk": np.random.choice(["Low", "Medium", "High"])
            })
    
    return pd.DataFrame(env_data)

# Risk calculation function (simple threshold-based for MVP)
def calculate_risk(health_data, water_data, environmental_data):
    # Simple risk calculation based on:
    # 1. Number of recent disease cases
    # 2. Water contamination levels
    # 3. Recent rainfall (flood risk)
    
    recent_cases = health_data[health_data['date'] > (datetime.now() - timedelta(days=7)).date()]
    case_count = recent_cases['cases'].sum()
    
    recent_water_issues = water_data[
        (water_data['date'] > (datetime.now() - timedelta(days=7)).date()) & 
        (water_data['ftk_test_result'] == 'Contaminated')
    ]
    water_risk = len(recent_water_issues) * 10
    
    recent_rainfall = environmental_data[
        environmental_data['date'] > (datetime.now() - timedelta(days=3)).date()
    ]
    rainfall_risk = recent_rainfall['rainfall'].mean() / 10
    
    total_risk = min(100, case_count + water_risk + rainfall_risk)
    
    if total_risk > 50:
        return "High", total_risk
    elif total_risk > 20:
        return "Medium", total_risk
    else:
        return "Low", total_risk

# Main app
def main():
    st.title("🏥 Smart Community Health Monitoring & Early Warning System")
    st.markdown("---")
    
    # Generate sample data
    health_data = generate_sample_data()
    water_data = generate_water_quality_data()
    environmental_data = generate_environmental_data()
    
    # Calculate overall risk
    risk_level, risk_score = calculate_risk(health_data, water_data, environmental_data)
    
    # Display risk alert
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if risk_level == "High":
            st.error(f"🚨 HIGH RISK ALERT: Potential outbreak detected (Score: {risk_score:.1f})")
        elif risk_level == "Medium":
            st.warning(f"⚠️ MEDIUM RISK: Elevated risk of water-borne diseases (Score: {risk_score:.1f})")
        else:
            st.success(f"✅ LOW RISK: Conditions appear normal (Score: {risk_score:.1f})")
    
    st.markdown("---")
    
    # Dashboard metrics
    st.subheader("Community Health Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Total Cases This Month", health_data['cases'].sum())
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        contaminated_sources = water_data[water_data['ftk_test_result'] == 'Contaminated']['location'].nunique()
        st.metric("Contaminated Water Sources", contaminated_sources)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        high_rainfall = environmental_data[environmental_data['rainfall'] > 30]['date'].nunique()
        st.metric("High Rainfall Days", high_rainfall)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        asha_reporting = health_data['reported_by'].nunique()
        st.metric("Active ASHA Workers", asha_reporting)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Data visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Disease Cases by Village")
        cases_by_village = health_data.groupby('village')['cases'].sum().reset_index()
        fig = px.bar(cases_by_village, x='village', y='cases', color='village')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Water Quality Overview")
        water_quality_counts = water_data['ftk_test_result'].value_counts().reset_index()
        fig = px.pie(water_quality_counts, values='count', names='ftk_test_result')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Symptom Trends")
        symptom_trends = health_data.groupby(['date', 'symptom'])['cases'].sum().reset_index()
        fig = px.line(symptom_trends, x='date', y='cases', color='symptom')
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Rainfall Data")
        rainfall_trend = environmental_data.groupby('date')['rainfall'].mean().reset_index()
        fig = px.line(rainfall_trend, x='date', y='rainfall')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Data collection form (simulated)
    st.subheader("Submit Health Report (ASHA Worker)")
    
    with st.form("health_report_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            village = st.selectbox("Village", ["Village A", "Village B", "Village C", "Village D"])
            symptom = st.selectbox("Symptom", ["Fever", "Diarrhea", "Vomiting", "Dehydration", "Stomach pain"])
            cases = st.number_input("Number of Cases", min_value=1, max_value=50, value=1)
        
        with col2:
            water_quality = st.selectbox("Water Quality Observation", ["Good", "Fair", "Poor"])
            comments = st.text_area("Additional Comments")
            reported_by = st.text_input("Reported By (ASHA ID)")
        
        submitted = st.form_submit_button("Submit Report")
        
        if submitted:
            # Simulate form submission
            new_report = {
                "date": datetime.now().date(),
                "village": village,
                "symptom": symptom,
                "cases": cases,
                "water_quality": water_quality,
                "reported_by": reported_by,
                "timestamp": datetime.now()
            }
            
            st.session_state.submissions.append(new_report)
            st.success("Report submitted successfully!")
            
            # Check if this triggers an alert
            if cases >= 5 or water_quality == "Poor":
                alert_msg = f"Alert: {cases} cases of {symptom} reported in {village}. Water quality: {water_quality}"
                st.session_state.alerts.append({
                    "timestamp": datetime.now(),
                    "message": alert_msg,
                    "priority": "High" if cases >= 10 else "Medium"
                })
                st.warning(f"⚠️ Alert generated: {alert_msg}")
    
    # Display recent submissions
    if st.session_state.submissions:
        st.subheader("Recent Submissions")
        submissions_df = pd.DataFrame(st.session_state.submissions)
        st.dataframe(submissions_df.tail(5))
    
    # Alert management section
    st.markdown("---")
    st.subheader("Early Warning Alerts")
    
    if st.session_state.alerts:
        for alert in st.session_state.alerts[-5:]:  # Show last 5 alerts
            if alert['priority'] == 'High':
                st.error(f"🚨 {alert['timestamp'].strftime('%Y-%m-%d %H:%M')}: {alert['message']}")
            else:
                st.warning(f"⚠️ {alert['timestamp'].strftime('%Y-%m-%d %H:%M')}: {alert['message']}")
    else:
        st.info("No active alerts at this time.")
    
    # Alert action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Send SMS Alert to Community"):
            st.success("SMS alert sent to community stakeholders!")
    with col2:
        if st.button("Notify Health Department"):
            st.success("Health department notified!")
    with col3:
        if st.button("Request Water Testing"):
            st.success("Water testing team dispatched!")
    
    # Data export
    st.markdown("---")
    st.subheader("Data Export")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.download_button(
            label="Download Health Data",
            data=health_data.to_csv(index=False),
            file_name="health_data.csv",
            mime="text/csv"
        ):
            st.success("Health data downloaded!")
    with col2:
        if st.download_button(
            label="Download Water Quality Data",
            data=water_data.to_csv(index=False),
            file_name="water_quality_data.csv",
            mime="text/csv"
        ):
            st.success("Water quality data downloaded!")
    with col3:
        if st.download_button(
            label="Download Environmental Data",
            data=environmental_data.to_csv(index=False),
            file_name="environmental_data.csv",
            mime="text/csv"
        ):
            st.success("Environmental data downloaded!")

if __name__ == "__main__":
    main()