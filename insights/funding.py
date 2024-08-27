
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_funding_over_time(companies_data):
    # Convert the list of company data into a DataFrame
    df = pd.DataFrame(companies_data)
    
    # Parse the 'Fundraising History' and calculate Total Funding
    df['Total Funding'] = df['Fundraising History'].apply(
        lambda x: sum([
            int(float(round['amount'].split()[0])) 
            for round_name, round in x.items() 
            if isinstance(round, dict) and 'amount' in round and round_name != 'founded'
        ])
    )

    # Group by 'Founded' year and sum the total funding
    funding_trend = df.groupby('Founded')[['Total Funding']].sum()

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    funding_trend.plot(kind='bar', ax=ax)
    plt.title("Total Funding Over Time")
    plt.xlabel("Year Founded")
    plt.ylabel("Total Funding in USD")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Display the data as a table
    st.write("Funding Trend Data:")
    st.dataframe(funding_trend)


def plot_average_funding_per_round(companies_data):
    # Convert the list of company data into a DataFrame
    df = pd.DataFrame(companies_data)

    # Compute average funding per round
    funding_rounds = []
    for history in df['Fundraising History']:
        for round_name, round_data in history.items():
            if isinstance(round_data, dict) and 'amount' in round_data and round_name != 'founded':
                funding_rounds.append({
                    'round': round_name,
                    'amount': float(round_data['amount'].split()[0])
                })
    
    funding_df = pd.DataFrame(funding_rounds)
    funding_averages = funding_df.groupby('round')['amount'].agg(['mean', 'count'])
    funding_averages = funding_averages.sort_values('mean', ascending=False)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = funding_averages['mean'].plot(kind='bar', ax=ax)
    plt.title("Average Funding per Round")
    plt.xlabel("Funding Round")
    plt.ylabel("Average Amount in USD")
    plt.xticks(rotation=45)

    # Add value labels on top of each bar
    for i, v in enumerate(funding_averages['mean']):
        ax.text(i, v, f'${v:,.0f}\n(n={funding_averages["count"][i]})', 
                ha='center', va='bottom')

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Display the data as a table
    st.write("Average Funding per Round Data:")
    st.dataframe(funding_averages)

    # Add a download button for the data
    csv = funding_averages.to_csv().encode('utf-8')
    st.download_button(
        label="Download funding averages as CSV",
        data=csv,
        file_name="funding_averages.csv",
        mime="text/csv",
    )

# Example usage:
# plot_funding_over_time(companies_data)
# plot_average_funding_per_round(companies_data)
