
from mock import MagicMock, Mock
from authomatic import Authomatic
from flask.ext.testing import TestCase

import mm
from mm import app, session
from mm.models import Item, Account, Character, Ingredient, Inventory, RecipeBook, Planet, PlanetLoot


class TestAccount(TestCase):

    def create_app(self):
        """ This app config will be overlayed on the normal config
            allowing us to use a sqlite db for unit tests. """
        app.config.from_object('config.TestConfiguration')
        return app

    def setUp(self):
        """ Since the DB is stored in memory for the duration,
            we need to repopulate it and add it to self. """
        mm.db.drop_all()
        mm.db.create_all()
        app.testing = True

        ironore = Item(id='ironOre', name='Iron Ore')
        mm.db.session.add(ironore)

        self.oldauth = mm.login.authomatic
        result = Mock()
        result.user = Mock()
        result.user.update = MagicMock()
        result.user.name = 'bob dole'
        result.user.id = '123123123'
        result.provider.name = 'google'
        result.user.email = 'foo@bar.com'
        self.bob = Account(oauth_id=result.user.id, realname=result.user.name, email=result.user.email, username=result.user.id, provider=result.provider.name)
        self.conan = Character(name="Conan", account=self.bob)
        mm.db.session.add(self.bob)
        mm.db.session.add(self.conan)

        mm.db.session.commit()

        mm.login.authomatic = Mock(Authomatic)
        mm.login.authomatic.login = MagicMock(return_value=result)

        self.app = app.test_client()
        response = self.app.get("/login/google/")
        self.assertTemplateUsed('index.html')
        self.assertIn('Welcome back, bob dole.', response.data)


    def tearDown(self):
        """ clean up after ourselves. """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.login.authomatic = self.oldauth


    def test_get_character_inventory(self):
        """ successfully craft one valid item """
        response = self.app.get("/character/inventory")
        self.assertIn('success', response.data)
        self.assertIn('Current Inventory', response.data)
        self.assertNotIn('Iron Ore', response.data)

        ironore=Item(id='ironore', name='Iron Ore')
        mm.db.session.add(ironore)
        self.conan.adjust_inventory(ironore, 2)

        response = self.app.get("/character/inventory")
        self.assertIn('success', response.data)
        self.assertIn('Current Inventory', response.data)
        self.assertIn('Iron Ore', response.data)


    def test_craft_with_no_recipe(self):
        """ successfully craft one valid item """
#        response = self.app.get("/craft/refinery/1")
#        self.assertIn('failure', response.data)
#        self.assertIn("You don't have the refinery recipe!", response.data)


