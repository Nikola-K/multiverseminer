#
#from mock import MagicMock, Mock
#from authomatic import Authomatic
#from flask.ext.testing import TestCase
#
#from mm import app, db, login
#import mm
#from mm.models import Item, Account, Character, Ingredient, Inventory, Planet, PlanetLoot, RecipeBook
#
#
#class MmTestCase(TestCase):
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
#
#        db.drop_all()
#        db.create_all()
#        app.testing = True
#
#        # create items and recipes
#        refinery = Item(id='refinery', name='Refinery')
#        earth = Planet(id='earth', name='Earth')
#
#        # create account, character and inventory
#        self.oldauth = mm.login.authomatic
#        result = Mock()
#        result.user = Mock()
#        result.user.update = MagicMock()
#        result.user.name = 'bob dole'
#        result.user.id = '123123123'
#        result.user.provider = 'google'
#        result.user.email = 'foo@bar.com'
#        self.bob = Account(oauth_id=result.user.id, realname=result.user.name, email=result.user.email, username=result.user.id)
#        self.conan = Character(name="Conan")
#        self.bob.character=self.conan
#        db.session.add(self.bob)
#
#        db.session.commit()
#        mm.login.authomatic = Mock(Authomatic)
#        mm.login.authomatic.login = MagicMock(return_value=result)
#        self.app = app.test_client()
#        response = self.app.get("/login/google/")
#        self.assertTemplateUsed('index.html')
#        self.assertIn('Welcome back, bob dole.', response.data)
#
#    def tearDown(self):
#        """ clean up after ourselves. """
#        mm.db.session.rollback()
#        mm.db.session.close()
#        mm.db.drop_all()
#        mm.login.authomatic = self.oldauth
#
#
#    def test_index_route(self):
#        """ test the primary route """
#        response = self.app.get("/")
#        self.assertTemplateUsed('index.html')
#        self.assertIn('text/javascript', response.data)
#        self.assert200(response)
#
#    def test_logout_route(self):
#        """ test the logout route """
#        response = self.app.get("/logout")
#        self.assertTemplateUsed('index.html')
#        self.assertIn('Log in', response.data, "Verify logged out.")
#        self.assert200(response)
#
#    def test_favicon_route(self):
#        """ make sure our favicon is being returned """
#        response = self.app.get("/favicon.ico")
#        self.assert200(response)
#
#    def test_404_route(self):
#        """ check the 404 page """
#        response = self.app.get("/404shouldbehere")
#        self.assert404(response)
#
#    def test_collect_valid_type(self):
#        """ collect a valid mine type """
#        response = self.app.get("/collect/mine")
#        self.assertIn('success', response.data)
#
#    def test_collect_invalid_type(self):
#        """ collect invalid type """
#        response = self.app.get("/collect/mined")
#        self.assertIn('failure', response.data)
#        self.assertIn("Invalid collection type.", response.data)
#
