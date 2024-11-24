from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def get_population_data():
    url = "https://countriesnow.space/api/v0.1/countries/population/cities"
    response = requests.get(url)
    return response.json().get("data", [])

def get_flags_data():
    url = "https://countriesnow.space/api/v0.1/countries/flag/images"
    response = requests.get(url)
    data = response.json().get('data')
    return data

def get_capital():
    url = "https://countriesnow.space/api/v0.1/countries/capital"
    response = requests.get(url)
    data = response.json().get('data')
    return data

@app.route("/flag", methods=["GET", "POST"])
def flag():
    result = None
    if request.method == "POST":
        country_name = request.form.get("country")
        data = get_flags_data()
        for country in data:
            if country["name"].lower() == country_name.lower():
                result = {"name": country["name"], "flag": country["flag"]}
                break
        if not result:
            result = {"error": f"No flag found for '{country_name}'."}
    return render_template("flag.html", result=result)

@app.route("/population")
def population():
    data = get_population_data()
    return render_template("population.html", data=data)

@app.route("/capital")
def capital():
    data = get_capital()
    return render_template("capital.html", data=data)
    
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
