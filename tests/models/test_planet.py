
import mm

from flask.ext.testing import TestCase
from datetime import datetime
from mm.models.character import randint
from mm.models import Planet
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

        self.earth=Planet(id='earth', name='Earth')
        mm.db.session.add(self.earth)

        mm.db.session.commit()

    def teardown(self):
        """ """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.db.dispose()

    def test_ingredient_strings(self):
        """ validate ingredient strings """
        self.assertEquals("<Planet Earth>", self.earth.__repr__())
        self.assertEquals("Earth", self.earth.__unicode__())

