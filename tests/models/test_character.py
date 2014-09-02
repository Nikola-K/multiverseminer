
import mm

from flask.ext.testing import TestCase
from datetime import datetime
from mm.models.character import randint
from mm.models import Account, Character, Planet, PlanetLoot, Item, RecipeBook, Inventory, Ingredient
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
        self.bob = Account(username='Bob', oauth_id='111', email='bob@bob.com', provider='google', realname='bob')
        mm.db.session.add(self.bob)
        self.earth = Planet(name='Earth', id='earth')
        mm.db.session.add(self.earth)
        self.bob.planet=self.earth

        # added to bob
        self.conan = Character(name='Conan', account=self.bob)
        mm.db.session.add(self.conan)
        # non-added
        self.beowulf = Character(name='Beowulf')
        mm.db.session.add(self.beowulf)
        
        self.ironore = Item(name='Iron Ore', id='ironore')
        mm.db.session.add(self.ironore)
        self.ironbar = Item(name='Iron Bar', id='ironbar')
        mm.db.session.add(self.ironbar)
        self.refinery = Item(name='Refinery', id='refinery')
        mm.db.session.add(self.refinery)
        self.ironsword = Item(name='ironsword', id='ironsword')
        mm.db.session.add(self.ironsword)


        mm.db.session.add(Ingredient(item=self.ironore, recipe=self.ironbar, amount=5))
        mm.db.session.add(Ingredient(item=self.ironbar, recipe=self.refinery, amount=1))
        mm.db.session.add(Ingredient(item=self.ironbar, recipe=self.ironsword, amount=1))
        mm.db.session.add(Inventory(item=self.ironore, character=self.conan, amount=100))
        mm.db.session.add(RecipeBook(item=self.ironbar, character=self.conan))
        mm.db.session.add(RecipeBook(item=self.ironsword, character=self.conan))
        mm.db.session.commit()
    def teardown(self):
        """ """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.db.dispose()

    def test_character_account(self):
        """ validate character relationship with bob """
        self.beowulf.account=self.bob
        self.assertEquals(self.bob.characters, [self.conan, self.beowulf])

    def test_has_recipe(self):
        """ validate character relationships """
        self.assertTrue(self.conan.has_recipe('ironbar'))
        self.assertFalse(self.conan.has_recipe('chicken nuggets'))

    def test_in_inventory(self):
        """ validate character relationships """
        self.assertTrue(self.conan.in_inventory('ironore'))
        self.assertFalse(self.conan.in_inventory('ironore',10000))
        self.assertFalse(self.conan.in_inventory('chicken nuggets',1))

    def test_character_strings(self):
        """ validate character relationships """
        self.assertEquals(self.conan.__repr__(),"<Character u'Conan'>")
        self.assertEquals(self.conan.__unicode__(),"Conan")

    def test_adjust_inventory_exceptions(self):
        """ validate inventory throws proper exceptions """
        with self.assertRaises(CraftingException) as cm:
            self.conan.adjust_inventory(self.ironore,-1000)
        self.assertEqual('You need -1000 ironore, but have 100', cm.exception.message)

        with self.assertRaises(CraftingException) as cm:
            self.conan.adjust_inventory(self.ironbar,-1000)
        self.assertEqual('Item ironbar not found in inventory??', cm.exception.message)

    def test_adjust_inventory(self):
        """ validate inventory works properly"""
        self.assertEquals(self.conan.adjust_inventory(self.ironore,1),101)
        self.assertEquals(self.conan.adjust_inventory(self.ironore,-10), 91)
        self.assertEquals(self.conan.adjust_inventory(self.ironbar,10), 10)

    def test_craft_item(self):
        """ validate inventory works properly"""
        # test new item
        self.assertFalse(self.conan.in_inventory(self.ironbar.id) )
        self.assertEquals(self.conan.craft_item('ironbar',1),self.ironbar)
        self.assertTrue(self.conan.in_inventory(self.ironbar.id) )
        # test existing item
        self.assertEquals(self.conan.craft_item('ironbar',1),self.ironbar)
        self.assertTrue(self.conan.in_inventory(self.ironbar.id),2 )
    
    def test_craft_item_exceptions(self):
        """ validate crafting throws proper exceptions """

        with self.assertRaises(CraftingException) as cm:
            self.conan.craft_item('ironore')
        self.assertEqual('ironore is a base material and non-craftable.', cm.exception.message)

        with self.assertRaises(CraftingException) as cm:
            self.conan.craft_item('refinery')
        self.assertEqual("You don't have the refinery recipe!", cm.exception.message)

        with self.assertRaises(CraftingException) as cm:
            self.conan.craft_item('chicken nugget')
        self.assertEqual("Item chicken nugget doesn't exist in DB", cm.exception.message)

        with self.assertRaises(CraftingException) as cm:
            self.conan.craft_item('ironsword',2)
        self.assertEqual("cannot craft 2 ironsword without 2 ironbar", cm.exception.message)


    @patch('mm.models.character.randint')
    def test_update_collection(self, randint):
        """ validate successful collections """
        mm.db.session.add(PlanetLoot(planet=self.earth, item=self.ironore, droprate=0.1))

        randint.return_value=10
        self.bob.last_mine=datetime(2005, 7, 14, 12, 30)
        result= self.conan.update_collection('mine')
        self.assertIn('success' ,result.response[0])
        self.assertIn('You found something' ,result.response[0])
        self.assertIn('ironore' ,result.response[0])

        randint.return_value=10000000
        self.bob.last_mine=datetime(2005, 7, 14, 12, 30)
        result= self.conan.update_collection('mine')
        self.assertIn('success' ,result.response[0])
        self.assertIn('nothing found.' ,result.response[0])
        self.assertNotIn('ironore' ,result.response[0])

        self.bob.last_mine=datetime.utcnow()
        result= self.conan.update_collection('mine')
        self.assertIn('success' ,result.response[0])
        self.assertIn('too soon' ,result.response[0])
        self.assertNotIn('ironore' ,result.response[0])

        self.bob.last_mine=datetime.utcnow()
        result= self.conan.update_collection('pillowfight')
        self.assertIn('failure' ,result.response[0])
        self.assertIn('Invalid collection type.' ,result.response[0])
        self.assertNotIn('ironore' ,result.response[0])
        self.assertIn('pillowfight' ,result.response[0])
