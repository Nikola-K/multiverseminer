""" This contains a list of all models used by Multiverse Miner"""

from mm import db


class Planet(db.Model):
    """ """
    id = db.Column(db.String(64), primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)

    mineable_max = db.Column(db.Integer, default=100000, nullable=False)
    mineable_remaining = db.Column(db.Integer, default=100000, nullable=False)
    mineable_replenish = db.Column(db.Float, default=1.1, nullable=False)

    gatherable_max = db.Column(db.Integer, default=100000, nullable=False)
    gatherable_remaining = db.Column(db.Integer, default=100000, nullable=False)
    gatherable_replenish = db.Column(db.Float, default=1.1, nullable=False)

    scavengable_max = db.Column(db.Integer, default=100000, nullable=False)
    scavengable_remaining = db.Column(db.Integer, default=100000, nullable=False)
    scavengable_replenish = db.Column(db.Float, default=1.1, nullable=False)

    def __repr__(self):
        """ return a tag for the planet"""
        return '<Planet %s>' % (self.name)

    def __unicode__(self):
        """ return the unicode name """
        return self.name
