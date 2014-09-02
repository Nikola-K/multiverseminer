from mock import MagicMock, Mock
from authomatic import Authomatic
from flask.ext.testing import TestCase

from mm import app, db, login
import mm
from mm.models import Item, Account, Character, Ingredient, Inventory, Planet, PlanetLoot, RecipeBook


def setup_user(abb, db):
    # create items and recipes
    gold = Item(id='gold', name='Gold')
    ironore = Item(id='ironOre', name='Iron Ore')
    ironbar = Item(id='ironBar', name='Iron Bar')
    refinery = Item(id='refinery', name='Refinery')
    earth = Planet(id='earth', name='Earth')

    oldauth = mm.login.authomatic
    result = Mock()
    result.user = Mock()
    result.user.update = MagicMock()
    result.user.name = 'bob dole'
    result.user.id = '123123123'
    result.user.provider = 'google'
    result.user.email = 'foo@bar.com'
    bob = Account(oauth_id=result.user.id, realname=result.user.name, email=result.user.email, username=result.user.id)
    conan = Character(name="Conan")
    bob.character=conan
    db.session.add(gold)
    db.session.add(ironore)
    db.session.add(ironbar)
    db.session.add(refinery)
    db.session.add(Ingredient(item=ironore, recipe=ironbar, amount=5))
    db.session.add(Ingredient(item=ironbar, recipe=refinery, amount=1))
    db.session.add(RecipeBook(character=conan, item=ironbar))
    db.session.add(bob)
    db.session.add(Inventory(character=conan, item=ironore, amount=200))
    db.session.add(Inventory(character=conan, item=ironbar, amount=1))
    db.session.add(Inventory(character=conan, item=gold, amount=200))
    db.session.add(earth)
    db.session.add(PlanetLoot(planet=earth, item=gold, droprate=.1))
    db.session.add(PlanetLoot(planet=earth, item=ironore, droprate=.1))
    db.session.commit()
    mm.login.authomatic = Mock(Authomatic)
    mm.login.authomatic.login = MagicMock(return_value=result)
    return oldauth
