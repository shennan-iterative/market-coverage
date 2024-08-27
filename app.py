
import streamlit as st
import pandas as pd
from insights import (
    plot_foundersAnalysis,
    plot_average_funding_per_round,
    plot_funding_over_time,
    plot_funding_by_location,
    plot_industry_distribution,
    plot_total_investors,
    summarize_deals_by_sector,
    summarize_market_coverage_by_country,
    plot_valuation_insights
)
import re
import matplotlib.pyplot as plt

@st.cache_data
def load_data(file):
    data = pd.read_json(file)
    data['Total Funding'] = data['Total Funding'].apply(lambda x: float(re.sub(r'[^\d.]', '', x)) if isinstance(x, str) else x)
    return data

def main():
    st.set_page_config(layout="wide", page_title="Company Insights Dashboard")
    st.title("Company Insights Dashboard")
    
    uploaded_file = st.file_uploader("Upload a JSON file", type=['json'])
    
    if uploaded_file is not None:
        try:
            companies_data = load_data(uploaded_file)
            
            st.sidebar.header("Filters")
            max_funding = int(companies_data['Total Funding'].max())
            min_funding = st.sidebar.slider("Minimum total funding (USD)", 0, max_funding, 0)
            filtered_data = companies_data[companies_data['Total Funding'] >= min_funding]
            
            tab1, tab2, tab3 = st.tabs(["Overview", "Funding Analysis", "Geographic Insights"])
            
            with tab1:
                display_overview(filtered_data)
            
            with tab2:
                display_funding_analysis(filtered_data)
            
            with tab3:
                display_geographic_insights(filtered_data)

        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            st.write("Error details:", e)
            import traceback
            st.write("Traceback:", traceback.format_exc())

def display_overview(data):
    st.header("Data Overview")
    st.dataframe(data)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Industry Distribution")
        plot_industry_distribution(data)
    
    with col2:
        st.subheader("Total Number of Unique Investors")
        plot_total_investors(data)

def display_funding_analysis(data):
    st.header("Funding Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Total Funding Over Time")
        plot_funding_over_time(data)
    
    with col2:
        st.subheader("Average Funding per Round")
        plot_average_funding_per_round(data)
    
    st.subheader("Funding vs Last Valuation")
    plot_valuation_insights(data)
    
    display_deals_by_sector(data)

def display_geographic_insights(data):
    st.header("Geographic Insights")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Funding by Geographic Location")
        plot_funding_by_location(data)
    
    with col2:
        st.subheader("Number of Companies Founded by Each Founder")
        plot_foundersAnalysis(data)
    
    display_market_coverage(data)

def display_deals_by_sector(data):
    deals_by_sector = summarize_deals_by_sector(data.to_dict('records'))
    if deals_by_sector is not None:
        st.subheader("Deals by Sector")
        col1, col2 = st.columns([3, 1])
        with col1:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(deals_by_sector['sector'], deals_by_sector['total_amount'])
            ax.set_xlabel('Sector')
            ax.set_ylabel('Total Amount')
            ax.set_title('Total Funding Amount by Sector')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
        
        with col2:
            st.dataframe(deals_by_sector)
            csv = deals_by_sector.to_csv(index=False)
            st.download_button(
                label="Download deals by sector as CSV",
                data=csv,
                file_name="deals_by_sector.csv",
                mime="text/csv",
            )

def display_market_coverage(data):
    st.subheader("Market Coverage by Country")
    countries_of_interest = list(set(data['Country HQ'].dropna()))
    selected_countries = st.multiselect(
        "Select countries for analysis",
        countries_of_interest,
        default=countries_of_interest
    )
    market_coverage = summarize_market_coverage_by_country(data.to_dict('records'), selected_countries)
    market_coverage_df = pd.DataFrame.from_dict(market_coverage, orient='index', columns=['Number of Companies']).reset_index()
    market_coverage_df.columns = ['Country', 'Number of Companies']
    market_coverage_df = market_coverage_df.sort_values('Number of Companies', ascending=False)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(market_coverage_df['Country'], market_coverage_df['Number of Companies'])
        ax.set_xlabel('Country')
        ax.set_ylabel('Number of Companies')
        ax.set_title('Market Coverage by Country')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    
    with col2:
        st.dataframe(market_coverage_df)
        csv = market_coverage_df.to_csv(index=False)
        st.download_button(
            label="Download market coverage as CSV",
            data=csv,
            file_name="market_coverage.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
