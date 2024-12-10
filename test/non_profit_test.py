import pytest

from app.non_profit import get_non_profits 

def test_get_non_profits():
    # Sample inputs (can be adjusted as needed)
    state = "FL"
    category = "4"
    parameters_list = ['totprgmrevnue', 'grsincfndrsng ']
    filter_param = 'totprgmrevnue'
    year = 2023
    
    # Call the function you want to test
    sorted_orgs = get_non_profits(state, category, parameters_list, filter_param, year)

    # Perform assertions to check the behavior
    assert isinstance(sorted_orgs, list)  # Ensure the result is a list
    assert len(sorted_orgs) > 0  # Check that the list is not empty

    # Check the structure of the first organization in the list
    first_org = sorted_orgs[0]
    assert 'ein' in first_org  # Check if 'ein' exists in the first organization
    assert isinstance(first_org['ein'], str)  # Ensure 'ein' is a string
    
    # Check if the first organization has the expected filter parameter
    assert 'filter' in first_org  # Ensure 'filter' is in the first organization
    assert first_org['filter'] is not None  # Ensure the filter value is not None
