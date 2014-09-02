
import mm

from flask.ext.testing import TestCase
from datetime import datetime
from mm.models.character import randint
from mm.models import Item, Category, Ingredient
from mock import Mock, MagicMock, patch
from config import TestConfiguration
from mm.exceptions import CraftingException

class TestCharacter(TestCase):
    """ Ensure that the character is functioning."""

    def create_app(self):
        """ """
        mm.app.config.from_object('config.TestConfiguration')
        return mm.app

    def setUp(self):
        """ """
        mm.db.drop_all()
        mm.db.create_all()

        self.copperore = Item(name='copper Ore', id='copperore')
        mm.db.session.add(self.copperore)        
        self.ironore = Item(name='Iron Ore', id='ironore')
        mm.db.session.add(self.ironore)
        self.ironbar = Item(name='Iron Bar', id='ironbar')
        mm.db.session.add(self.ironbar)
        mm.db.session.add(Ingredient(item=self.ironore, recipe=self.ironbar, amount=1))


        mm.db.session.commit()

    def teardown(self):
        """ """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.db.dispose()

    def test_item_category(self):
        """ validate character relationship with bob """
        ores=Category(id='ores', name='Ores')
        self.ironore.category=ores
        self.assertIn(self.ironore, ores.items)
        self.assertEquals(self.ironore.category, ores)

    def test_item_contains(self):
        """ validate item contains()"""
        self.assertFalse(self.ironbar.contains(self.ironbar))
        self.assertTrue(self.ironbar.contains(self.ironore))

    def test_item_equals(self):
        """ validate item equality """
        self.assertEquals(self.ironbar, self.ironore.used_in[0].recipe)
        self.assertNotEquals(self.ironbar, self.ironore)

    def test_item_strings(self):
        """ validate item strings """
        self.assertEquals("<Item u'Iron Bar'>", self.ironbar.__repr__())
        self.assertEquals("Iron Bar", self.ironbar.__unicode__())


