import os
# import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()
app = Flask(__name__)
url = os.getenv("DATABASE_URL")
app.congig["SQLALCHEMY_DATABASE_URL"] = url
db.init(app)


# connection = psycopg2.connect(url)

@app.get("/")
def home():
    return "Hello"
# api = Api(app)
#
#

# # from flask_restful import Resource, Api
# #
# # CREATE_CARD_TABLE = """
# # CREATE TABLE IF NOT EXISTS cards (
# #    id SERIAL PRIMARY KEY,
# #    suit VARCHAR(10) NOT NULL,
# #    rank VARCHAR(10) NOT NULL,
# #    value INTEGER
# # );
# # """
# #
# # CREATE_PLAYER_TABLE = """
# # CREATE TABLE IF NOT EXISTS players (
# #     id SERIAL PRIMARY KEY,
# #     name VARCHAR(255) NOT NULL,
# #     score INTEGER
# # );
# # """
# #
# # CREATE_DECK_TABLE = """
# # CREATE TABLE IF NOT EXISTS decks (
# #     id SERIAL PRIMARY KEY,
# #     name VARCHAR(255) NOT NULL,
# #     description TEXT,
# #     owner_id INTEGER REFERENCES players(id),
# #     shuffled BOOLEAN DEFAULT FALSE,
# #     drawn_cards JSONB DEFAULT '[]'
# # );
# # """
# #
# # CREATE_GAME_TABLE = """
# # CREATE TABLE IF NOT EXISTS games (
# #     id SERIAL PRIMARY KEY,
# #     name VARCHAR(100) NOT NULL,
# #     current_turn INTEGER,
# #     deck_id INTEGER REFERENCES decks(id)
# # );
# # """
# #
# # CREATE_ROUND_TABLE = """
# # CREATE TABLE IF NOT EXISTS rounds (
# #     id SERIAL PRIMARY KEY,
# #     active_players INTEGER ARRAY,
# #     community_cards INTEGER ARRAY,
# #     betting_round VARCHAR(20),
# #     winners VARCHAR(100) ARRAY
# # );
# # """
# #
# # insert_card = """
# # INSERT INTO cards (suit, rank, value)
# # VALUES (%s, %s, %s);
# # """
# #
# # insert_player = """
# # INSERT INTO players (name, score)
# # VALUES (%s, %s);
# # """
# #
# # insert_deck = """
# # INSERT INTO decks (name, description, owner_id, shuffled, drawn_cards)
# # VALUES (%s, %s, %s, %s, %s);
# # """
# #
# # insert_game = """
# # INSERT INTO games (name, current_turn, deck_id)
# # VALUES (%s, %s, %s);
# # """
# #
# # insert_round = """
# # INSERT INTO rounds (active_players, community_cards, betting_round, winners)
# # VALUES (%s, %s, %s, %s);
# # """
# #
# load_dotenv()
# app = Flask(__name__)
# api = Api(app)
# url = os.getenv("DATABASE_URL")
# connection = psycopg2.connect(url)
# #
# #
# # @app.post("/api/room")
# # def create_card():
# #     try:
# #         data = requests.get_json()
# #         card_data = data["card"]
# #         with connection.cursor() as cursor:
# #             cursor.execute(insert_card, (card_data["suit"], card_data["rank"], card_data["value"]))
# #             cursor.execute("SELECT * FROM cards")
# #
# #             # Fetch all rows of the result
# #             rows = cursor.fetchall()
# #
# #             # Convert the result into a list of dictionaries
# #             card_data = []
# #             for row in rows:
# #                 card = {
# #                     "id": row[0],
# #                     "suit": row[1],
# #                     "rank": row[2],
# #                     "value": row[3]
# #                 }
# #                 card_data.append(card)
# #
# #             return jsonify(card_data)
# #         connection.commit()
# #
# #         return jsonify({"message": "Card created successfully"}), 201
# #
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500
#
#
# import os
# import psycopg2
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify
# from flask_restful import Resource, Api
#
#
# app = Flask(__name__)
# api = Api(app)
# url = os.getenv("DATABASE_URL")
# connection = psycopg2.connect(url)
#
# CREATE_CARD_TABLE = """
# CREATE TABLE IF NOT EXISTS cards (
#    id SERIAL PRIMARY KEY,
#    suit VARCHAR(10) NOT NULL,
#    rank VARCHAR(10) NOT NULL,
#    value INTEGER
# );
# """
#
# CREATE_PLAYER_TABLE = """
# CREATE TABLE IF NOT EXISTS players (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     score INTEGER
# );
# """
#
# CREATE_DECK_TABLE = """
# CREATE TABLE IF NOT EXISTS decks (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     description TEXT,
#     owner_id INTEGER REFERENCES players(id),
#     shuffled BOOLEAN DEFAULT FALSE,
#     drawn_cards JSONB DEFAULT '[]'
# );
# """
#
# CREATE_GAME_TABLE = """
# CREATE TABLE IF NOT EXISTS games (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     current_turn INTEGER,
#     deck_id INTEGER REFERENCES decks(id)
# );
# """
#
# CREATE_ROUND_TABLE = """
# CREATE TABLE IF NOT EXISTS rounds (
#     id SERIAL PRIMARY KEY,
#     active_players INTEGER ARRAY,
#     community_cards INTEGER ARRAY,
#     betting_round VARCHAR(20),
#     winners VARCHAR(100) ARRAY
# );
# """
#
# insert_card = """
# INSERT INTO cards (suit, rank, value)
# VALUES (%s, %s, %s);
# """
#
# insert_player = """
# INSERT INTO players (name, score)
# VALUES (%s, %s);
# """
#
# insert_deck = """
# INSERT INTO decks (name, description, owner_id, shuffled, drawn_cards)
# VALUES (%s, %s, %s, %s, %s);
# """
#
# insert_game = """
# INSERT INTO games (name, current_turn, deck_id)
# VALUES (%s, %s, %s);
# """
#
# insert_round = """
# INSERT INTO rounds (active_players, community_cards, betting_round, winners)
# VALUES (%s, %s, %s, %s);
# """
#
#
# @app.post("/api/card")
# class Midnight(Resource):
#     def create_card(self):
#         try:
#             data = request.get_json()
#             card_data = data["card"]
#             with connection.cursor() as cursor:
#                 cursor.execute(insert_card, (card_data["suit"], card_data["rank"], card_data["value"]))
#             connection.commit()
#             return jsonify({"message": "Card created successfully"}), 201
#
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500
#
#
# @app.get("/api/cards")
# def get_cards():
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM cards")
#
#             # Fetch all rows of the result
#             rows = cursor.fetchall()
#
#             # Convert the result into a list of dictionaries
#             card_data = []
#             for row in rows:
#                 card = {
#                     "id": row[0],
#                     "suit": row[1],
#                     "rank": row[2],
#                     "value": row[3]
#                 }
#                 card_data.append(card)
#
#             return jsonify(card_data)
#
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#
#
# api.add_resource(Midnight, '/midnight')
#
# if __name__ == "__main__":
#     app.run(debug=True)
