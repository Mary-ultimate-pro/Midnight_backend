# from app import db
# from sqlsaddedlalchemy.orm import relationship
#
#
# class Card(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     suit = db.Column(db.String(50))
#     rank = db.Column(db.String(50))
#     value = db.Column(db.integer)
#     deck_id = db.Column(db.Integer, db.ForeignKey("decks.id"))
#
#
# class Player(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(50))
#     score = db.Column(db.integer)
#     round_id = db.Column(db.Integer, db.ForeignKey("rounds.id"))
#
#
# class Round(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     number = db.Column(db.Integer)
#     active_players = db.Column(db.string(50))
#     winners = db.Column(db.string(50))
#
#
# class Game(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(50))
#     players = db.Column(db.String(50))
#     related_name = db.Column(db.integer)
#     deck = db.Column(db.integer)
#     status = db.Column(db.String(50))
#
#
# class Deck(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     card = db.Column(db.String(50))
#     shuffled = db.Column(db.String(50))
#     drawn_cards = db.Column(db.integer)
#
#
