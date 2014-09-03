#
#from mock import MagicMock, Mock
#from authomatic import Authomatic
#from flask.ext.testing import TestCase
#
#from mm import app, session
#import mm
#from mm.models import Item, Account, Character, Ingredient, Inventory, Planet, PlanetLoot, RecipeBook
#
#
#class TestLogin(TestCase):
#
#    def create_app(self):
#        """ This app config will be overlayed on the normal config
#            allowing us to use a sqlite db for unit tests. """
#        app.config.from_object('config.TestConfiguration')
#        return app
#
#    def setUp(self):
#        """ Since the DB is stored in memory for the duration,
#            we need to repopulate it and add it to self. """
#        mm.db.drop_all()
#        mm.db.create_all()
#        app.testing = True
#
#        ironore = Item(id='ironOre', name='Iron Ore')
#        mm.db.session.add(ironore)
#
#        self.oldauth = mm.login.authomatic
#        result = Mock()
#        result.user = Mock()
#        result.user.update = MagicMock()
#        result.user.name = 'bob dole'
#        result.user.id = '123123123'
#        result.provider.name = 'google'
#        result.user.email = 'foo@bar.com'
#        self.bob = Account(oauth_id=result.user.id, realname=result.user.name, email=result.user.email, username=result.user.id, provider=result.provider.name)
#        self.conan = Character(name="Conan", account=self.bob)
#        self.bob.character=self.conan
#        mm.db.session.add(self.bob)
#        mm.db.session.add(self.conan)
#
#        mm.db.session.commit()
#        mm.login.authomatic = Mock(Authomatic)
#        mm.login.authomatic.login = MagicMock(return_value=result)
#        self.app = app.test_client()
#
#
#    def tearDown(self):
#        """ clean up after ourselves. """
#        mm.db.session.rollback()
#        mm.db.session.close()
#        mm.db.drop_all()
#        mm.login.authomatic = self.oldauth
#
#    def test_login_page(self):
#        """ successfully craft one valid item """
#        response = self.app.get("/login")
#        self.assertTemplateUsed('require_login.html')
#
#    def test_provider_bad_return_user_route(self):
#        """ Test a bad user object from provider results."""
#        result = Mock()
#        result.user = False
#
#        mm.login.authomatic.login = MagicMock(return_value=result)
#        response = self.app.get("/login/google/")
#        self.assertTemplateUsed('account.html')
#        self.assertIn('', response.data)
#
#    def test_provider_no_user_name_route(self):
#        """ test a bad user.name from provider results. """
#        result = Mock()
#        result.user = Mock()
#        result.user.update = MagicMock()
#        result.user.name = False
#
#        mm.login.authomatic.login = MagicMock(return_value=result)
#        response = self.app.get("/login/google/")
#        self.assertTemplateUsed('account.html')
#        self.assertIn('There is an issue with your account. Contact us.',
#                      response.data)
#        self.assertStatus(response, 200)
#
#    def test_provider_new_account(self):
#        """ test a new account. """
#        result = Mock()
#        result.user = Mock()
#        result.user.update = MagicMock()
#        result.user.name = 'Joe'
#        result.user.id = 11111111
#        result.provider.name = 'google'
#        result.user.email = 'joe@example.com'
#
#        mm.login.authomatic.login = MagicMock(return_value=result)
#        response = self.app.get("/login/google/")
#        self.assertTemplateUsed('index.html')
#        self.assertIn('Welcome to Multiverse Miner, Joe.', response.data)
#        self.assertStatus(response, 200)
#
#    def test_provider_existing_account(self):
#        """ test an existing account """
#
#        response = self.app.get("/login/google/")
#        self.assertTemplateUsed('index.html')
#        self.assertIn('Welcome back, bob dole.', response.data)
#        self.assertStatus(response, 200)
#
#    def test_provider_without_character(self):
#        """ test an existing account with no character """
#        self.bob.character=None
#        response = self.app.get("/login/google/")
#        self.assertTemplateUsed('index.html')
#        self.assertIn('No character created', response.data)
#        self.assertStatus(response, 200)
#
#
#    def test_provider_borked(self):
#        """ test a new account. """
#        response = self.app.get("/logout")
#        mm.login.authomatic = self.oldauth
#        response = self.app.get("/login/google/")
#        self.assertStatus(response, 302)
#        self.assertIn('accounts.google.com', response.headers[1][1])
#
