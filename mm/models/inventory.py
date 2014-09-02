""" This contains a list of all models used by Multiverse Miner"""

from mm import db

class Inventory(db.Model):
    # This table is personal inventory only.
    __tablename__ = 'inventory'
    character_name = db.Column(db.ForeignKey('character.name'), primary_key=True)
    item_id = db.Column(db.ForeignKey('item.id'), primary_key=True)
    amount = db.Column(db.Integer, default=1, nullable=False)

    character = db.relationship("Character", backref=db.backref('inventory', uselist=True), uselist=False)
    item = db.relationship("Item", uselist=False, foreign_keys=[item_id])

    db.PrimaryKeyConstraint('item_id', 'character_name', name='inventory_pk')

    def __repr__(self):
        """ return a tag for the inventory"""
        return '<Inventory %s %s for %s>' % (self.amount, self.item_id, self.character_name)

    def __unicode__(self):
        """ return the unicode name """
        return '<Inventory %s %s for %s>' % (self.amount, self.item_id, self.character_name)
