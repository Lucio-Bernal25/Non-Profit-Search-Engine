import pytest

from app.non_profit import get_non_profits 

def test_get_non_profits():
    # Sample inputs (can be adjusted as needed)
    state = "FL"
    category = "4"
    parameters_list = ['totprgmrevnue', 'grsincfndrsng ']
    filter_param = 'totprgmrevnue'
    year = 2022 #no data for 2023


    sorted_orgs = get_non_profits(state, category, parameters_list, filter_param, year)
    assert isinstance(sorted_orgs, list)  # Ensure the result is a list
    print("Sorted orgs length:", len(sorted_orgs))
    assert len(sorted_orgs) > 0  # Check that the list is not empty