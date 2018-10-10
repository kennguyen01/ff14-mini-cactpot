from flask import Flask, flash, redirect, render_template, request
from mini_cactpot import calculate

app = Flask(__name__)


@app.context_processor
def ticket_payout():
    """
    Make the values of payouts available to all templates
    """
    values = [10000, 36, 720, 360, 80, 252, 108, 72, 54, 180,
              72, 180, 119, 36, 306, 1080, 144, 1800, 3600]
    return dict(payout=values)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    """
    Get user inputs from POST and calculate results
    """

    # Get user inputs and conver to int
    inputs = request.form.getlist("user_inputs")
    inputs = [int(i) for i in inputs]

    # Redirect user to index if inputs != 4
    if inputs.count(0) != 5:
        return redirect("/")

    # Check if user repeats numbers
    for number in inputs:
        if number:
            if inputs.count(number) != 1:
                return redirect("/")

    # Dictionary of lines payout and suggestion
    results = calculate(inputs)

    # Line number and cell ids for highlighting payout
    keys = [i for i in results["suggestion"][0].keys()]
    values = [i for j in results["suggestion"][0].values() for i in j]

    return render_template("result.html", results=results, inputs=inputs, keys=keys, values=values)
