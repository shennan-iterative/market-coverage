import pandas as pd
import matplotlib.pyplot as plt

def plot_valuation_insights(companies_data):
    df = pd.DataFrame(companies_data)
    df['Last Valuation'] = df['Last Valuation'].apply(lambda x: int(x.split()[0]) if x != "N/A" else None)
    
    plt.figure(figsize=(10, 6))
    df.plot.scatter(x='Total Funding', y='Last Valuation')
    plt.title("Funding vs Last Valuation")
    plt.xlabel("Total Funding in USD")
    plt.ylabel("Last Valuation in USD")
    plt.tight_layout()
    plt.show()
