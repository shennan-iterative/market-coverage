import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import json

def safe_get(data, key, default='Unknown'):
    if isinstance(data, dict):
        return data.get(key, default)
    elif isinstance(data, str):
        try:
            return json.loads(data).get(key, default)
        except json.JSONDecodeError:
            st.warning(f"Unable to parse string as JSON: {data[:50]}...")
            return default
    else:
        st.warning(f"Unexpected data type: {type(data)}")
        return default

def summarize_deals_by_sector(companies_data):
    deals = []

    for company in companies_data:
        sector = safe_get(company, 'Industry')
        funding_rounds = safe_get(company, 'Fundraising History', {})
        
        if isinstance(funding_rounds, str):
            try:
                funding_rounds = json.loads(funding_rounds)
            except json.JSONDecodeError:
                st.warning(f"Unable to parse Fundraising History: {funding_rounds[:50]}...")
                continue

        for round_name, round_info in funding_rounds.items():
            if isinstance(round_info, dict) and 'amount' in round_info and round_name != 'founded':
                amount_str = round_info['amount']
                try:
                    amount_value = float(amount_str.split()[0])
                except ValueError:
                    st.warning(f"Invalid amount format: {amount_str}")
                    continue
                currency = amount_str.split()[-1]
                
                deals.append({
                    'sector': sector,
                    'amount': amount_value,
                    'currency': currency,
                    'country': safe_get(company, 'Country HQ')
                })

    if not deals:
        st.error("No valid deals data found")
        return None

    deals_df = pd.DataFrame(deals)
    sector_summary = deals_df.groupby('sector').agg(
        total_deals=('amount', 'count'),
        total_amount=('amount', 'sum')
    ).reset_index().sort_values('total_amount', ascending=False)

    return sector_summary

def summarize_market_coverage_by_country(companies_data, countries):
    coverage = {country: 0 for country in countries}

    for company in companies_data:
        country = safe_get(company, 'Country HQ')
        if country in coverage:
            coverage[country] += 1

    return coverage
