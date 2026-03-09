import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
from report_generator import generate_report

BASE_DIR = os.path.dirname(__file__)

student_model = joblib.load(os.path.join(BASE_DIR, "student_stress_model.pkl"))
health_model = joblib.load(os.path.join(BASE_DIR, "health_stress_model.pkl"))

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
load_css(os.path.join(BASE_DIR, "styles.css"))

st.set_page_config(
    page_title="AI Health Monitor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown('<h1 class="main-header">🧠 AI Health Monitor & Stress Analyzer</h1>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <p style='font-size: 1.2rem; color: #666;'>Analyze your lifestyle and health factors to detect stress levels with AI-powered insights</p>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown('<h2 class="sidebar-header">📝 Input Your Data</h2>', unsafe_allow_html=True)

    # Lifestyle Section
    st.markdown("### 🏃‍♂️ Lifestyle Factors")
    col1, col2 = st.columns(2)
    with col1:
        screen_time = st.slider("📱 Screen Time (hrs/day)", 0, 12, 5, key="screen_time")
        physical_activity = st.slider("💪 Physical Activity (hrs/week)", 0, 15, 3, key="physical_activity")
    with col2:
        sleep_duration = st.slider("😴 Sleep Duration (hrs)", 0, 12, 7, key="sleep_duration")
        age = st.slider("🎂 Age", 15, 60, 21, key="age_lifestyle")

    education = st.selectbox(
        "🎓 Education_Category",
        [0,1,2],
        key="education"
    )

    st.markdown("---")

    st.markdown("### 🏥 Health Metrics")
    col3, col4 = st.columns(2)
    with col3:
        Gender = st.selectbox("⚧ Gender", ["Male", "Female"], key="gender_select")
        Age = st.slider("🎂 Age", 15, 60, 21, key="age_health")
        Occupation = st.selectbox("💼 Occupation", ["Student", "Employed", "Unemployed"], key="occupation_select")
    with col4:
        Sleep_Duration = st.slider("😴 Sleep Duration (hrs)", 0, 12, 7, key="sleep_duration_health")
        Quality_of_Sleep = st.slider("🌙 Quality of Sleep (1-10)", 1, 10, 6, key="quality_of_sleep")
        Physical_Activity_Level = st.slider("🏃‍♂️ Activity Level (1-10)", 1, 10, 5, key="physical_activity_level")

    col5, col6 = st.columns(2)
    with col5:
        heart_rate = st.slider("❤️ Heart Rate (bpm)", 50, 120, 75, key="heart_rate")
        daily_steps = st.slider("👣 Daily Steps", 0, 15000, 6000, key="daily_steps")
    with col6:
        systolic_bp = st.slider("🩸 Systolic BP", 90, 180, 120, key="systolic_bp")
        diastolic_bp = st.slider("🩸 Diastolic BP", 60, 120, 80, key="diastolic_bp")

    Gender = 1 if Gender == "Female" else 0
    Occupation = ["Student", "Employed", "Unemployed"].index(Occupation)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_button = st.button("🔍 Analyze My Stress Level", use_container_width=True, type="primary")

if analyze_button:

    
    student_input = pd.DataFrame({
        "Physical Activity (hrs/week)": [physical_activity],
        "Screen Time (hrs/day)": [screen_time],
        "Sleep Duration (hrs)": [sleep_duration],
        "Age": [age],
        "Education_Category": [education]
    })

    student_pred = student_model.predict(student_input)[0]

    
    health_input = pd.DataFrame({
        "Gender":[Gender],    
        "Age":[Age],
        "Occupation":[Occupation],   
        "Sleep Duration":[Sleep_Duration],
        "Quality of Sleep":[Quality_of_Sleep],
        "Physical Activity Level":[Physical_Activity_Level],
        "Heart Rate":[heart_rate],
        "Daily Steps":[daily_steps],
        "Systolic_BP":[systolic_bp],
        "Diastolic_BP":[diastolic_bp]
    })

    health_pred = health_model.predict(health_input)[0]

    student_stress_map = {1: "Low", 2: "Medium", 3: "High"}
    student_pred_text = student_stress_map.get(student_pred, str(student_pred))
    
    if health_pred <= 5:
        health_pred_text = "Low"
    elif health_pred <= 6.5:
        health_pred_text = "Medium"
    else:
        health_pred_text = "High"

    stress_priority = {"High": 3, "Medium": 2, "Low": 1}
    stress_levels = [student_pred_text, health_pred_text]
    final_stress = max(stress_levels, key=lambda x: stress_priority.get(x, 0))
    causes = []
    if screen_time > 6:
        causes.append("High Screen Time")
    if sleep_duration < 6:
        causes.append("Low Sleep Duration")
    if physical_activity < 2:
        causes.append("Low Physical Activity")
    if daily_steps < 4000:
        causes.append("Low Daily Steps")
    if heart_rate > 90:
        causes.append("High Heart Rate")

    tips = []
    if screen_time > 6:
        tips.append("Reduce screen time below 5 hours")
    if sleep_duration < 7:
        tips.append("Sleep at least 7–8 hours daily")
    if physical_activity < 3:
        tips.append("Exercise 30 minutes daily")
    if daily_steps < 6000:
        tips.append("Try to walk 6000–8000 steps daily")
    if heart_rate > 90:
        tips.append("Practice relaxation techniques like meditation")


    with st.expander("🔧 Model Predictions (Debug)"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Student Model", f"{student_pred} → {student_pred_text}")
        with col_b:
            st.metric("Health Model", f"{health_pred} → {health_pred_text}")

    # Enhanced Stress Result Display
    st.markdown("---")
    st.subheader("📊 Stress Analysis Result")

    # Stress level indicator
    stress_colors = {"High": "#ff6b6b", "Medium": "#ffd93d", "Low": "#6bcf7f"}
    stress_icons = {"High": "⚠️", "Medium": "⭕", "Low": "✅"}

    # Create a visual stress gauge
    stress_value = {"Low": 25, "Medium": 50, "High": 85}[final_stress]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stress_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Stress Level: {final_stress}"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': stress_colors[final_stress]},
            'steps': [
                {'range': [0, 33], 'color': "#6bcf7f"},
                {'range': [33, 66], 'color': "#ffd93d"},
                {'range': [66, 100], 'color': "#ff6b6b"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': stress_value
            }
        }
    ))

    col_gauge, col_result = st.columns([1, 1])
    with col_gauge:
        st.plotly_chart(fig, use_container_width=True)

    with col_result:
        if final_stress == "High":
            st.markdown(f"""
            <div class="stress-card high-stress">
                <h3>{stress_icons[final_stress]} High Stress Detected</h3>
                <p>Your current lifestyle and health metrics indicate high stress levels. Immediate attention recommended.</p>
            </div>
            """, unsafe_allow_html=True)
        elif final_stress == "Medium":
            st.markdown(f"""
            <div class="stress-card medium-stress">
                <h3>{stress_icons[final_stress]} Moderate Stress Level</h3>
                <p>Your metrics show moderate stress. Consider making some lifestyle adjustments.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="stress-card low-stress">
                <h3>{stress_icons[final_stress]} Low Stress Level</h3>
                <p>Great! Your current lifestyle appears to be managing stress well.</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns(2)

    report_path = generate_report(final_stress, heart_rate, daily_steps, sleep_duration)

    with open(report_path, "rb") as file:
        st.download_button(
            label="📥 Download Health Report",
            data=file,
            file_name="health_report.pdf",
            mime="application/pdf"
        )

    with col_left:
        st.subheader("🔍 Possible Causes")
        if causes:
            for c in causes:
                st.markdown(f"• {c}")
        elif final_stress == "High":
            st.markdown("⚠️ **High stress detected** - Review your health metrics")
        elif final_stress == "Medium":
            st.markdown("⭕ **Moderate stress detected** - Some lifestyle adjustments needed")
        else:
            st.markdown("✅ **No major stress-causing factors detected!**")

    with col_right:
        st.subheader("💡 AI Recommendations")
        if tips:
            for t in tips:
                st.markdown(f"✔ {t}")
        elif final_stress == "High":
            st.markdown("✔ Reduce stress through meditation and relaxation")
            st.markdown("✔ Increase physical activity")
            st.markdown("✔ Ensure 7-8 hours of sleep daily")
        elif final_stress == "Medium":
            st.markdown("✔ Add more physical activity to your routine")
            st.markdown("✔ Maintain consistent sleep schedule")
        else:
            st.markdown("✅ **Keep maintaining your healthy lifestyle!**")

    st.markdown("---")
    st.subheader("📈 Your Health Metrics Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("❤️ Heart Rate", f"{heart_rate} bpm", delta="Normal" if 60 <= heart_rate <= 100 else "Check")
    with col2:
        st.metric("👣 Daily Steps", f"{daily_steps:,}", delta="Good" if daily_steps >= 6000 else "Low")
    with col3:
        st.metric("😴 Sleep Quality", f"{Quality_of_Sleep}/10", delta="Excellent" if Quality_of_Sleep >= 8 else "Fair")
    with col4:
        st.metric("💪 Activity Level", f"{Physical_Activity_Level}/10", delta="Active" if Physical_Activity_Level >= 7 else "Sedentary")

    st.markdown("### Lifestyle Comparison")
    df_chart = pd.DataFrame({
        "Metric": ["Screen Time", "Sleep Duration", "Physical Activity"],
        "Your Value": [screen_time, sleep_duration, physical_activity],
        "Recommended": [5, 8, 5]  # Recommended values
    })

    fig = px.bar(df_chart, x="Metric", y=["Your Value", "Recommended"],
                 barmode='group',
                 color_discrete_sequence=['#667eea', '#764ba2'],
                 title="Your Lifestyle vs Recommended Values")

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        title_font_size=16
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🏆 Health Score Summary")

    health_score = 0
    health_score += min(100, (8 - abs(sleep_duration - 8)) * 12.5)  # Sleep score
    health_score += min(100, (heart_rate - 50) / 0.7) if heart_rate <= 100 else max(0, 100 - (heart_rate - 100) * 2)  # Heart rate score
    health_score += min(100, daily_steps / 100)  # Steps score
    health_score += min(100, Quality_of_Sleep * 10)  # Sleep quality score
    health_score = min(100, health_score / 4)  # Average

    col_score, col_desc = st.columns([1, 2])
    with col_score:
        fig_score = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=health_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Health Score"},
            delta={'reference': 75},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#6bcf7f" if health_score >= 70 else "#ffd93d" if health_score >= 50 else "#ff6b6b"},
                'steps': [
                    {'range': [0, 50], 'color': "#ff6b6b"},
                    {'range': [50, 70], 'color': "#ffd93d"},
                    {'range': [70, 100], 'color': "#6bcf7f"}
                ]
            }
        ))
        st.plotly_chart(fig_score, use_container_width=True)
        
        report_path = generate_report(final_stress, heart_rate, daily_steps, sleep_duration)


    # with col_desc:
    #     if health_score >= 70:
    #         st.success("🌟 **Excellent Health Score!** Keep up the great work!")
    #     elif health_score >= 60:
    #         st.info("👍 **Good Health Score.** You're on the right track!")
    #     elif health_score >= 40:
    #         st.warning("⚠️ **Fair Health Score.** Consider making some improvements.")
    #     else:
    #         st.error("🚨 **Poor Health Score.** Immediate lifestyle changes recommended.")