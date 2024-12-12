import json
import requests
from operator import itemgetter

#building URL
def build_url(state="", category=""):
    base_url = "https://projects.propublica.org/nonprofits/api/v2/search.json"
    params = []

    # Add state parameter
    if state:
        params.append(f"state%5Bid%5D={state}")

    # Add category parameter
    if category:
        params.append(f"ntee%5Bid%5D={category}")

    # Join all parameters with '&'
    query_string = "&".join(params)

    # Create final URL
    final_url = f"{base_url}?{query_string}"
    return final_url

# Organization-specific accessing of data from API. Will add parameters from list, and a filter parameter that uses filter_param for the specified year.
def org_data_access(ein, parameters_list, year, filter_param):
    organization_url = f"https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json"
    # org_search refers to the /organizations/:ein.json Result
    org_search = requests.get(organization_url).json()
    # filings refer to the filing object. It is a list of years of filings each with a filing object datum.
    filings = org_search['filings_with_data']

    org_dict = {}


    # Adding necessary filter parameter to org_dict for specfic year. Can be accessed with ['filter']
    add_filter_param(org_dict, filings, int(year), filter_param)

    # Adding basic necessary parameters to org_dict object which includes: ein, organiation object, year, formtype.
    org_dict['ein'] = ein
    org_dict['organization'] = org_search['organization']
    try:    
        org_dict['start_year'] = int(filings[-1]['tax_prd_yr'])
        org_dict['last_year'] = int(filings[0]['tax_prd_yr'])
    except IndexError:
        org_dict['start_year'] = None
        org_dict['last_year'] = None
    org_dict['filings'] = []

    #adding a filings list with every year's filings with only the necessary parameters (the parameters from the pameters_list)
    for filing in filings:
        filing_dict = {}
        try:
            year_filing = filing['tax_prd_yr']
        except KeyError:
            year_filing=None
            
        filing_dict['tax_prd_year'] = year_filing
        # Adding parameters specified in list
        for parameter in parameters_list:
            try:
                filing_dict[parameter] = filing[parameter]
            except KeyError:
                filing_dict[parameter] = 0
        org_dict['filings'].append(filing_dict)
    return org_dict

#Support function for org_data_access that gets value that will be used to organize organizations from best to worst.
def add_filter_param(org_dict, filings, year, filter_param):
    #locating if filing of specified year exists
    org_dict['filter'] = None
    try:
        if len(filings)==0:
            org_dict['filter'] = None
        elif (int(filings[-1]['tax_prd_yr'])<=year) and (int(filings[0]['tax_prd_yr'])>=year):
            #iterating through different years to find correct one and add it with the filter key
            for filing in filings:
                if int(filing['tax_prd_yr'])==year:
                    org_dict['filter'] = filing[filter_param]
    except IndexError:
        org_dict['filter'] = None

def get_non_profits(state="", category="", parameters_list=['totprgmrevnue', 'grsincfndrsng '], filter_param = 'totprgmrevnue', year = 2022):
    # URL
    url = build_url(state, category)
    print(url)

    #Getting file from API with the Non-profits that fit parameters and adding all eins to list. List is called list_ein.
    list_ein = []
    initial_search = requests.get(url).json()
    for item in initial_search['organizations']:
        list_ein.append({'ein':item['ein'],'info':item})
    
    #From list of appropiate non-profits identified by eins, access the data of each one, and get the required parameters
    sorted_orgs = []
    for item in list_ein:
        org = org_data_access(item['ein'], parameters_list, year, filter_param)
        #check if filter param is valid for year (Won't add data that doesn't have a value in the year we are filtering of)
        if not(org['filter'] is None):
            org['filter'] = int(org['filter'])
            sorted_orgs.append(org)

    #sort the data pased on the desired parameter
    sorted_orgs = sorted(sorted_orgs, key=itemgetter('filter'), reverse=True)
    return sorted_orgs

#Get financial data for a specifc non-profit identified by ein.
def fetch_financial_data(ein):
    BASE_URL = "https://projects.propublica.org/nonprofits/api/v2/organizations"
    response = requests.get(f"{BASE_URL}/{ein}.json")
    data = response.json()

    filings = data.get('filings_with_data', [])[:10]
    if not filings:
        print(f"No financial data found for EIN: {ein}")
        return []

    graph_data = []

    for filing in filings:
        try:
            year = int(filing.get('tax_prd_yr', 0))
            revenues = float(filing.get('totrevenue', 0) or 0)
            expenses = float(filing.get('totfuncexpns', 0) or 0)
            assets = float(filing.get('totassetsend', 0) or 0)
            url = filing.get('pdf_url', '')

            graph_data.append({
                'Year': year,
                'Total Revenue': revenues,
                'Total Expenses': expenses,
                'Total Assets': assets,
                'URL': url
            })
        except (ValueError, TypeError) as e:
            print(f"Error processing filing: {e}")
            continue

    return graph_data

#Get basic data for a specifc non-profit identified by ein.
def fetch_org_info(ein):
    BASE_URL = "https://projects.propublica.org/nonprofits/api/v2/organizations"
    
    response = requests.get(f"{BASE_URL}/{ein}.json")
    data = response.json()
    
    return data['organization']
    
    
# Description of Data structure sorted_orgs:
    # A list of org objects organized based on a specfic value on a specific year.
    # Each org object is a dictionary that includes the base parameters ein, the organization object ['organization'], start_year, last year, formtype, and the filings list object ['filings'].
    # The organization object is a dictionary that includes details of the organization such as name, state...
    # The filings list object is a list of with each filings with each year containing: the specific year ['tax_prd_yr'] and the specified parameters given in parameters_list.

categorynames = {
    "":"",
    "1": "Arts, Culture & Humanities",
    "2": "Education",
    "3": "Environment and Animals",
    "4": "Health",
    "5": "Human Services",
    "6": "International, Foreign Affairs",
    "7": "Public, Societal Benefit",
    "8": "Religion Related",
    "9": "Mutual/Membership Benefit",
    "10": "Unknown, Unclassified"
}
filternames = {
    "totrevenue": "Total Revenue",
    "totprgmrevnue": "Total Program Revenue",
    "grsincfndrsng": "Gross Fundraising",
    "gftgrntsrcvd170": "Gifts, grants, membership fees received",
    "compnsatncurrofcr": "Compensation of current officers, directors, etc."
}

#Test output
if __name__ == "__main__":
    ### CONTROL SECTION ###

    # the state will be represented by the two-letter U.S. Postal Service abbreviation
    state = "FL"

    # the industry/category the nonprofit operates in will be represented by a numerical value. Ex: Arts, Culture & Humanities will have a value of 1
    category = "4"

    # parameters (filings) that will be included in the output data structure
    parameters_list = ['totprgmrevnue', 'grsincfndrsng ', 'totrevenue', 'gftgrntsrcvd170' , 'compnsatncurrofcr', 'pdf_url']

    #parameter that will organize the order of the data structure
    filter_param = 'totprgmrevnue'

    #year used for filtering
    year = 2022
    
    """
    sorted_orgs = get_non_profits(state, category, parameters_list, filter_param, year)
    for item in sorted_orgs:
        print('\n_______________________________________')
        print("EIN: ", item['ein'])
        print("NAME: ", item['organization']['name'])
        print("FIRST YEAR OF FILING: ", item['start_year'])
        print("LAST YEAR OF FILING: ", item['last_year'])
        print("FILTER PARAMETER VALUE: ", "${:,.2f}".format(item['filter']))
        print('_______________________________________\n')
        
    """
        