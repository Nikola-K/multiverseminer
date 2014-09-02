
import mm

from flask.ext.testing import TestCase
from datetime import datetime
from mm.models.character import randint
from mm.models import Item, Category
from mock import Mock, MagicMock, patch
from config import TestConfiguration
from mm.exceptions import CraftingException

class TestCategory(TestCase):
    """ Ensure that the category is functioning."""

    def create_app(self):
        """ """
        mm.app.config.from_object('config.TestConfiguration')
        return mm.app

    def setUp(self):
        """ """
        mm.db.drop_all()
        mm.db.create_all()

        self.consumable=Category(id='consumables', name='Consumables')
        mm.db.session.add(self.consumable)
        self.food=Category(id='food', name='Food')
        self.food.parent=self.consumable
        mm.db.session.add(self.food)
        self.potion=Category(id='potion', name='Potion', parent=self.consumable)
        mm.db.session.add(self.potion)
        mm.db.session.commit()

    def teardown(self):
        """ """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.db.dispose()

    def test_category_strings(self):
        """ validate category strings """
        self.assertEquals("<Category u'Food'>", self.food.__repr__())
        self.assertEquals("Food", self.food.__unicode__())

    def test_category_parents(self):
        """ validate category relationships """
        self.assertEquals(None, self.consumable.parent)
        self.assertEquals([self.food, self.potion], self.consumable.children)
        self.assertEquals(self.consumable, self.food.parent)
        self.assertEquals(self.consumable, self.potion.parent)


