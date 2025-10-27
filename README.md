# SME/MSME Business Insights AI Agent

This project is an AI-powered business insights tool designed specifically for Small and Medium Enterprises (SMEs/MSMEs). It provides advanced analytics, financial insights, and business recommendations using Generative AI.

## Features

- Interactive dashboard with key business metrics
- AI-powered chat interface for business queries
- Financial analysis and trend visualization
- Real-time insights and recommendations
- Easy-to-use Streamlit interface

## Technical Stack

- LLM: Mistral (via Ollama)
- Agent Framework: LangChain
- Vector Database: ChromaDB
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Frontend: Streamlit
- Data Storage: CSV

## Setup Instructions

1. Install Ollama and download the Mistral model:
```bash
# Install Ollama from https://ollama.ai/
ollama pull mistral
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Start the Ollama server:
```bash
ollama serve
```

4. Run the Streamlit application:
```bash
streamlit run app.py
```

## Usage

1. **Dashboard**: View key business metrics and trends
2. **Chat with AI**: Ask questions about your business data
3. **Financial Analysis**: Deep dive into financial metrics and period-wise analysis

## Sample Queries

- "What was the profit in May 2023?"
- "Suggest strategies to improve profits"
- "Summarize business performance in Q1 2023"
- "Show me the sales trend"
- "What's the average customer count?"

## Project Structure

```
.
├── data/
│   └── sample_data.csv
├── app.py
├── business_insights_agent.py
├── requirements.txt
└── README.md
```