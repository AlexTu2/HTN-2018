from flask import Flask
from flask import request, Response
import auth
import json
import decks
import pickle

app = Flask(__name__)

auth_system = auth.AuthObject("s03.jamesxu.ca", "mtg", "mtg123", "mtg")
deck_system = decks.DeckHandler("s03.jamesxu.ca", "mtg", "mtg123", "mtg")


def signed_in(username, token=0):
    return auth_system.logged_in[username] == token

@app.route('/')
def root():
    return 'Hello World!'


@app.route('/create_user', methods=["POST"])
def create_user():
    success = False
    if request.path == "/create_user":
        if request.method == "POST":

            data = request.get_json()
            status = auth_system.create_user(data['username'], data['password'])

            if status:
                success = True
                respArray = {"status": 200}
                response = Response()
                response.set_data(json.dumps(respArray))
                return response
    if not success:
        status = {"status": 500}
        response = Response()
        response.set_data(json.dumps(status))
        return response


@app.route('/sign_in', methods=["POST"])
def sign_in():
    success = False
    if request.path == "/sign_in":
        if request.method == "POST":

            data = request.get_json()
            status = auth_system.sign_in(data['username'], data['password'])

            if status:
                success = True
                respArray = {"status": 200, "token": status}
                response = Response()
                response.set_data(json.dumps(respArray))
                return response
    if not success:
        status = {"status": 500}
        response = Response()
        response.set_data(json.dumps(status))
        return response


@app.route('/get_decks', methods=["POST"])
def get_decks():
    data = request.get_json()
    token = data["token"]
    username = data['username']
    if auth_system.user_exists(username) and signed_in(username, token):
        resp = deck_system.retrieve_decks(username)
        if resp:
            response = Response()
            response.set_data(json.dumps({"status": 200, "data": resp}))

            return response

    response = Response()
    response.set_data(json.dumps({"status": 500, "data": None}))
    return response


@app.route('/set_deck', methods=["POST"])
def set_deck():
    data = request.get_json()
    token = data["token"]
    if request.method == "POST":
        data = request.get_json()
        username = data['username']
        if auth_system.user_exists(username) and signed_in(username, token):
            deck_name = data['deck_name']
            deck_data = data['deck_data']

            deck_system.set_deck(username, deck_name, deck_data)

            response = Response()
            response.set_data(json.dumps({"status": 200}))

            return response

    response = Response()
    response.set_data(json.dumps({"status": 500}))
    return response


@app.route('/del_deck', methods=["POST"])
def del_deck():
    data = request.get_json()
    token = data["token"]
    if request.method == "POST":
        data = request.get_json()
        username = data['username']
        if auth_system.user_exists(username) and signed_in(username, token):
            deck_name = data['deck_name']


            response = Response()
            response.set_data(json.dumps({"status": 200}))

            return response

    response = Response()
    response.set_data(json.dumps({"status": 500, "data": None}))
    return response


@app.route('/get_stats', methods=["POST"])
def get_stats():
    data = request.get_json()
    token = data["token"]
    if request.method == "POST":
        data = request.get_json()
        username = data['username']
        if auth_system.user_exists(username) and signed_in(username, token):

            respArray = deck_system.get_stats(username)
            if respArray:
                response = Response()
                response.set_data(json.dumps({"status": 200, "data": respArray}))

                return response

    response = Response()
    response.set_data(json.dumps({"status": 500, "data": None}))
    return response


@app.route('/get_cards', methods=["GET"])
def get_cards():
    cards = pickle.loads(open("CardList.pckl", "rb"))
    response = Response()
    response.set_data(json.dumps({"status": 500, "data": cards}))


if __name__ == '__main__':
    app.run()