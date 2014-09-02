""" This contains a list of all models used by Multiverse Miner"""

from mm import db
from datetime import datetime, timedelta


class Item(db.Model):
    """ Primary table with all the goodies. """
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    category_id = db.Column(db.ForeignKey('category.id'))

    accuracy = db.Column(db.Float, default=0, nullable=False)
    attack = db.Column(db.Float, default=0, nullable=False)
    attack_speed = db.Column(db.Float, default=0, nullable=False)
    auto_gather = db.Column(db.Float, default=0, nullable=False)
    auto_mine = db.Column(db.Float, default=0, nullable=False)
    auto_refine = db.Column(db.Float, default=0, nullable=False)
    auto_produce_id = db.Column(db.ForeignKey('item.id'))
    auto_scavenge = db.Column(db.Float, default=0, nullable=False)
    defense = db.Column(db.Float, default=0, nullable=False)
    description = db.Column(db.Text, default=0, nullable=False)
    evasion = db.Column(db.Float, default=0, nullable=False)
    experience = db.Column(db.Integer, default=0, nullable=False)
    # NOTE gear_type may not be needed- we could just query the category.
    gear_type = db.Column(db.String(64))
    health = db.Column(db.Float, default=0, nullable=False)
    lootLuck = db.Column(db.Float, default=0, nullable=False)
    minimum_miningLevel = db.Column(db.Integer, default=0, nullable=False)
    mining_luck = db.Column(db.Float, default=0, nullable=False)
    perception = db.Column(db.Float, default=0, nullable=False)
    planet_limit = db.Column(db.Float, default=0, nullable=False)
    regeneration = db.Column(db.Float, default=0, nullable=False)
    resilience = db.Column(db.Float, default=0, nullable=False)
    scavenge_luck = db.Column(db.Float, default=0, nullable=False)
    ship_speed = db.Column(db.Float, default=0, nullable=False)
    storagelimit = db.Column(db.Integer, default=0, nullable=False)
    strength = db.Column(db.Float, default=0, nullable=False)
    value = db.Column(db.Integer, default=0, nullable=False)
    # FIXME craft-produce should tell how many of the item is created when crafted
    # for example you can make many copper necklaces from a copper bar, even accounting for waste
    category = db.relationship('Category', backref='items')

    # FIXME autoproduce untested
    autoproduce = db.relationship('Item', foreign_keys=[auto_produce_id])

    def contains(self, item):
        """ Check to see if an ingredient is in this item"""
        for ingredient in self.ingredients:
            if ingredient.item == item:
                return True
        return False

    def __eq__(self, other):
        return hasattr(other, 'id') and self.id == other.id

    def __repr__(self):
        """ return a tag for the item"""
        return '<Item %r>' % (self.name)

    def __unicode__(self):
        """ return the unicode name """
        return self.name
