#!/usr/bin/env python3

from flask import Flask, redirect, render_template, request
from mini_cactpot import Result

app = Flask(__name__)


@app.context_processor
def ticket_payout():
    """
    Make the values of payouts available to all templates
    """
    values = [10000, 36, 720, 360, 80, 252, 108, 72, 54, 180,
              72, 180, 119, 36, 306, 1080, 144, 1800, 3600]
    return dict(payout=values)


@app.route("/mini-cactpot", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/mini-cactpot/result", methods=["POST"])
def result():
    """
    Get user inputs from POST and calculate results
    """

    # Get user inputs from form and convert to list of ints
    inputs = request.form.getlist("user_inputs")
    inputs = [int(i) for i in inputs]

    # Redirect to index if user does not choose 4 numbers
    if inputs.count(0) != 5:
        return redirect("/mini-cactpot")

    # Check if user repeats numbers
    for number in inputs:
        if number:
            if inputs.count(number) != 1:
                return redirect("/mini-cactpot")

    # Dictionary of lines payout and suggestion
    results = Result(inputs)
    results = results.calculate()

    # Line number and cell ids for highlighting payout
    keys = [i for i in results["suggestion"][0].keys()]
    values = [i for j in results["suggestion"][0].values() for i in j]

    return render_template("result.html", results=results, inputs=inputs, keys=keys, values=values)
