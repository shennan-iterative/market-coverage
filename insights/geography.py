import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_funding_by_location(companies_data):
    # Convert the list of company data into a DataFrame
    df = pd.DataFrame(companies_data)

    # Calculate Total Funding
    df['Total Funding'] = df['Total Funding'].apply(
        lambda x: float(x.split()[0]) if isinstance(x, str) else x
    )

    # Group by 'Country HQ' and sum the total funding
    funding_by_country = df.groupby('Country HQ')['Total Funding'].sum().sort_values(ascending=False)

    # Allow user to select the number of top countries to display
    num_countries = st.slider("Select number of top countries to display", 
                              min_value=3, max_value=len(funding_by_country), value=10)

    # Get the top N countries
    top_countries = funding_by_country.head(num_countries)

    # Plotting
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    # Pie chart
    ax1.pie(top_countries, labels=top_countries.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title(f"Funding Distribution by Top {num_countries} Countries")

    # Bar chart
    bars = ax2.bar(top_countries.index, top_countries.values)
    ax2.set_title(f"Total Funding by Top {num_countries} Countries")
    ax2.set_xlabel("Country")
    ax2.set_ylabel("Total Funding (USD)")
    ax2.tick_params(axis='x', rotation=45)

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                 f'${height:,.0f}',
                 ha='center', va='bottom', rotation=0)

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Display the data as a table
    st.write("Funding by Country Data:")
    st.dataframe(funding_by_country)

    # Add a download button for the data
    csv = funding_by_country.to_csv().encode('utf-8')
    st.download_button(
        label="Download funding by country data as CSV",
        data=csv,
        file_name="funding_by_country.csv",
        mime="text/csv",
    )

    # Display additional statistics
    st.write("Funding Statistics:")
    st.write(f"Total number of countries: {len(funding_by_country)}")
    st.write(f"Country with highest funding: {funding_by_country.index[0]} (${funding_by_country.iloc[0]:,.0f})")
    st.write(f"Country with lowest funding: {funding_by_country.index[-1]} (${funding_by_country.iloc[-1]:,.0f})")
    st.write(f"Average funding per country: ${funding_by_country.mean():,.0f}")

# Example usage:
# plot_funding_by_location(companies_data)
