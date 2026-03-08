# AI Health Monitor & Stress Analyzer

A modern, AI-powered web application built with Streamlit that analyzes lifestyle and health factors to detect stress levels and provide personalized recommendations.

## Features

🧠 **AI-Powered Analysis**: Uses machine learning models to predict stress levels
📊 **Interactive Dashboard**: Beautiful visualizations and metrics
🎯 **Personalized Recommendations**: Tailored advice based on your health data
📱 **Responsive Design**: Works on desktop and mobile devices
⚡ **Real-time Analysis**: Instant results with visual feedback

## Project Structure

```
student_health_prediction/
├── app.py                 # Main Streamlit application
├── styles.css            # Custom CSS styling
├── student_stress_model.pkl    # ML model for student stress
├── health_stress_model.pkl     # ML model for health stress
├── Sleep_health_and_lifestyle_dataset.csv
└── Student Mental Health Analysis During Online Learning.csv
```

## Installation & Setup

1. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

2. **Activate Environment**:
   ```bash
   # Windows
   .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install streamlit pandas joblib plotly
   ```

4. **Run the Application**:
   ```bash
   cd student_health_prediction
   streamlit run app.py
   ```

## Usage

1. **Input Your Data**: Use the sidebar to enter your lifestyle and health metrics
2. **Analyze**: Click the "🔍 Analyze My Stress Level" button
3. **Review Results**: Check your stress level, causes, and recommendations
4. **Monitor Progress**: Use the health metrics dashboard to track improvements

## Features Overview

### Input Sections
- **Lifestyle Factors**: Screen time, physical activity, sleep, age, education
- **Health Metrics**: Gender, age, occupation, sleep quality, heart rate, daily steps, blood pressure

### Analysis Results
- **Stress Level Gauge**: Visual indicator of your current stress level
- **Possible Causes**: Factors contributing to your stress
- **AI Recommendations**: Personalized tips for improvement
- **Health Metrics Dashboard**: Key health indicators with comparisons
- **Overall Health Score**: Comprehensive health assessment

## Technologies Used

- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning models
- **Pandas**: Data manipulation
- **Joblib**: Model serialization

## Model Information

The app uses two pre-trained machine learning models:
- **Student Stress Model**: Predicts stress based on lifestyle factors
- **Health Stress Model**: Predicts stress based on health metrics

Both models are trained on relevant datasets and provide accurate stress level predictions.

## Customization

### Styling
Modify `styles.css` to customize the appearance:
- Color schemes
- Layout spacing
- Typography
- Responsive design

### Models
Replace the `.pkl` files with your own trained models (ensure same input format)

## Contributing

Feel free to enhance the UI, add new features, or improve the ML models!

## License

This project is open source and available under the MIT License.