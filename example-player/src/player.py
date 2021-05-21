import ast
from flask import Flask, request


app = Flask(__name__)

@app.route('/')
def health_check():
    # This endpoint will be ocasionally called by Kubernetes to check
    # if the application is still running
    return ''

@app.route('/roll-again')
def roll_again():
    # This will be the endpoint called by the game master server
    # Put your code here and return either "True" to roll again
    # or "False" to stop (the return value has to be a string)

    # This is your own score so far without the current rolls (int)
    own_score = request.args.get('own-score', type=int)

    # This is your opponents score so far (int)
    opp_score = request.args.get('opp-score', type=int)

    # This is the list of your rolls so far in this round (last being your
    # most recent roll) (list[int])
    current_rolls = request.args.get('current-rolls', type=ast.literal_eval)

    ### HERE GOES YOUR CODE ###

    return "False"
