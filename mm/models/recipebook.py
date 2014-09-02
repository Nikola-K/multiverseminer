""" This contains a list of all models used by Multiverse Miner"""

from mm import db


class RecipeBook(db.Model):
    # This table represents which recipes a character knows
    __tablename__ = 'recipebook'
    character_name = db.Column(db.ForeignKey('character.name'), primary_key=True)
    item_id = db.Column(db.ForeignKey('item.id'), primary_key=True)
    mastered = db.Column(db.Integer, default=1, nullable=False)

    character = db.relationship("Character", backref='recipebook', foreign_keys=[character_name])
    item = db.relationship("Item", foreign_keys=[item_id])

    db.PrimaryKeyConstraint('item_id', 'character_name', name='recipebook_pk')

    def __repr__(self):
        """ return a tag for the recipe"""
        return '<Recipe for %s owned by %s>' % (self.item_id, self.character_name)

    def __unicode__(self):
        """ return the unicode name """
        return '<Recipe for %s owned by %s>' % (self.item_id, self.character_name)
