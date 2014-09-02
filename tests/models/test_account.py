
import mm

from flask.ext.testing import TestCase

from mm.models import Account, Character, Planet
from mock import Mock
from config import TestConfiguration


class TestAccount(TestCase):
    """ Ensure that the account is functioning."""
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        """ """
        mm.app.config.from_object('config.TestConfiguration')
        return mm.app

    def setUp(self):
        """ """
        mm.db.create_all()
        self.bob = Account(username='Bob', oauth_id='111', email='bob@bob.com', provider='google', realname='bob')
        self.conan = Character(name='Conan')
        self.beowulf = Character(name='Beowulf')
        self.earth = Planet(name='Earth')
        mm.db.session.add(self.bob)
    def teardown(self):
        """ """
        mm.db.session.commit()
        mm.db.drop_all()

    def test_account_characters(self):
        """ validate character relationships """
        self.conan.account=self.bob
        self.assertEquals(self.bob.characters, [self.conan])

        self.bob.characters.append(self.beowulf)
        self.assertEquals(self.bob.characters, [self.conan, self.beowulf])

        self.assertEquals(self.bob.character, None)
        self.bob.character=self.beowulf
        self.assertEquals(self.bob.character, self.beowulf)

    def test_account_planet(self):
        """ validate planet relationship """

        self.bob.planet=self.earth
        token = "Token is %r" % self.bob.planet
        self.assertEquals("Token is <Planet Earth>", token)

    def test_account_strings(self):
        """ test string methods """
        token = "Token is %r" % self.bob
        self.assertEquals('Token is <Account Bob>',token)

        token = self.bob.__unicode__()
        self.assertEquals('Bob',token)
        
