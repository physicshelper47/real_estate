import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Cost_benefits_buy_VS_rent import calculate_buy_vs_rent_with_opportunity_cost

def scan_1D(scan_range, base_params, param_name):
    heatmap_data = []
    for value in scan_range:
        test_params = base_params.copy()
        if param_name == "rent_increase_rate":
            test_params["home_appreciation_rate"] = value
        test_params[param_name] = value
        _, break_even_year = calculate_buy_vs_rent_with_opportunity_cost(**test_params)
        heatmap_data.append(break_even_year if break_even_year else 31)  # Use 31 for "never breaks even"
    return np.array(heatmap_data)

if __name__ == '__main__':
    # Base input parameters
    params = {
        "home_price": 369900,
        "down_payment_percent": 0.035,
        "mortgage_rate": 0.07,
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
    scan_range = np.arange(0.01, 0.08, 0.01)  # $300k to $750k
    param_name='mortgage_rate'
    base_params = params.copy()

    heatmap_data=scan_1D(scan_range, base_params, param_name)

    # Run analysis and plot
    plt.plot(scan_range, heatmap_data, marker='o')
    plt.title(f"Break-even Year vs {param_name.replace('_', ' ').title()}")
    plt.xlabel(param_name.replace('_', ' ').title())
    plt.ylabel("Break-even Year")
    plt.grid(True)
    plt.show()