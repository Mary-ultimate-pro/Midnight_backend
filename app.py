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
    players = db.Column(db.Integer, nullable=True)

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

    def __init__(self, name, score, is_active, is_winner, is_round, game_id):
        self.name = name
        self.score = score
        self.is_active = is_active
        self.is_winner = is_winner
        self.is_round = is_round
        self.game_id = game_id


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


class Winner(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    score = db.Column(db.Integer, nullable=True)
    number = db.Column(db.Integer)
    round_id = db.Column(db.Integer, db.ForeignKey(Round.id), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id), nullable=True)
    deck_id = db.Column(db.Integer, db.ForeignKey(Deck.id), nullable=True)
    is_player = db.Column(db.Boolean, default=False)

    def __init__(self, name, score, number, round_id, game_id, deck_id, is_player):
        self.name = name
        self.score = score
        self.number = number
        self.round_id = round_id
        self.game_id = game_id
        self.deck_id = deck_id
        self.is_player = is_player


class WinnerSchema(ma.Schema):
    class Meta:
        fields = (
            "name",
            "score",
            "number",
            "round_id"
            "game_id",
            "deck_id",
            "players",
        )


winner_schema = WinnerSchema()
winners_schema = WinnerSchema(many=True)


class Active(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    score = db.Column(db.Integer, nullable=True)
    round_id = db.Column(db.Integer, db.ForeignKey(Round.id), nullable=True)
    game_id = db.Column(db.Integer, db.ForeignKey(Game.id), nullable=True)
    number = db.Column(db.Integer)

    def __init__(self, name, score, number, round_id, game_id):
        self.name = name
        self.score = score
        self.number = number
        self.round_id = round_id
        self.game_id = game_id


class ActiveSchema(ma.Schema):
    class Meta:
        fields = (
            "name",
            "score",
            "number",
            "round_id",
            "game_id",
        )


active_schema = ActiveSchema()
actives_schema = ActiveSchema(many=True)


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

    new_player = Player(name, score, is_active, is_winner, round_id, game_id, )

    db.session.add(new_player)
    db.session.commit()

    return player_schema.jsonify(new_player)


@app.get("/player")
def get_players():
    players = players_schema.dump(Player.query.all())
    return jsonify(players)


@app.get("/player/<id>")
def get_player(id):
    player = Player.query.get(id)
    return player_schema.jsonify(player)


@app.post("/game")
def create_game():
    # id = request.json["id"]
    name = request.json["name"]
    # score = request.json["score"]
    players = request.json["players"]
    deck = request.json["deck"]

    new_game = Game(name, players, deck)

    db.session.add(new_game)
    db.session.commit()

    return game_schema.jsonify(new_game)


@app.get("/game")
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


@app.post("/round")
def create_round():
    # id = request.json["id"]
    number = request.json["number"]
    players = request.json["players"]

    new_round = Round(number, players)

    db.session.add(new_round)
    db.session.commit()

    return round_schema.jsonify(new_round)


@app.get("/round")
def get_rounds():
    rounds = rounds_schema.dump(Round.query.all())
    return jsonify(rounds)


@app.get("/round/<id>")
def get_round(id):
    round = Round.query.get(id)
    return round_schema.jsonify(round)


@app.post("/winner")
def create_winner():
    name = request.json["name"]
    score = request.json["score"]
    number = request.json["number"]
    round_id = request.json["round_id"]
    game_id = request.json["game_id"]
    # is_active = request.json["is_active"]
    deck_id = request.json["deck_id"]
    is_player = request.json["is_player"]

    new_winner = Winner(name, score, number, round_id, game_id, deck_id, is_player)
    db.session.add(new_winner)
    db.session.commit()

    return winner_schema.jsonify(new_winner)


@app.get("/winner")
def get_winners():
    winners = winners_schema.dump(Winner.query.all())
    return jsonify(winners)


@app.get("/winner/<id>")
def get_winner(id):
    winner = Winner.query.get(id)
    return winner_schema.jsonify(winner)


@app.post("/active")
def create_active():
    name = request.json["name"]
    score = request.json["score"]
    round_id = request.json["round_id"]
    game_id = request.json["game_id"]
    number = request.json["number"]

    new_active = Active(name, score, number, round_id, game_id)
    db.session.add(new_active)
    db.session.commit()

    return active_schema.jsonify(new_active)


@app.get("/active")
def get_actives():
    actives = actives_schema.dump(Active.query.all())
    return jsonify(actives)


@app.get("/active/<id>")
def get_active(id):
    active = Active.query.get(id)
    return active_schema.jsonify(active)
