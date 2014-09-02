
import mm

from flask.ext.testing import TestCase

from mm.models import Account, Character, Planet
from mock import Mock
from config import TestConfiguration

class TestAccount(TestCase):
    """ Ensure that the account is functioning."""

    def create_app(self):
        """ """
        mm.app.config.from_object('config.TestConfiguration')
        return mm.app

    def setUp(self):
        """ """
        mm.db.drop_all()
        mm.db.create_all()
        self.bob = Account(username='Bob', oauth_id='111', email='bob@bob.com', provider='google', realname='bob')
        mm.db.session.add(self.bob)
        self.earth = Planet(name='Earth', id='earth')
        mm.db.session.add(self.earth)
        self.bob.planet=self.earth

        # added to bob
        self.conan = Character(name='Conan', account=self.bob)
        mm.db.session.add(self.conan)
        # non-added
        self.beowulf = Character(name='Beowulf')
        mm.db.session.add(self.beowulf)

        mm.db.session.commit()

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

        self.assertEquals(self.bob.character, self.conan)
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
        

