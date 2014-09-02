
import mm

from flask.ext.testing import TestCase
from datetime import datetime
from mm.models import Item, Ingredient, Character, Account, Planet, Inventory
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

        self.inventory=Inventory(item=self.ironore, character=self.conan, amount=100)
        mm.db.session.add(self.inventory)

        mm.db.session.commit()

    def teardown(self):
        """ """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.db.dispose()

    def test_inventory_strings(self):
        """ validate inventory strings """
        self.assertEquals("<Inventory 100 ironore for Conan>", self.inventory.__repr__())
        self.assertEquals("<Inventory 100 ironore for Conan>", self.inventory.__unicode__())

    def test_inventory_relationships(self):
        """ validate inventory relationships """
        # WARNING, this is fragile...
        self.assertEquals(self.conan, self.inventory.character)
        self.assertEquals(self.ironore, self.inventory.item)

