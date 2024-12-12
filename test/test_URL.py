import pytest
from app.non_profit import build_url

def test_build_url():
    # Test the function with only state parameter
    state = "FL"
    expected_url = "https://projects.propublica.org/nonprofits/api/v2/search.json?state%5Bid%5D=FL"
    assert build_url(state=state) == expected_url

    # Test the function with both state and category parameters
    category = "4"
    expected_url = "https://projects.propublica.org/nonprofits/api/v2/search.json?state%5Bid%5D=FL&ntee%5Bid%5D=4"
    assert build_url(state=state, category=category) == expected_url

    # Test the function with no parameters (default)
    expected_url = "https://projects.propublica.org/nonprofits/api/v2/search.json?"
    assert build_url() == expected_url
