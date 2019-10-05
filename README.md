# FF14 Mini Cactpot Flask App
A brute force calculator for the [Mini Cactpot](https://na.finalfantasyxiv.com/lodestone/playguide/contentsguide/goldsaucer/cactpot/#anchor_002) game in Final Fantasy 14

Link to web app: [Mini Cactpot Calculator](https://kingle.pythonanywhere.com/mini-cactpot)

## About

This program calculates the best payout by enumerating all possible combinations for each 3-number line. The game consists of a 3x3 scratch off ticket with 1 number given to the user. User picks 3 additional numbers to fill in the ticket. In the picture below, number 1 to 8 on the outside indicate each 3-number lines used to calculate payout.

For example:

    4   5   6   7   8  
    3 | 1 | 3 | x  
    2 | x | 9 | x  
    1 | x | x | 7
    
The app will display the average of all lines and highlight the line with highest payout.

      180  211  146  227  395
    ********************
     2253   1    3    0
    ********************
      395   0    9    0
      227   0    0    7

## Running App Locally on Linux

Clone repo and install all dependencies. Then `cd` to the app directory and enter this in the terminal:

```console
$ export FLASK_APP=application.py FLASK_DEBUG=1
flask run
```

The app will now be deployed locally on [http://127.0.0.1:5000/](http://127.0.0.1:5000/). The `FLASK_DEBUG=1` flag lets the app reload automatically after changes to the code.
