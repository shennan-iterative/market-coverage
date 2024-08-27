import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_industry_distribution(companies_data):
    df = pd.DataFrame(companies_data)
    industry_count = df['Industry'].value_counts()

    # Allow user to select the number of top industries to display
    num_industries = st.slider("Select number of top industries to display", 
                               min_value=5, max_value=len(industry_count), value=10)

    # Get the top N industries
    top_industries = industry_count.nlargest(num_industries)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = top_industries.plot(kind='bar', ax=ax)
    plt.title(f"Top {num_industries} Industries by Number of Companies")
    plt.xlabel("Industry")
    plt.ylabel("Number of Companies")
    plt.xticks(rotation=45, ha='right')

    # Add value labels on top of each bar
    for i, v in enumerate(top_industries):
        ax.text(i, v, str(v), ha='center', va='bottom')

    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Display the data as a table
    st.write("Industry Distribution Data:")
    st.dataframe(industry_count)

    # Add a download button for the data
    csv = industry_count.to_csv().encode('utf-8')
    st.download_button(
        label="Download industry distribution as CSV",
        data=csv,
        file_name="industry_distribution.csv",
        mime="text/csv",
    )

    # Display additional statistics
    st.write("Industry Statistics:")
    st.write(f"Total number of industries: {len(industry_count)}")
    st.write(f"Most common industry: {industry_count.index[0]} ({industry_count.iloc[0]} companies)")
    st.write(f"Least common industry: {industry_count.index[-1]} ({industry_count.iloc[-1]} companies)")


