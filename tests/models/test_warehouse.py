
import mm

from flask.ext.testing import TestCase
from datetime import datetime
from mm.models import Item, Character, Planet, Warehouse
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

        self.earth = Planet(id='earth', name='Earth')
        mm.db.session.add(self.earth)

        self.ironore = Item(name='Iron Ore', id='ironore')
        mm.db.session.add(self.ironore)

        self.warehouse=Warehouse(item=self.ironore, character=self.conan, planet=self.earth)
        mm.db.session.add(self.warehouse)

        mm.db.session.commit()

    def teardown(self):
        """ """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.db.dispose()

    def test_warehouse_strings(self):
        """ validate warehouse strings """
        self.assertEquals("<Warehouse 1 ironore for Conan on earth>", self.warehouse.__repr__())
        self.assertEquals("<Warehouse 1 ironore for Conan on earth>", self.warehouse.__unicode__())

    def test_warehouse_relationships(self):
        """ validate warehouse relationships """
        # WARNING, this is fragile...
        self.assertEquals(self.conan, self.warehouse.character)
        self.assertEquals(self.ironore, self.warehouse.item)
        self.assertEquals(self.earth, self.warehouse.planet)



