---
name: advanced-data-analyst
description: |
  Advanced data analysis and visualization skill for complex datasets, machine learning, and automated reporting. 
  Triggers when user mentions 'data analysis', 'machine learning', 'visualization', 'automated reporting', 
  'predictive analytics', or 'dashboard creation'.
---

## 🎯 Advanced Data Analyst Skill

### 📊 **Core Capabilities**
- **Advanced Data Analysis**: Complex statistical analysis, trend identification, pattern recognition
- **Machine Learning**: Supervised/unsupervised learning, model training, prediction systems
- **Data Visualization**: Interactive charts, dashboards, reports, 3D visualizations
- **Automated Reporting**: Scheduled reports, real-time dashboards, alert systems
- **Predictive Analytics**: Forecasting, anomaly detection, recommendation systems

### 🛠️ **Available Tools**
- **Data Processing**: pandas, numpy, scipy, polars
- **Visualization**: matplotlib, seaborn, plotly, bokeh, dash
- **Machine Learning**: scikit-learn, tensorflow, pytorch, xgboost
- **Web Apps**: flask, streamlit, dash, plotly dash
- **Automation**: schedule, celery, airflow
- **Database**: sqlite, postgresql, mongodb, redis

### 🚀 **Quick Start Examples**

#### 1. **Advanced Data Analysis**
```python
# Analyze complex datasets with statistical methods
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Load and analyze data
df = pd.read_csv('data.csv')
print(f"Dataset shape: {df.shape}")
print(f"Statistical summary:\n{df.describe()}")

# Advanced correlation analysis
correlation_matrix = df.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Advanced Correlation Analysis')
plt.show()
```

#### 2. **Machine Learning Pipeline**
```python
# Complete ML pipeline with model training
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler

# Prepare data
X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))
```

#### 3. **Interactive Dashboard**
```python
# Create interactive dashboard with Plotly Dash
import dash
from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Advanced Analytics Dashboard"),
    dcc.Graph(id='correlation-heatmap'),
    dcc.Graph(id='feature-importance'),
    html.Div(id='data-table')
])

@app.callback(
    [dash.dependencies.Output('correlation-heatmap', 'feature-importance')],
    [dash.dependencies.Input('data-source')]
def update_charts(data_source):
    # Create advanced visualizations
    pass
```

#### 4. **Automated Reporting System**
```python
# Automated reporting with scheduling
import schedule
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generate_automated_report():
    """Generate and send automated reports"""
    # Load latest data
    df = pd.read_csv('latest_data.csv')
    
    # Perform analysis
    analysis_results = perform_advanced_analysis(df)
    
    # Create visualizations
    charts = create_visualizations(df)
    
    # Generate report
    report_html = create_html_report(analysis_results, charts)
    
    # Send report
    send_email_report(report_html)
    
    print(f"Report generated at {datetime.now()}")

# Schedule automated reports
schedule.every().day.at("09:00").do(generate_automated_report)
```

### 🎯 **Use Cases**

#### **Business Intelligence**
- Sales forecasting and trend analysis
- Customer behavior analytics
- Market research and competitive analysis
- Financial modeling and risk assessment

#### **Scientific Research**
- Experimental data analysis
- Statistical modeling and hypothesis testing
- Research visualization and publication
- Automated data collection and processing

#### **Web Analytics**
- User behavior analysis
- A/B testing and conversion optimization
- Real-time dashboard creation
- Automated reporting systems

#### **Predictive Analytics**
- Sales forecasting
- Customer churn prediction
- Demand planning
- Anomaly detection

### 🔧 **Configuration**

#### Environment Setup
```bash
# Install required packages
pip install pandas numpy scipy matplotlib seaborn plotly dash
pip install scikit-learn tensorflow pytorch xgboost
pip install streamlit flask schedule celery
pip install sqlalchemy psycopg2 redis
```

#### Data Sources
```python
# Configure data sources
DATA_SOURCES = {
    'database': 'postgresql://user:pass@localhost/db',
    'api': 'https://api.example.com/data',
    'file': '/path/to/data.csv',
    'stream': 'kafka://localhost:9092'
}
```

### 📈 **Advanced Features**

#### **Real-time Analytics**
```python
# Real-time data processing
import asyncio
import websockets
from datetime import datetime

async def real_time_analytics():
    """Process real-time data streams"""
    while True:
        # Get latest data
        data = await get_real_time_data()
        
        # Perform analysis
        insights = analyze_real_time_data(data)
        
        # Update dashboard
        update_dashboard(insights)
        
        # Check for alerts
        check_alerts(insights)
        
        await asyncio.sleep(60)  # Update every minute
```

