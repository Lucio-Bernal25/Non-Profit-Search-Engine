
from flask import Blueprint, request, render_template, redirect, flash

from app.non_profit import get_non_profits

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
@home_routes.route("/dashboard")
def about():
    print("Dashboard...")
    
    #What is request_data? (GET vs POST?)
    print("REQUEST DATA:", request_data)

    state = request_data.get("state") or "" # get specified state or use null
    
    category = request_data.get("category") or "" 
    
    filter_param = request_data.get("filter_param") or "totprgmrevnue"
    
    year = request_data.get("year") or "2020"

    try:
        parameters_list = ['totprgmrevnue', 'grsincfndrsng ', 'totrevenue', 'gftgrntsrcvd170' , 'compnsatncurrofcr', 'pdf_url']
        
        sorted_orgs = get_non_profits(state, category, parameters_list, filter_param, year)


        flash("Fetched Real-time Market Data!", "success")
        return render_template("stocks_dashboard.html",
            #What do we pass into the dashboard??? Info for graph + parameters we define
            state=state,
        )
    except Exception as err:
        print('OOPS', err)


        flash("Market Data Error. Please check your symbol and try again!", "danger")
        return redirect("/stocks/form")

