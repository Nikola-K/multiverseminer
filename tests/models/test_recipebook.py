
import mm

from flask.ext.testing import TestCase
from datetime import datetime
from mm.models import Item, Ingredient, Character, Account, Planet, RecipeBook
from mock import Mock, MagicMock, patch
from config import TestConfiguration
from mm.exceptions import CraftingException

class TestIngredient(TestCase):
    """ Ensure that the ingredient is functioning."""

    def create_app(self):
        """ """
        mm.app.config.from_object('config.TestConfiguration')
        return mm.app

    def setUp(self):
        """ """
        mm.db.drop_all()
        mm.db.create_all()

        self.conan = Character(name='Conan')
        mm.db.session.add(self.conan)

        self.ironore = Item(name='Iron Ore', id='ironore')
        mm.db.session.add(self.ironore)

        self.recipe=RecipeBook(item=self.ironore, character=self.conan)
        mm.db.session.add(self.recipe)

        mm.db.session.commit()

    def teardown(self):
        """ """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.db.dispose()

    def test_recipebook_strings(self):
        """ validate recipebook strings """
        self.assertEquals("<Recipe for ironore owned by Conan>", self.recipe.__repr__())
        self.assertEquals("<Recipe for ironore owned by Conan>", self.recipe.__unicode__())

    def test_inventory_relationships(self):
        """ validate inventory relationships """
        # WARNING, this is fragile...
        self.assertEquals(self.conan, self.recipe.character)
        self.assertEquals(self.ironore, self.recipe.item)


