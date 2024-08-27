import pandas as pd
import streamlit as st
import plotly.express as px

def plot_foundersAnalysis(companies_data):
    st.header("Founder Analysis")
    
    df = pd.DataFrame(companies_data)
    
    # Extract founder names, handling potential None values
    founder_names = df['Founder'].apply(lambda x: x['name'] if isinstance(x, dict) and 'name' in x else 'Unknown')
    
    # Count the occurrences of each founder name
    founder_count = founder_names.value_counts().reset_index()
    founder_count.columns = ['Founder', 'Number of Companies']

    # Create an interactive bar chart using Plotly
    fig = px.bar(founder_count, x='Founder', y='Number of Companies', 
                 title='Number of Companies Founded by Each Founder',
                 labels={'Founder': 'Founder Name', 'Number of Companies': 'Number of Companies Founded'},
                 color='Number of Companies', color_continuous_scale='Viridis')
    fig.update_layout(xaxis_tickangle=-45, height=600)
    st.plotly_chart(fig, use_container_width=True)

    # Display additional founder information
    st.subheader("Founder Details")
    
    # Create a selectbox to choose a founder
    founder_list = [founder['name'] for founder in df['Founder'] if isinstance(founder, dict) and 'name' in founder]
    selected_founder = st.selectbox("Select a founder to view details:", founder_list)

    # Display information for the selected founder
    for _, company in df.iterrows():
        founder = company['Founder']
        if isinstance(founder, dict) and 'name' in founder and founder['name'] == selected_founder:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"### {founder['name']}")
                st.write(f"**Company:** {company['Company']}")
                st.write(f"**Designation:** {founder.get('designation', 'N/A')}")
                st.write(f"**Email:** {founder.get('email', 'N/A')}")
            with col2:
                st.markdown("#### Short Bio")
                st.write(founder.get('shortBio', 'N/A'))
                if 'linkedin' in founder:
                    st.markdown(f"[LinkedIn Profile]({founder['linkedin']})")
            st.markdown("---")

    # Add a download button for founder data
    founder_df = pd.DataFrame([f for f in df['Founder'] if isinstance(f, dict)])
    csv = founder_df.to_csv(index=False)
    st.download_button(
        label="Download Founder Data as CSV",
        data=csv,
        file_name="founder_data.csv",
        mime="text/csv",
    )
