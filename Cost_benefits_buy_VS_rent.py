import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calculate_monthly_mortgage_payment(loan_amount, annual_rate, loan_term_years):
    monthly_rate = annual_rate / 12
    n_payments = loan_term_years * 12
    if monthly_rate == 0:
        return loan_amount / n_payments
    return loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / \
           ((1 + monthly_rate) ** n_payments - 1)


def calculate_buy_vs_rent_with_opportunity_cost(
    home_price, down_payment_percent, mortgage_rate, loan_term_years,
    property_tax_rate, maintenance_rate, home_appreciation_rate,
    monthly_rent, rent_increase_rate,
    household_income, marginal_tax_rate, standard_deduction,
    time_horizon_years,
    closing_cost_percent=0.03, selling_cost_percent=0.06,
    investment_return_rate=0.08
):
    down_payment = home_price * down_payment_percent
    loan_amount = home_price - down_payment
    monthly_payment = calculate_monthly_mortgage_payment(loan_amount, mortgage_rate, loan_term_years)
    closing_cost = home_price * closing_cost_percent

    home_value = home_price
    rent = monthly_rent
    remaining_balance = loan_amount

    cumulative_buy_cost = closing_cost
    cumulative_rent_cost = 0
    equity_built = 0
    investable_funds = down_payment + closing_cost
    investment_balance = investable_funds
    break_even_year = None

    summary = []

    for year in range(1, time_horizon_years + 1):
        annual_interest = 0
        annual_principal = 0

        for _ in range(12):
            interest = remaining_balance * (mortgage_rate / 12)
            principal = monthly_payment - interest
            annual_interest += interest
            annual_principal += principal
            remaining_balance -= principal

        equity_built += annual_principal
        maintenance = home_value * maintenance_rate
        property_tax = home_value * property_tax_rate
        itemized_deductions = annual_interest + min(property_tax, 10000)
        deductible_amount = max(0, itemized_deductions - standard_deduction)
        tax_savings = deductible_amount * marginal_tax_rate

        annual_buy_cost = 12 * monthly_payment + maintenance + property_tax - tax_savings
        cumulative_buy_cost += annual_buy_cost

        # Home appreciation and selling cost
        appreciated_value = home_value * ((1 + home_appreciation_rate) ** year)
        selling_cost = appreciated_value * selling_cost_percent

        # Net cost = cumulative cost - equity - home value gain + selling cost
        net_cost_of_buying = cumulative_buy_cost - equity_built - (appreciated_value - home_price) + selling_cost

        # Rent + investing difference
        annual_rent = 12 * rent
        cumulative_rent_cost += annual_rent
        rent *= (1 + rent_increase_rate)

        # If renting, invest the difference (if any) between owning and renting
        savings = max(0, annual_buy_cost - annual_rent)
        investment_balance = (investment_balance + savings) * (1 + investment_return_rate)

        # Break-even: buy net cost < rent + investment gains
        if break_even_year is None and net_cost_of_buying < (cumulative_rent_cost - investment_balance):
            break_even_year = year

        summary.append({
            "Year": year,
            "Annual Interest": annual_interest,
            "Annual Principal": annual_principal,
            "Cumulative Buy Cost": cumulative_buy_cost,
            "Equity Built": equity_built,
            "Appreciated Home Value": appreciated_value,
            "Selling Cost": selling_cost,
            "Net Cost of Buying": net_cost_of_buying,
            "Annual Rent": annual_rent,
            "Cumulative Rent Cost": cumulative_rent_cost,
            "Investment Value": investment_balance,
            "Tax Savings": tax_savings
        })

    return pd.DataFrame(summary), break_even_year


def plot_opportunity_comparison(df, break_even_year):
    plt.figure(figsize=(12, 7))
    plt.plot(df["Year"], df["Cumulative Rent Cost"]-df["Investment Value"], label="Opportunity adjusted rent", linewidth=2)
    plt.plot(df["Year"], df["Net Cost of Buying"], label="Net Cost of Buying", linewidth=2)
    plt.plot(df["Year"], df["Equity Built"], ':', label="Equity Built", alpha=0.8)

    if break_even_year:
        plt.axvline(x=break_even_year, color='red', linestyle='--', label=f'Break-Even Year: {break_even_year}')

    plt.title("Buy vs Rent with Opportunity Cost of Investing")
    plt.xlabel("Year")
    plt.ylabel("Dollars ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    # === INPUT PARAMETERS ===
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
        "investment_return_rate": 0.08
    }

    # === RUN ANALYSIS ===
    df, break_even_year = calculate_buy_vs_rent_with_opportunity_cost(**params)
    df.to_csv('tmp.csv')
    # === DISPLAY RESULTS ===
    pd.set_option('display.float_format', '${:,.2f}'.format)
    print(df[["Year", "Net Cost of Buying", "Cumulative Rent Cost", "Investment Value", "Equity Built"]])
    print(f"\n📌 Break-even year (with opportunity cost): {break_even_year if break_even_year else 'Never within time horizon'}")

    # === PLOT ===
    plot_opportunity_comparison(df, break_even_year)
