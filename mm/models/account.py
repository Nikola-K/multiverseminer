""" This contains a list of all models used by Multiverse Miner"""

from mm import db
from datetime import datetime, timedelta


class Account(db.Model):
    """ Account object represents an individual user"""

    time = datetime.utcnow()
    id = db.Column(db.Integer, primary_key=True)
    oauth_id = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    realname = db.Column(db.String(64), nullable=False)
    provider = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=time, nullable=False)
    last_login = db.Column(db.DateTime)
    access_level = db.Column(db.Integer, default='0', nullable=False)
    # In the future I can imagine more collection types.
    last_mine = db.Column(db.DateTime, default=time, nullable=False)
    last_gather = db.Column(db.DateTime, default=time, nullable=False)
    last_scavenge = db.Column(db.DateTime, default=time, nullable=False)

    character_id = db.Column(db.ForeignKey('character.name', name="fk_acc_id", use_alter=True))
    character = db.relationship("Character", uselist=False, remote_side=[character_id])


    planet_id = db.Column(db.ForeignKey('planet.id'))
    planet = db.relationship("Planet", backref='players')

    def __repr__(self):
        """ return a tag for the player"""
        return '<Account %s>' % (self.username)

    def __unicode__(self):
        """ return the unicode name """
        return self.username


