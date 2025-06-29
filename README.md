# 🌆 Sustainable Smart City Assistant

A smart chatbot that answers queries related to sustainable cities using IBM Watsonx Granite LLM. Built using **FastAPI** for the backend and **Streamlit** for the frontend.

# Project Features

- Ask questions related to Smart City infrastructure, sustainability, transport, energy, etc.
- AI-generated responses using IBM Watsonx Granite LLM (Granite 13B Chat v2).
- Built using:
  - 🔹 FastAPI (Backend)
  - 🔹 Streamlit (Frontend)
  - 🔹 IBM Watsonx.ai (LLM API)
  - 🔹 Pinecone (optional for semantic memory)

# Project Structure

SustainableSmartCityAssistant/
│
├── frontend/                    # Streamlit UI
│   └── dashboard.py
│
├── backend/                     # FastAPI backend
│   ├── main.py
│   ├── routes/
│   │   ├── summarize.py
│   │   ├── chat.py
│   │   ├── search.py
│   │   └── forecast.py
│   ├── models/
│   │   └── linear_regression.py
│   ├── utils/
│   │   ├── file_parser.py
│   │   ├── embedding.py
│   │   └── granite_api.py
│   ├── .env
│   └── requirements.txt
│
├── data/
│   ├── sample_kpi.csv
│   ├── smart_city_policy.txt
│   └── config.json
│
└── README.md

# Configure API Credentials or Environment Variables (.env)

WATSONX_API_KEY=your_api_key           # IBM watsonx API key for LLM services
WATSONX_PROJECT_ID=your_project_id     # IBM watsonx project identifier
WATSONX_URL=your_url                   # IBM watsonx API endpoint URL
WATSONX_MODEL_ID=your_model_id         # IBM watsonx model ID for LLM
PINECONE_API_KEY=your_pinecone_key     # Pinecone vector DB API key
PINECONE_ENV=your_pinecone_env         # Pinecone environment (e.g., us-east1-gcp)
INDEX_NAME=your_index_name             # Pinecone index name for document search

#  Run Backend
cd backend
uvicorn main:app --reload

#  Run Frontend
cd ../frontend
streamlit run dashboard.py
# Requirements
fastapi
uvicorn
pydantic
python-dotenv
requests
streamlit
ibm-watsonx-ai>=1.3.0
Python 3.8+
See requirements.txt for Python packages

# Clone the repository:
git clone <your-repo-url>
cd city
# Install dependencies:
pip install -r requirements.txt
# Run the dashboard:
streamlit run smart_dashboard.py

# Customization
Add your own data in the sample_data/ folder or connect to live sources.
Update backend endpoints in the UI files if your API runs elsewhere.