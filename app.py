import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow

load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)

url = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = url
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

ma = Marshmallow(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    players = relationship("Player", backref="game")
    deck = relationship("Deck", backref="game")

    def __init__(self, name, players, deck):
        self.name = name
        self.players = players
        self.deck = deck


class GameSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "players", "deck")


game_schema = GameSchema()
games_schema = GameSchema(many=True)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cards = relationship("Card", backref="cards_deck")
    shuffled = db.Column(db.Boolean, default=False)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id), nullable=True)

    def __init__(self, cards, shuffled, game_id):
        self.cards = cards
        self.shuffled = shuffled
        self.game_id = game_id


class DeckSchema(ma.Schema):
    class Meta:
        fields = ("id", "cards", "shuffled")


deck_schema = DeckSchema()
decks_schema = DeckSchema(many=True)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    suit = db.Column(db.String(50), nullable=True)
    rank = db.Column(db.String(50), nullable=True)
    value = db.Column(db.Integer)
    deck_id = db.Column(db.Integer, db.ForeignKey(Deck.id), nullable=True)
    is_drawn = db.Column(db.Boolean, default=False)

    def __init__(self, suit, rank, value, deck_id, is_drawn):
        self.suit = suit
        self.rank = rank
        self.value = value
        self.deck_id = deck_id
        self.is_drawn = is_drawn


class CardSchema(ma.Schema):
    class Meta:
        fields = ("id", "suit", "rank", "value", "deck_id", "is_drawn")


card_schema = CardSchema()
cards_schema = CardSchema(many=True)


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer)
    players = relationship("Player", backref="round_players")

    def __init__(self, number, players):
        self.number = number
        self.players = players


class RoundSchema(ma.Schema):
    class Meta:
        fields = ("id", "number", "players")


round_schema = RoundSchema()
rounds_schema = RoundSchema(many=True)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    score = db.Column(db.Integer, nullable=True)
    round_id = db.Column(db.Integer, db.ForeignKey(Round.id), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    is_winner = db.Column(db.Boolean, default=False)

    def __init__(self, name, score, is_active, is_winner):
        self.name = name
        self.score = score
        self.is_active = is_active
        self.is_winner = is_winner


class PlayerSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "score",
            "round_id",
            "game_id",
            "is_active",
            "is_winner",
        )


player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)


@app.get("/")
def home():
    return "Hello world!"


# creates a new card
@app.post("/card")
def create_card():
    suit = request.json["suit"]
    rank = request.json["rank"]
    value = request.json["value"]
    deck_id = request.json["deck_id"]
    is_drawn = request.json["is_drawn"]

    new_card = Card(suit, rank, value, deck_id, is_drawn)

    db.session.add(new_card)
    db.session.commit()

    return card_schema.jsonify(new_card)


# gets all cards
@app.get("/card")
def get_cards():
    cards = cards_schema.dump(Card.query.all())
    return jsonify(cards)


# get a single card
@app.get("/card/<id>")
def get_card(id):
    card = Card.query.get(id)
    return card_schema.jsonify(card)


with app.app_context():
    db.create_all()


# create a new_player
@app.post("/player")
def create_player():
    # id = request.json["id"]
    name = request.json["name"]
    score = request.json["score"]
    round_id = request.json["round_id"]
    game_id = request.json["game_id"]
    is_active = request.json["is_active"]
    is_winner = request.json["is_winner"]

    new_player = Player(name, score, is_active, is_winner, round_id, game_id, id)

    db.session.add(new_player)
    db.session.commit()

    return player_schema.jsonify(new_player)


@app.post("/game")
def create_game():
    # id = request.json["id"]
    name = request.json["name"]
    # score = request.json["score"]
    players = request.json["players"]
    deck = request.json["deck"]

    new_game = Game(name, players , deck)

    db.session.add(new_game)
    db.session.commit()

    return game_schema.jsonify(new_game)


@app.get("/")
def get_games():
    games = games_schema.dump(Game.query.all())
    return jsonify(games)


@app.get("/game/<id>")
def get_game(id):
    game = Game.query.get(id)
    return game_schema.jsonify(game)


@app.post("/deck")
def create_deck():
    # id = request.json["id"]
    cards = request.json["cards"]
    shuffled = request.json["shuffled"]
    game_id = request.json["game_id"]

    new_deck = Deck(cards, shuffled, game_id)

    db.session.add(new_deck)
    db.session.commit()

    return deck_schema.jsonify(new_deck)


@app.get("/")
def get_decks():
    decks = decks_schema.dump(Deck.query.all())
    return jsonify(decks)


@app.get("/deck/<id>")
def get_deck(id):
    deck = Deck.query.get(id)
    return deck_schema.jsonify(deck)


@app.post("/deck")
def create_round():
    # id = request.json["id"]
    number = request.json["number"]
    players = request.json["players"]

    new_round = Round(id, number, players)

    db.session.add(new_round)
    db.session.commit()

    return round_schema.jsonify(new_round)


@app.get("/")
def get_rounds():
    rounds = rounds_schema.dump(Round.query.all())
    return jsonify(rounds)


@app.get("/round/<id>")
def get_round(id):
    round = Round.query.get(id)
    return round_schema.jsonify(round)
