import os
from typing import Dict, List, Any
import pandas as pd
import numpy as np
import streamlit as st
from langchain.llms import Ollama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import Document

class BusinessInsightsAgent:
    def __init__(self, data_path: str):
        """Initialize the Business Insights Agent"""
        self.data_path = data_path
        self.data = None
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.memory = None
        self.qa_chain = None
        self._refresh_data()

    def _refresh_data(self):
        """Refresh data and reinitialize components"""
        self.data = self._load_data(self.data_path)
        self._initialize_llm()
        self._initialize_embeddings()
        self.vectorstore = self._create_vectorstore()
        self.memory = self._setup_memory()
        self.qa_chain = self._setup_qa_chain()

    def _initialize_llm(self):
        """Initialize the LLM"""
        self.llm = Ollama(
            model="mistral",
            base_url="http://127.0.0.1:11434",
            temperature=0.7
        )

    def _initialize_embeddings(self):
        """Initialize embeddings model"""
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )

    def _load_data(self, data_path: str) -> pd.DataFrame:
        """Load and preprocess the CSV data"""
        try:
            df = pd.read_csv(data_path, skipinitialspace=True)
            df.columns = df.columns.str.strip()
            df['Month'] = df['Month'].str.strip()
            df['Profit'] = df['Sales (INR)'] - df['Expenses (INR)']
            df['Profit_Margin'] = (df['Profit'] / df['Sales (INR)']) * 100
            return df
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return pd.DataFrame()

    def _create_vectorstore(self) -> Chroma:
        """Create and populate the vector store"""
        documents = []
        for idx, row in self.data.iterrows():
            content = (
                f"Financial Report for {row['Month']}\n"
                f"Sales: ₹{row['Sales (INR)']:,.2f}\n"
                f"Expenses: ₹{row['Expenses (INR)']:,.2f}\n"
                f"Profit: ₹{row['Profit']:,.2f}\n"
                f"Profit Margin: {row['Profit_Margin']:.1f}%\n"
                f"Customers: {row['Customers']}\n"
                f"Inventory Cost: ₹{row['Inventory Cost (INR)']:,.2f}\n"
                f"Marketing Spend: ₹{row['Marketing Spend (INR)']:,.2f}"
            )
            doc = Document(
                page_content=content,
                metadata={
                    'month': row['Month'],
                    'sales': row['Sales (INR)'],
                    'profit': row['Profit']
                }
            )
            documents.append(doc)
        
        return Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings
        )

    def _setup_memory(self) -> ConversationBufferMemory:
        """Setup conversation memory"""
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    def _setup_qa_chain(self) -> ConversationalRetrievalChain:
        """Setup the QA chain with custom prompts"""
        template = """You are an AI business analyst for SME/MSME businesses.
        Analyze the provided financial data and give clear insights.
        
        Format rules:
        - Use ₹ symbol for currency
        - Show calculations clearly
        - Round percentages to 1 decimal place
        
        Context: {context}
        Chat History: {chat_history}
        Question: {question}
        
        Analysis:"""

        PROMPT = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=template
        )

        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            verbose=True
        )

    def get_financial_metrics(self, period: str = None) -> Dict[str, float]:
        """Get financial metrics for a specific period"""
        if period:
            data = self.data[self.data['Month'].str.contains(period)]
        else:
            data = self.data
            
        return {
            'Total_Sales': data['Sales (INR)'].sum(),
            'Total_Expenses': data['Expenses (INR)'].sum(),
            'Total_Profit': data['Profit'].sum(),
            'Average_Profit_Margin': data['Profit_Margin'].mean(),
            'Average_Customers': data['Customers'].mean(),
            'Total_Inventory_Cost': data['Inventory Cost (INR)'].sum(),
            'Total_Marketing_Spend': data['Marketing Spend (INR)'].sum()
        }

    def ask_question(self, question: str) -> Dict[str, Any]:
        """Process a business question"""
        try:
            response = self.qa_chain({"question": question})
            return {
                'answer': response['answer'],
                'sources': response.get('source_documents', [])
            }
        except Exception as e:
            st.error(f"Error processing question: {str(e)}")
            return {
                'answer': "I apologize, but I encountered an error processing your question.",
                'sources': []
            }

    def get_trend_analysis(self) -> Dict[str, List[Any]]:
        """Get trend analysis for key metrics"""
        return {
            'months': self.data['Month'].tolist(),
            'sales': self.data['Sales (INR)'].tolist(),
            'expenses': self.data['Expenses (INR)'].tolist(),
            'profits': self.data['Profit'].tolist(),
            'customers': self.data['Customers'].tolist(),
            'profit_margins': self.data['Profit_Margin'].tolist()
        }