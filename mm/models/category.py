""" This contains a list of all models used by Multiverse Miner"""

from mm import db

class Category(db.Model):
    """ Category models the hierarchy of items."""
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    parent_id = db.Column(db.ForeignKey('category.id'))
    parent = db.relationship("Category")

    def __repr__(self):
        """ return a tag for the category"""
        return '<Category %r>' % (self.name)

    def __unicode__(self):
        """ return the unicode name """
        return self.name
