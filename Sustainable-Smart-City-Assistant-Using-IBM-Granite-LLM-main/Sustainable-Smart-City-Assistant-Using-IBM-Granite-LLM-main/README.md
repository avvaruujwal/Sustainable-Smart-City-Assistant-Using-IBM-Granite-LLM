# 🏙️ Smart City Dashboard

A modern, interactive dashboard for monitoring and managing smart city KPIs, policies, and sustainability initiatives. Built with Streamlit and Plotly, this dashboard provides real-time analytics, AI-powered chat, policy search, anomaly detection, forecasting, and more.

## Features
- **Real-Time Dashboard:** Visualize energy, water, air quality, and traffic KPIs with live charts and status indicators.
- **AI Chat Assistant:** Get instant answers and support from an integrated AI assistant.
- **Policy Search & Summarization:** Search and summarize city policies using semantic search and AI.
- **KPI Forecasting:** Upload your data and generate 30-day forecasts for key metrics.
- **Anomaly Detection:** Detect unusual patterns in your city data.
- **Eco Tips:** Receive personalized eco-friendly tips.
- **Feedback & Reporting:** Submit feedback and generate sustainability reports.

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd city
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the dashboard:**
   ```bash
   streamlit run smart_dashboard.py
   ```
4. **(Optional) Start the backend API:**
   - Ensure your FastAPI backend is running if you want chat, policy, and data features to work.

## Project Structure
```
city/
  app/                # Backend FastAPI app (APIs, services)
  ui/                 # Streamlit UI components
  smart_dashboard.py  # Main Streamlit dashboard app
  requirements.txt    # Python dependencies
```

## Environment Variables (.env)
Some features (such as API endpoints, secret keys, or database connections) require configuration via a `.env` file in the project root. This file is not included by default for security reasons.

**`.env` file:**
```env
WATSONX_API_KEY=your_api_key           # IBM watsonx API key for LLM services
WATSONX_PROJECT_ID=your_project_id     # IBM watsonx project identifier
WATSONX_URL=your_url                   # IBM watsonx API endpoint URL
WATSONX_MODEL_ID=your_model_id         # IBM watsonx model ID for LLM
PINECONE_API_KEY=your_pinecone_key     # Pinecone vector DB API key
PINECONE_ENV=your_pinecone_env         # Pinecone environment (e.g., us-east1-gcp)
INDEX_NAME=your_index_name             # Pinecone index name for document search
```

- Make sure to update the `.env` file with your actual configuration values.
- The application will automatically load these variables if you use a package like `python-dotenv` or configure your environment accordingly. 

## Requirements
- Python 3.8+
- See `requirements.txt` for Python packages

## Customization
- Add your own data in the `sample_data/` folder or connect to live sources.
- Update backend endpoints in the UI files if your API runs elsewhere.

---
*Created for smart city innovation and sustainability.* 
