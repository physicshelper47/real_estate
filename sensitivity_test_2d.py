import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Cost_benefits import calculate_buy_vs_rent_with_opportunity_cost

def run_sensitivity_analysis(base_params, price_range, rate_range, key_names=["home_price", "mortgage_rate"]):
    heatmap_data = []

    for home_price in price_range:
        row = []
        for mortgage_rate in rate_range:
            test_params = base_params.copy()
            test_params[key_names[0]] = home_price
            test_params[key_names[1]] = mortgage_rate
            _, break_even_year = calculate_buy_vs_rent_with_opportunity_cost(**test_params)
            row.append(break_even_year if break_even_year else 31)  # Use 31 for "never breaks even"
        heatmap_data.append(row)

    return np.array(heatmap_data)

def plot_heatmap(heatmap_matrix, price_range, rate_range, key_names):
    plt.figure(figsize=(12, 8))

    if key_names[1] == "home_price":
        yticklabels=[f"${p//1000}k" for p in price_range]
    if key_names[0] == "home_price":
        xticklabels=[f"${p//1000}k" for p in rate_range]
    if key_names[1] in ["mortgage_rate", "down_payment_percent"]:
        yticklabels=[f"{r:.2%}" for r in price_range]
    if key_names[0] in ["mortgage_rate", "down_payment_percent"]:
        xticklabels=[f"{r:.2%}" for r in rate_range]
    sns.heatmap(
        heatmap_matrix,
        xticklabels=xticklabels,
        yticklabels=yticklabels,
        annot=True, fmt="d", cmap="coolwarm", cbar_kws={"label": "Break-even Year"},
    )
    plt.title(f"Sensitivity Analysis: Break-even Year by {key_names[0]} and {key_names[1]}")
    plt.xlabel(key_names[0])
    plt.ylabel(key_names[1])
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # Base input parameters
    params = {
        "home_price": 440000,
        "down_payment_percent": 0.05,
        "mortgage_rate": 0.06,
        "loan_term_years": 30,
        "property_tax_rate": 0.0058,
        "maintenance_rate": 0.01,
        "home_appreciation_rate": 0.03,
        "monthly_rent": 2300,
        "rent_increase_rate": 0.03,
        "household_income": 150000,
        "marginal_tax_rate": 0.24,
        "standard_deduction": 29200,
        "time_horizon_years": 30,
        "closing_cost_percent": 0.00,
        "selling_cost_percent": 0.06,
        "investment_return_rate": 0.1
    }

    # Test ranges
    #key_names = ["home_price", "mortgage_rate"]
    #key1_range = np.arange(300000, 751000, 50000)  # $300k to $750k
    #key2_range = np.arange(0.03, 0.081, 0.01)       # 3% to 8%

    key_names = ["mortgage_rate", "down_payment_percent"]
    key1_range = np.arange(0.00, 0.21, 0.01)  # $300k to $750k
    key2_range = np.arange(0.03, 1., 0.01)  # 3% to 8%

    # Run analysis and plot
    heatmap_matrix = run_sensitivity_analysis(params, key1_range, key2_range, key_names)
    plot_heatmap(heatmap_matrix, key1_range, key2_range, key_names)