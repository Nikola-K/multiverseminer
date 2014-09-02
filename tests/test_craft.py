
from mock import MagicMock, Mock
from authomatic import Authomatic
from flask.ext.testing import TestCase

import mm
from mm import app, db, login, craft
from mm.models import Item, Account, Character, Ingredient, Inventory, RecipeBook, Planet, PlanetLoot
from presets import setup_user


class CraftTestCase(TestCase):

    def create_app(self):
        """ This app config will be overlayed on the normal config
            allowing us to use a sqlite db for unit tests. """
        app.config.from_object('config.TestConfiguration')
        return app

    def setUp(self):
        """ Since the DB is stored in memory for the duration,
            we need to repopulate it and add it to self. """
        db.create_all()
        app.testing = True
        self.oldauth=setup_user(app, db)
        self.app = app.test_client()
        response = self.app.get("/login/google/")
        self.assertTemplateUsed('index.html')
        self.assertIn('Welcome back, bob dole.', response.data)

    def tearDown(self):
        """ clean up after ourselves. """
        # remove the cookie
        db.session.remove()
        # remove the DB.
        db.drop_all()
        mm.login.authomatic = self.oldauth

    def test_craft_one_valid_item(self):
        """ successfully craft one valid item """
        response = self.app.get("/craft/ironBar/1")
        self.assertIn('success', response.data)
        self.assertIn('1 Iron Bar crafted!', response.data)

    def test_craft_with_no_recipe(self):
        """ successfully craft one valid item """
        response = self.app.get("/craft/refinery/1")
        self.assertIn('failure', response.data)
        self.assertIn("You don't have the refinery recipe!", response.data)

    def test_craft_one_invalid_item(self):
        """ fail to craft one invalid item """
        response = self.app.get("/craft/gold/1")
        self.assertIn('failure', response.data)
        self.assertIn("gold is a base material and non-craftable.", response.data)

    def test_craft_one_nonexistant_item(self):
        """ fail to craft one non-existent item """

        response = self.app.get("/craft/fakeitem/1")
        self.assertIn('failure', response.data)
        self.assertIn("Item fakeitem doesn't exist in DB", response.data)

    def test_not_enough_resources(self):
        """ fail to have enough resources """

        response = self.app.get("/craft/ironBar/100")
        self.assertIn('failure', response.data)
        self.assertIn('cannot craft 100 ironBar without 500 ironOre', response.data)
