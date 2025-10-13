# Constants
HALF_LIFE_BY_TIER = {
    'basic': 15,
    'mid': 20,
    'high': 30,
}

PRICE_PER_SQFT_BY_TIER = {
    'basic': 175,
    'mid': 225,
    'high': 300,
}


def opportunity_cost_calc(rent_per_month, hourly_wage, build_duration_years, daily_management_hours):
    """
    Calculate the opportunity cost of building a home, including:
    - Rent paid during construction
    - Time spent managing the build, valued at hourly wage

    Args:
        rent_per_month (float): Monthly rent expense.
        hourly_wage (float): Your value per hour.
        build_duration_years (float): Duration of construction (in years).
        daily_management_hours (float): Daily hours spent on managing the project.

    Returns:
        float: Total opportunity cost in dollars.
    """
    total_rent_cost = rent_per_month * 12 * build_duration_years
    total_management_hours = build_duration_years * 365 * daily_management_hours
    time_value_cost = total_management_hours * hourly_wage

    return total_rent_cost + time_value_cost


def calculate_property_valuation(
    sqft,
    age,
    tier,
    land_size_acres,
    land_price_per_acre,
    land_prep_cost=0,
    opportunity_cost=0
):
    """
    Estimate property value based on build quality, structure depreciation,
    land value, land prep, and opportunity costs.

    Args:
        sqft (float): Structure size in square feet.
        age (float): Age of the structure in years.
        tier (str): Build quality tier ('basic', 'mid', 'high').
        land_size_acres (float): Land area in acres.
        land_price_per_acre (float): Cost per acre.
        land_prep_cost (float): Cost to prep the land.
        opportunity_cost (float): Calculated opportunity cost.

    Returns:
        dict: Detailed report and all calculated values.
    """
    tier = tier.lower()
    if tier not in HALF_LIFE_BY_TIER or tier not in PRICE_PER_SQFT_BY_TIER:
        raise ValueError("Invalid tier. Use one of: 'basic', 'mid', 'high'.")

    # Lookup constants
    half_life = HALF_LIFE_BY_TIER[tier]
    price_per_sqft = PRICE_PER_SQFT_BY_TIER[tier]

    # Structure valuation
    structure_initial_value = sqft * price_per_sqft
    depreciation_factor = 0.5 ** (age / half_life)
    structure_current_value = structure_initial_value * depreciation_factor

    # Land valuation
    land_value = land_size_acres * land_price_per_acre

    # Final valuations
    total_market_value = structure_current_value + land_value
    total_cost_basis = structure_initial_value + land_value + land_prep_cost + opportunity_cost
    value_margin = total_market_value - total_cost_basis

    # Text report
    report = f"""\
🏡 Property Valuation Report
----------------------------
📐 Structure:
  - Size: {sqft:,} sqft
  - Tier: {tier.capitalize()}
  - Price per Sqft: ${price_per_sqft}
  - Initial Value: ${structure_initial_value:,.2f}
  - Age: {age} years
  - Half-life: {half_life} years
  - Depreciation Factor: {depreciation_factor:.4f}
  - Current Value: ${structure_current_value:,.2f}

🌱 Land:
  - Size: {land_size_acres} acres
  - Price per Acre: ${land_price_per_acre:,.2f}
  - Raw Land Value: ${land_value:,.2f}
  - Land Prep Cost: ${land_prep_cost:,.2f}

💸 Additional Costs:
  - Opportunity Cost: ${opportunity_cost:,.2f}

--------------------------------------------
💰 Total Estimated Market Value: ${total_market_value:,.2f}
🧾 Total Build Cost Basis: ${total_cost_basis:,.2f}
📈 Value Margin: ${value_margin:,.2f}
"""

    return {
        'sqft': sqft,
        'age_years': age,
        'tier': tier,
        'price_per_sqft': price_per_sqft,
        'half_life': half_life,
        'structure_initial_value': structure_initial_value,
        'structure_current_value': structure_current_value,
        'depreciation_factor': depreciation_factor,
        'land_size_acres': land_size_acres,
        'land_price_per_acre': land_price_per_acre,
        'land_value': land_value,
        'land_prep_cost': land_prep_cost,
        'opportunity_cost': opportunity_cost,
        'total_property_value': total_market_value,
        'total_cost_basis': total_cost_basis,
        'value_margin': value_margin,
        'report': report
    }


# Sample usage
if __name__ == '__main__':
    # Example inputs
    rent_per_month = 2500
    hourly_wage = 50
    build_duration_years = 2
    daily_management_hours = 1

    # Calculate opportunity cost
    opp_cost = opportunity_cost_calc(
        rent_per_month=rent_per_month,
        hourly_wage=hourly_wage,
        build_duration_years=build_duration_years,
        daily_management_hours=daily_management_hours
    )

    # Final valuation
    result = calculate_property_valuation(
        sqft=2500,
        age=5,  #in years
        tier='mid', #basic, mid, high
        land_size_acres=12.5,
        land_price_per_acre=6000,
        land_prep_cost=50000,
        opportunity_cost=opp_cost
    )

    # Print report
    print(result['report'])
