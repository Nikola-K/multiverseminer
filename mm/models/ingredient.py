""" This contains a list of all models used by Multiverse Miner"""

from mm import db
from flask import jsonify
from datetime import datetime, timedelta
from random import randint
from mm.exceptions import CraftingException


class Ingredient(db.Model):
    """ ingredient is an association table that crosses the
        recipe with the child items and their amounts. """
    __tablename__ = 'ingredient'

    recipe_id = db.Column(db.ForeignKey('item.id'), primary_key=True)
    item_id = db.Column(db.ForeignKey('item.id'), primary_key=True)
    amount = db.Column(db.Integer, default=1, nullable=False)

    recipe = db.relationship("Item", backref='ingredients',
                             foreign_keys=[recipe_id])
    item = db.relationship("Item", backref='usedIn', foreign_keys=[item_id])

    db.PrimaryKeyConstraint('recipe_id', 'item_id', name='ingredient_pk')

    def __repr__(self):
        """ return a tag for the ingredient"""
        return '<Ingredient %s %s for %s>' % (self.amount,
                                              self.item_id, self.recipe_id)

    def __eq__(self, itm):
        return (hasattr(itm, 'recipe_id') and
                hasattr(itm, 'item_id') and
                self.recipe_id == itm.recipe_id and
                self.item_id == itm.item_id)

    def __unicode__(self):
        """ return the unicode name """
        return "Ingredient for %s " % self.recipe_id
