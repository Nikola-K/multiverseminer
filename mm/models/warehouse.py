""" This contains a list of all models used by Multiverse Miner"""

from mm import db


class Warehouse(db.Model):
    # This table is planetary inventory only.
    __tablename__ = 'warehouse'
    character_name = db.Column(db.ForeignKey('character.name'), primary_key=True)
    planet_id = db.Column(db.ForeignKey('planet.id'), primary_key=True)
    item_id = db.Column(db.ForeignKey('item.id'), primary_key=True)
    amount = db.Column(db.Integer, default=1, nullable=False)

    character = db.relationship("Character", backref='warehouse', foreign_keys=[character_name])
    planet = db.relationship("Planet", backref='warehouse', foreign_keys=[planet_id])
    item = db.relationship("Item",  foreign_keys=[item_id])

    db.PrimaryKeyConstraint('item_id', 'character_name', 'planet_id', name='warehouse_pk')

    def __repr__(self):
        """ return a tag for the warehouse"""
        return '<Warehouse %s %s for %s on %s>' % (self.amount, self.item_id, self.character_name, self.planet_id)

    def __unicode__(self):
        """ return the unicode name """
        return '<Warehouse %s %s for %s on %s>' % (self.amount, self.item_id, self.character_name, self.planet_id)
