import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def convert_currency(amount, currency):
    # Example currency conversion rates to USD; you might want to use a library or API for real conversion rates.
    conversion_rates = {
        'USD': 1,
        'EUR': 1.1,  # Example rate
        'SGD': 0.75,  # Example rate
        # Add more currencies as needed
    }
    return amount * conversion_rates.get(currency, 1)

def summarize_deals_by_sector(companies_data):
    deals = []
    
    for company in companies_data:
        sectors = company.get('sectorList', [])
        funding_rounds = company['fundingInfo']['fundingRoundList']
        
        for sector in sectors:
            for round_info in funding_rounds:
                if 'amount' in round_info:
                    amount_usd = convert_currency(round_info['amount']['amount'], round_info['amount']['currency'])
                    deals.append({
                        'sector': sector[0]['name'],  # Assuming sector is structured this way
                        'amount': amount_usd,
                        'country': company['location']['country']
                    })
    
    deals_df = pd.DataFrame(deals)
    
    # Group by sector and sum the amounts
    sector_summary = deals_df.groupby('sector').agg(
        total_deals=('amount', 'count'),
        total_amount=('amount', 'sum')
    ).reset_index()

    return sector_summary

def summarize_market_coverage_by_country(companies_data, countries):
    coverage = {country: 0 for country in countries}

    for company in companies_data:
        country = company['location']['country']
        if country in coverage:
            coverage[country] += 1

    return coverage

def plot_deals_by_sector(sector_summary):
    plt.figure(figsize=(12, 6))
    sns.barplot(data=sector_summary, x='sector', y='total_amount')
    plt.title("Total Deals by Sector")
    plt.xlabel("Sector")
    plt.ylabel("Total Amount in USD")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_market_coverage(market_coverage):
    countries = list(market_coverage.keys())
    counts = list(market_coverage.values())

    plt.figure(figsize=(12, 6))
    sns.barplot(x=countries, y=counts)
    plt.title("Market Coverage by Country")
    plt.xlabel("Countries")
    plt.ylabel("Number of Companies")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