#### **Machine Learning Operations**
```python
# Advanced ML operations
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Create advanced ML pipeline
ml_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', VotingClassifier([
        ('rf', RandomForestClassifier()),
        ('xgb', XGBClassifier()),
        ('svm', SVC())
    ]))
```

### 📊 **Visualization Gallery**

#### **Interactive Charts**
- **3D Scatter Plots**: Multi-dimensional data visualization
- **Heatmaps**: Correlation and pattern analysis
- **Time Series**: Trend analysis and forecasting
- **Geospatial**: Location-based data visualization
- **Network Graphs**: Relationship mapping

#### **Advanced Dashboards**
- **Executive Dashboards**: KPI monitoring and reporting
- **Operational Dashboards**: Real-time system monitoring
- **Analytical Dashboards**: Deep-dive data exploration
- **Predictive Dashboards**: Forecasting and prediction systems

### 🤖 **Machine Learning Models**

#### **Supervised Learning**
- **Classification**: Binary and multi-class classification
- **Regression**: Linear, polynomial, tree-based models
- **Ensemble Methods**: Random forests, gradient boosting, voting classifiers
- **Neural Networks**: Deep learning for complex patterns

#### **Unsupervised Learning**
- **Clustering**: K-means, hierarchical, DBSCAN
- **Dimensionality Reduction**: PCA, t-SNE, UMAP
- **Anomaly Detection**: Isolation forests, one-class SVM
- **Association Rules**: Market basket analysis

#### **Time Series**
- **Forecasting**: ARIMA, Prophet, LSTM
- **Anomaly Detection**: Seasonal decomposition, statistical tests
- **Trend Analysis**: Decomposition, smoothing techniques

### 📋 **Reporting Templates**

#### **Executive Reports**
```python
# Generate executive-level reports
def create_executive_report(data):
    """Create comprehensive executive report"""
    report = {
        'summary': data.describe(),
        'key_insights': extract_key_insights(data),
        'recommendations': generate_recommendations(data),
        'visualizations': create_executive_charts(data)
    }
    return report
```

#### **Technical Reports**
```python
# Generate detailed technical reports
def create_technical_report(data):
    """Create detailed technical analysis report"""
    report = {
        'statistical_analysis': perform_statistical_tests(data),
        'model_performance': evaluate_models(data),
        'feature_importance': analyze_feature_importance(data),
        'code_examples': provide_code_examples()
    }
    return report
```

### 🔄 **Automation Features**

#### **Scheduled Tasks**
- Daily/weekly/monthly report generation
- Data quality monitoring
- Model performance tracking
- Automated alert systems

#### **Alert Systems**
- Threshold-based alerts
- Anomaly detection alerts
- Performance degradation alerts
- Data quality alerts

### 🎯 **Best Practices**

#### **Data Quality**
- Data validation and cleaning
- Missing value handling
- Outlier detection and treatment
- Data type optimization

#### **Model Management**
- Model versioning and tracking
- Performance monitoring
- Model retraining schedules
- A/B testing frameworks

#### **Security**
- Data encryption and protection
- Access control and permissions
- Audit trails and logging
- Compliance checking

### 📚 **Documentation**

#### **Code Documentation**
- Function docstrings and type hints
- README files and usage examples
- API documentation
- Architecture diagrams

#### **Data Documentation**
- Data dictionaries and schemas
- Lineage documentation
- Quality reports
- Processing logs

### 🚀 **Getting Started**

1. **Install Dependencies**
```bash
pip install advanced-data-analyst
```

2. **Configure Environment**
```python
# Set up configuration
from advanced_data_analyst import DataAnalyst

analyst = DataAnalyst(
    data_sources=['database', 'api', 'file'],
    ml_models=['random_forest', 'xgboost', 'neural_network'],
    visualizations=['plotly', 'seaborn', 'bokeh']
)
```

3. **Start Analysis**
```python
# Begin advanced analysis
results = analyst.analyze_dataset('your_data.csv')
analyst.create_dashboard(results)
analyst.generate_report(results)
```

### 🎯 **Support and Maintenance**

#### **Troubleshooting**
- Common error solutions
- Performance optimization
- Memory management
- Debugging techniques

#### **Updates and Maintenance**
- Regular model retraining
- Data source updates
- Security patches
- Feature enhancements

---

## 🎯 **Ready to Use**

This skill is now ready to help with advanced data analysis, machine learning, and automated reporting. Simply mention any of the trigger phrases to activate these capabilities!