import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_total_investors(companies_data):
    # Convert the list of company data into a DataFrame
    df = pd.DataFrame(companies_data)

    # Calculate total unique investors for each company
    def count_unique_investors(fundraising_history):
        unique_investors = set()
        for round_info in fundraising_history.values():
            if isinstance(round_info, dict) and 'by' in round_info:
                investors = round_info['by'].split(',')
                unique_investors.update(inv.strip() for inv in investors)
        return len(unique_investors)

    total_investors = df['Fundraising History'].apply(count_unique_investors)

    # Create a new DataFrame with company names and investor counts
    investor_df = pd.DataFrame({
        'Company': df['Company'],
        'Total Unique Investors': total_investors
    })

    # Sort by number of investors in descending order
    investor_df = investor_df.sort_values('Total Unique Investors', ascending=False)

    # Allow user to select the number of top companies to display
    num_companies = st.slider("Select number of top companies to display", 
                              min_value=5, max_value=len(investor_df), value=20)

    # Get the top N companies
    top_companies = investor_df.head(num_companies)

    # Plotting
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.bar(top_companies['Company'], top_companies['Total Unique Investors'])
    plt.title(f"Top {num_companies} Companies by Number of Unique Investors")
    plt.xlabel("Company")
    plt.ylabel("Total Unique Investors")
    plt.xticks(rotation=90)

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}',
                ha='center', va='bottom')

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Display the data as a table
    st.write("Investor Count Data:")
    st.dataframe(investor_df)

    # Add a download button for the data
    csv = investor_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download investor count data as CSV",
        data=csv,
        file_name="investor_count_data.csv",
        mime="text/csv",
    )

    # Display additional statistics
    st.write("Investor Statistics:")
    st.write(f"Total number of companies: {len(investor_df)}")
    st.write(f"Company with most investors: {investor_df.iloc[0]['Company']} ({investor_df.iloc[0]['Total Unique Investors']} investors)")
    st.write(f"Company with least investors: {investor_df.iloc[-1]['Company']} ({investor_df.iloc[-1]['Total Unique Investors']} investors)")
    st.write(f"Average number of investors per company: {investor_df['Total Unique Investors'].mean():.2f}")

# Example usage:
# plot_total_investors(companies_data)
