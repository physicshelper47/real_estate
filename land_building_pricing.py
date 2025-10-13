import math

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

def calculate_property_valuation(sqft, age, tier, land_size_acres, land_price_per_acre):
    tier = tier.lower()
    if tier not in HALF_LIFE_BY_TIER or tier not in PRICE_PER_SQFT_BY_TIER:
        raise ValueError("Invalid tier. Use one of: 'basic', 'mid', 'high'.")

    # Lookup values
    half_life = HALF_LIFE_BY_TIER[tier]
    price_per_sqft = PRICE_PER_SQFT_BY_TIER[tier]

    # Calculate initial and depreciated structure value
    structure_initial_value = sqft * price_per_sqft
    decay_factor = 0.5 ** (age / half_life)
    structure_current_value = structure_initial_value * decay_factor

    # Land valuation
    land_value = land_size_acres * land_price_per_acre

    # Total property value
    total_value = structure_current_value + land_value

    # Create detailed report
    report = f"""\
🏡 Property Valuation Report
----------------------------
📐 Structure:
  - Size: {sqft:,} sqft
  - Build Quality Tier: {tier.capitalize()}
  - Price per Sqft: ${price_per_sqft}
  - Initial Value: ${structure_initial_value:,.2f}
  - Age: {age} years
  - Half-life: {half_life} years
  - Depreciation Factor: {decay_factor:.4f}
  - Current Structure Value: ${structure_current_value:,.2f}

🌱 Land:
  - Size: {land_size_acres} acres
  - Price per Acre: ${land_price_per_acre:,.2f}
  - Land Value: ${land_value:,.2f}

💰 Total Estimated Property Value: ${total_value:,.2f}
"""

    # Return dictionary and report
    result = {
        'sqft': sqft,
        'age_years': age,
        'tier': tier,
        'price_per_sqft': price_per_sqft,
        'half_life': half_life,
        'structure_initial_value': structure_initial_value,
        'structure_current_value': structure_current_value,
        'depreciation_factor': decay_factor,
        'land_size_acres': land_size_acres,
        'land_price_per_acre': land_price_per_acre,
        'land_value': land_value,
        'total_property_value': total_value,
        'report': report
    }

    return result


if __name__ == '__main__':
    result = calculate_property_valuation(
        sqft=2400,
        age=5,
        tier='mid',
        land_size_acres=12.5,
        land_price_per_acre=6000
    )

    print(result['report'])
