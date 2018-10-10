# FF14 Mini Cactpot Calculator
A brute force calculator for the Mini Cactpot game in Final Fantasy 14

This program calculates the best payout by enumerating
all possible combinations for each 3-number line.

The game consists of a 3x3 scratch off ticket with 1 number given to the user.
User picks 3 additional numbers to fill in the ticket. For example:

4   5   6   7  8
3 | 1 | 3 | x
2 | x | 9 | x
1 | x | x | 7

The numbers 1-8 indicate the 3-number lines used to calculate payout.

This program can be run with just the script on
Python 3 or hosted on a website with the Flask app.