"""
Author: Brian Smith (bcs4313)
This module serves as an DAO layer for the Slay The Spire 2 Model Context Protocol.
Information about this protocol can be found here: https://github.com/Gennadiyev/STS2MCP/blob/main/docs/raw-full.md
If you want more info: the docs of the repo has all the endpoints you would need
- In addition, any exceptions gary has in the program will be printed with the prefix 'Gary Stroke' :)
"""
import requests
import json
import time

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
    return r.json()


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
        if game_state["state_type"] != "monster" and game_state["state_type"] != "elite" and game_state["state_type"] != "boss":
            print("Vakku: Your are not fighting a monster right now. You test my patience mortal.")

        # get hand
        hand = game_state["player"]["hand"]
        print("Vakku: your hand sir -> " + str(hand))

        # base case 2: no cards
        if(len(hand) == 0):
            print("Vakku: you have nothing to play. I'm just gonna wait this one out.")

        # final case, scan for a card to play with your given energy pool
        energy = game_state["player"]["energy"]
        result = {}
        for i in range(len(hand)):
            card = hand[i]
            if(int(card["cost"]) <= energy):
                # card may or may not have a target
                if(card["target_type"] == "self"):
                    result = perform_action("play_card", {"card_index": i})
                else:
                    battle = game_state["battle"]
                    targetMonsterID = battle["enemies"][0]["entity_id"]
                    result = perform_action("play_card", {"card_index": i, "target": targetMonsterID})

                # sometimes a card can't be played for other reasons...
                if (result.get("status") == "error"):
                    print("Vakku card can't be played at index: " + str(i))
                    continue

                return result

        return result


def can_play_first_card():
    print("Vakku: scanning your game state...")
    game_state = get_full_game_state()

    # base case 1: no game state
    if game_state == "":
        return False
    else:
        # base case 2: not fighting
        if game_state["state_type"] != "monster" and game_state["state_type"] != "elite" and game_state["state_type"] != "boss":
            return False

        # base case 3: no hand or player
        if(game_state.get("player") == None or game_state.get("player").get("hand") == None):
            return False

        # get hand
        hand = game_state["player"]["hand"]
        #print("Vakku: your hand sir -> " + str(hand))

        # base case 2: no cards
        if (len(hand) == 0):
            return False

        # final case, scan for a card to play with your given energy pool
        energy = game_state["player"]["energy"]
        for card in hand:
            if(int(card["cost"]) <= energy):
                return True
        return False


# Automatically plays the game for you as Vakku
def vakku_simulator():

    while(True):
        time.sleep(0.3)
        if can_play_first_card():
            result = play_first_card()
            if(result.get("status") == "error"):
                print("Vakku: They blocked me. Ending my turn now")
                perform_action("end_turn", {})

        # end turn if at 0 energy
        game_state = get_full_game_state()
        if(game_state.get("player") != None and game_state["player"].get("energy") != None and int(game_state["player"]["energy"]) == 0):
            print("Vakku: Ending my turn now")
            perform_action("end_turn", {})

if __name__ == "__main__":
    get_full_game_state()
    vakku_simulator()