"""
Author: Brian Smith (bcs4313)
This module serves as an DAO layer for the Slay The Spire 2 Model Context Protocol.
Information about this protocol can be found here: https://github.com/Gennadiyev/STS2MCP/blob/main/docs/raw-full.md
If you want more info: the docs of the repo has all the endpoints you would need
- In addition, any exceptions gary has in the program will be printed with the prefix 'Gary Stroke' :)
"""
import requests
import json

# endpoint GET methods
def get_full_game_state():
    try:
        r = requests.get("http://localhost:15526/api/v1/singleplayer")
        return r.json()  # content is raw bytes unless converted
    except Exception as e:
        print("Gary Stroke: get_full_game_state exception: " + str(e))

    return ""  # failure case

# endpoint POST methods

# perform action
# @param str action: string representing the main intent behind the request
# @param dict params: a json-like dictionary containing attributes that describe our action
def perform_action(action, params):
    params["action"] = action
    r = requests.post("http://localhost:15526/api/v1/singleplayer", json=params)
    print("perform_action status: " + str(r.status_code))
    print("perform_action response body: " + str(r.json()))


# Example utility methods, for experimentation
# VAKKU Simulator
def play_first_card():
    print("Vakku: scanning your game state...")
    game_state = get_full_game_state()

    # base case 1: no game state
    if game_state == "":
        print("Vakku: failed to find your game state. Why do you disappoint him?")
    else:
        # base case 2: not fighting
        if game_state["state_type"] != "monster":
            print("Vakku: Your are not fighting a monster right now. You test my patience mortal.")

        # get hand
        hand = game_state["player"]["hand"]
        print("Vakku: your hand sir -> " + str(hand))

        # base case 2: no cards
        if(len(hand) == 0):
            print("Vakku: you have nothing to play. I'm just gonna wait this one out.")

        perform_action("play_card", {"card_index": 0})

if __name__ == "__main__":
    play_first_card()