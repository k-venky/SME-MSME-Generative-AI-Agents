import streamlit as st
import plotly.graph_objects as go
from business_insights_agent_new import BusinessInsightsAgent

# Set page configuration
st.set_page_config(
    page_title="SME Business Insights",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = BusinessInsightsAgent('data/sample_data.csv')

def create_metric_card(label, value, prefix="₹"):
    """Create a styled metric card"""
    if isinstance(value, (int, float)):
        if prefix == "₹":
            formatted_value = f"{prefix}{value:,.2f}"
        else:
            formatted_value = f"{value:,.1f}{prefix}"
    else:
        formatted_value = str(value)
        
    st.metric(label=label, value=formatted_value)

def plot_trend(data, title):
    """Create a trend line plot"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['months'],
        y=data['sales'],
        name='Sales',
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatter(
        x=data['months'],
        y=data['expenses'],
        name='Expenses',
        line=dict(color='red')
    ))
    
    fig.add_trace(go.Scatter(
        x=data['months'],
        y=data['profits'],
        name='Profit',
        line=dict(color='green')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Month",
        yaxis_title="Amount (₹)",
        hovermode='x unified'
    )
    
    return fig

def main():
    st.title("📊 SME Business Insights Dashboard")
    
    # Sidebar for period selection
    st.sidebar.title("Analysis Controls")
    period = st.sidebar.selectbox(
        "Select Period",
        ["All Time", "2023", "2024"]
    )
    
    selected_period = None if period == "All Time" else period
    
    # Get metrics
    metrics = st.session_state.agent.get_financial_metrics(selected_period)
    
    # Display key metrics
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card("Total Sales", metrics['Total_Sales'])
    with col2:
        create_metric_card("Total Profit", metrics['Total_Profit'])
    with col3:
        create_metric_card("Profit Margin", metrics['Average_Profit_Margin'], "%")
    with col4:
        create_metric_card("Avg. Customers", int(metrics['Average_Customers']), "")
    
    # Get and display trends
    st.subheader("Financial Trends")
    trends = st.session_state.agent.get_trend_analysis()
    st.plotly_chart(plot_trend(trends, "Sales, Expenses & Profit Trends"), use_container_width=True)
    
    # Business Insights Chat
    st.subheader("💬 Business Insights Chat")
    question = st.text_input(
        "Ask a question about your business data:",
        placeholder="E.g., What was the highest profit month?"
    )
    
    if question:
        with st.spinner("Analyzing..."):
            response = st.session_state.agent.ask_question(question)
            st.write("🤖 Analysis:", response['answer'])
            
            if response['sources']:
                with st.expander("View Source Data"):
                    for source in response['sources']:
                        st.text(source.page_content)

if __name__ == "__main__":
    main()