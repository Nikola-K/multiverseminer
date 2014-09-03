""" This contains a list of all models used by Multiverse Miner"""

from mm import db


class PlanetLoot(db.Model):
    """ ingredient is an association table that crosses the
        recipe with the child items and their amounts. """
    __tablename__ = 'planetloot'

    planet_id = db.Column(db.ForeignKey('planet.id'), primary_key=True)
    item_id = db.Column(db.ForeignKey('item.id'), primary_key=True)

    droprate = db.Column(db.Float, default=0, nullable=False)

    planet = db.relationship("Planet", backref='loot', foreign_keys=[planet_id])

    item = db.relationship("Item", backref='found_on', foreign_keys=[item_id])

    db.PrimaryKeyConstraint('planet_id', 'item_id', name='loot_pk')

    def __repr__(self):
        """ return a tag for the planet items"""
        return '<PlanetLoot %s %s on %s>' % (self.droprate, self.item_id, self.planet_id)

    def __eq__(self, itm):
        return self.planet_id == itm.planet_id and self.item_id == itm.item_id

    def __unicode__(self):
        """ return the unicode name """
        return "%s on %s" % (self.item_id, self.planet_id)
