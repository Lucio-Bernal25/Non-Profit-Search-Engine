
from flask import Blueprint, request, render_template, redirect, flash
from app.non_profit import get_non_profits, categorynames, filternames, states, fetch_financial_data, fetch_org_info

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
@home_routes.route("/home")
def index():
    print("HOME...")
    #return "Welcome Home"
    return render_template("home.html")

@home_routes.route("/about")
def about():
    print("ABOUT...")
    #return "About Me"
    return render_template("about.html")

#Model after stocks dashboard route
@home_routes.route("/dashboard", methods= ["POST"])
def dashboard():
    print("Dashboard...")
    
    request_data = dict(request.form)
    
    #What is request_data? (GET vs POST?)
    print("REQUEST DATA:", request_data)
    state = request_data.get("state") or "" # get specified state or use null
    
    category = request_data.get("category") or "" 
    
    filter_param = request_data.get("filter_param") or "totprgmrevnue"
    
    year = request_data.get("year") or "2020"
    try:
        parameters_list = ['totprgmrevnue', 'grsincfndrsng ', 'pdf_url']
        
        if not state in states:
            state=3/0 #Had to get an error :/
        
        sorted_orgs = get_non_profits(state, category, parameters_list, filter_param, year)
        flash("Fetched Real Non-Profit Data!", "success") 
        return render_template("dashboard.html",
            state=state,
            category = category,
            filter_param= filter_param,
            year= year,
            sorted_orgs = sorted_orgs,
            filter_param_name = filternames[filter_param],
            category_name = categorynames[category]
        ) 
    except Exception as err:
        print('OOPS', err)
        flash("Data Error. Please check your inputs and try again!", "danger")
        return redirect("/home")
    
    

@home_routes.route("/organization", methods=["GET"])
def stocks_dashboard():
    print("ORGANIZATION DASHBOARD...")

    request_data = dict(request.args)

    ein = request_data.get("ein")

    try:


        flash("Fetched information for Organization succesfully!", "success")
        return render_template("organization.html",
            ein=ein,
            organization_financials=fetch_financial_data(ein),
            org_info=fetch_org_info(ein)
        )
    except Exception as err:
        print('OOPS', err)


        flash("Data Error. Not Valid EIN. Please try again!", "danger")
        return redirect("/dashboard")
        