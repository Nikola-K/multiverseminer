
import mm

from flask.ext.testing import TestCase
from datetime import datetime
from mm.models.character import randint
from mm.models import Item, Planet, PlanetLoot
from mock import Mock, MagicMock, patch
from config import TestConfiguration
from mm.exceptions import CraftingException

class TestPlanetLoot(TestCase):
    """ Ensure that the planetloot is functioning."""

    def create_app(self):
        """ """
        mm.app.config.from_object('config.TestConfiguration')
        return mm.app

    def setUp(self):
        """ """
        mm.db.drop_all()
        mm.db.create_all()

        self.tinore = Item(name='tin Ore', id='tinore')
        mm.db.session.add(self.tinore)

        self.copperore = Item(name='copper Ore', id='copperore')
        mm.db.session.add(self.copperore)

        self.earth=Planet(id='earth', name='Earth')
        mm.db.session.add(self.earth)
        
        self.tinloot = PlanetLoot(item=self.tinore, planet=self.earth, droprate=0.1)
        mm.db.session.add(self.tinloot)
        self.copperloot = PlanetLoot(item=self.copperore, planet=self.earth, droprate=0.1)
        mm.db.session.add(self.copperloot)
        

        mm.db.session.commit()

    def teardown(self):
        """ """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.db.dispose()

    def test_ingredient_strings(self):
        """ validate ingredient strings """
        self.assertEquals("<PlanetLoot 0.1 copperore on earth>", self.copperloot.__repr__())
        self.assertEquals("copperore on earth", self.copperloot.__unicode__())

    def test_ingredient_relationships(self):
        """ validate ingredient relationships """
        # WARNING, this is fragile...
        self.assertEquals(self.copperloot, self.earth.loot[0])
        self.assertEquals(self.copperloot, self.copperore.found_on[0])
