
import mm

from flask.ext.testing import TestCase
from datetime import datetime
from mm.models.character import randint
from mm.models import Item, Ingredient, Character, Account, Planet
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

        self.tinore = Item(name='tin Ore', id='tinore')
        mm.db.session.add(self.tinore)
        self.tinbar = Item(name='Tin Bar', id='tinbar')
        mm.db.session.add(self.tinbar)

        self.copperore = Item(name='copper Ore', id='copperore')
        mm.db.session.add(self.copperore)
        self.copperbar = Item(name='Copper Bar', id='copperbar')
        mm.db.session.add(self.copperbar)

        self.coppersword = Item(name='Copper Sword', id='coppersword')
        mm.db.session.add(self.coppersword)
        self.coppershield = Item(name='Copper Shield', id='coppershield')
        mm.db.session.add(self.coppershield)

        self.bronzebar = Item(name='Bronze Bar', id='bronzebar')
        mm.db.session.add(self.bronzebar)

        mm.db.session.add(Ingredient(item=self.tinore, recipe=self.tinbar, amount=1))
        mm.db.session.add(Ingredient(item=self.copperore, recipe=self.copperbar, amount=1))

        mm.db.session.add(Ingredient(item=self.copperbar, recipe=self.coppersword, amount=4))
        mm.db.session.add(Ingredient(item=self.copperbar, recipe=self.coppershield, amount=4))

        mm.db.session.add(Ingredient(item=self.tinbar, recipe=self.bronzebar, amount=1))
        mm.db.session.add(Ingredient(item=self.copperbar, recipe=self.bronzebar, amount=1))


        mm.db.session.commit()

    def teardown(self):
        """ """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.db.dispose()

    def test_ingredient_strings(self):
        """ validate ingredient strings """
        self.assertEquals("<Ingredient 1 copperore for copperbar>", self.copperbar.ingredients[0].__repr__())
        self.assertEquals("<Ingredient for copperbar>", self.copperbar.ingredients[0].__unicode__())

    def test_ingredient_relationships(self):
        """ validate ingredient relationships """
        # WARNING, this is fragile...
        self.assertEquals(self.bronzebar, self.copperbar.used_in[2].recipe)
        self.assertEquals(self.copperore, self.copperbar.ingredients[0].item)

    def test_ingredient_equality(self):
        """ validate ingredient relationships """
        self.assertNotEquals(self.bronzebar.ingredients[0], self.bronzebar.ingredients[1])
        self.assertNotEquals(self.coppershield.ingredients[0], self.coppersword.ingredients[0])
