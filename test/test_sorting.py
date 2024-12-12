import pytest
from app.non_profit import get_non_profits 

# Simplified mock data with EINs, names, and revenue values
mocked_response = {
    "organizations": [
        {"ein": "123456789", "name": "Org 1"},
        {"ein": "987654321", "name": "Org 2"},
        {"ein": "456789123", "name": "Org 3"}
    ]
}

mocked_filing_data = [
    {"tax_prd_yr": 2022, "totprgmrevnue": 50000, "grsincfndrsng": 10000},
    {"tax_prd_yr": 2022, "totprgmrevnue": 70000, "grsincfndrsng": 20000},
    {"tax_prd_yr": 2022, "totprgmrevnue": 60000, "grsincfndrsng": 15000}
]

def sort_orgs_by_revenue(orgs, filings):
    """
    Sort the organizations by their total program revenue.
    """
    # Creating a dictionary to map EIN to revenue
    ein_to_revenue = {org['ein']: filing['totprgmrevnue'] for org, filing in zip(orgs, filings)}
    
    # Sort organizations by revenue
    return sorted(orgs, key=lambda org: ein_to_revenue[org['ein']], reverse=True)

# Test function to validate sorting
@pytest.mark.parametrize("state, category, expected_order", [
    ("FL", "4", ["987654321", "456789123", "123456789"])  # Expected order of EINs based on revenue!
])
def test_sorting(state, category, expected_order):
    # Get the list of organizations
    organizations = mocked_response['organizations']
    filings = mocked_filing_data

    # Sort the organizations using the revenue (mocked data)
    sorted_orgs = sort_orgs_by_revenue(organizations, filings)

    # Extract the EINs from the sorted organizations
    sorted_eins = [org['ein'] for org in sorted_orgs]
    
    # Assert that the sorted EINs match the expected order
    assert sorted_eins == expected_order, f"Expected {expected_order} but got {sorted_eins}"
