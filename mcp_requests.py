"""
Author: Brian Smith (bcs4313)
This module serves as an DAO layer for the Slay The Spire 2 Model Context Protocol.
Information about this protocol can be found here: https://github.com/Gennadiyev/STS2MCP/blob/main/docs/raw-full.md
If you want more info: the docs of the repo has all the endpoints you would need
- In addition, any exceptions gary has in the program will be printed with the prefix 'Gary Stroke' :)
"""
import requests


# endpoint GET methods
def get_full_game_state():
    try:
        r = requests.get("http://localhost:15526/api/v1/singleplayer")
        return r.content
    except Exception as e:
        print("Gary Stroke: get_full_game_state exception: " + e)

    return ""  # failure case

# endpoint POST methods

if __name__ == "__main__":
    get_full_game_state()