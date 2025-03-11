import os
from flask import Flask, jsonify, request
from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi
from discord_interactions import verify_key_decorator
from dotenv import load_dotenv
import pandas as pd
import sqlite3

load_dotenv()

DISCORD_PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
handler = Mangum(asgi_app)


@app.route("/", methods=["POST"])
async def interactions():
    print(f"👉 Request: {request.json}")
    raw_request = request.json
    return interact(raw_request)


#@verify_key_decorator(DISCORD_PUBLIC_KEY)

# def create_db_from_csv(csv_file, db_file):


def get_card_by_id_and_collection(card_id, collection, db_file='cards.db'):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cardObject = {
        id: None,
        "PokedexNumber": None,
        "name": None,
        "rarity": None,
        "collection": None,
        "type": None,
        "stage": None,
        "description": None
    }
    if collection is None:
        cursor.execute("SELECT * FROM cards WHERE rowid = ?", (card_id,))
    else:
        cursor.execute("SELECT * FROM cards WHERE ID = ? AND Collection = ?", (card_id, collection))
    card = cursor.fetchone()
    cardObject = {
        "id": card[0],
        "PokedexNumber": card[1],
        "name": card[2],
        "rarity": card[3],
        "collection": card[4],
        "type": card[5],
        "stage": card[6],
        "image": card[7],
    }
    print(card)
    conn.close()
    if card is None:
        return "Card not found"
    else:
        return cardObject



def interact(raw_request):
    if raw_request["type"] == 1:  # PING
        response_data = {"type": 1}  # PONG
    else:
        data = raw_request["data"]
        command_name = data["name"]

        if command_name == "hello":
            message_content = "Hello there!"
        elif command_name == "findCardByPokedexID":
            cardId = data["options"][0]["value"]
            if len(data["options"]) > 1 and "value" in data["options"][1]:
                collection = data["options"][1]["value"]
            else:
                collection = None
            message_content = get_card_by_id_and_collection(cardId, collection)
        elif command_name == "echo":
            original_message = data["options"][0]["value"]
            message_content = f"Echoing: {original_message}"

        response_data = {
            "type": 4,
            "data": {"content": message_content},
        }
    print(f"👈 Response: {response_data}")
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)