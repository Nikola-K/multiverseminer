
import mm

from flask.ext.testing import TestCase
from datetime import datetime
from mm.models import Account, Planet

from mock import Mock, MagicMock, patch

from mm.admin import BaseAdmin

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
        mm.db.session.commit()

    def teardown(self):
        """ """
        mm.db.session.rollback()
        mm.db.session.close()
        mm.db.drop_all()
        mm.db.dispose()

    def test_baseadmin_accssible_logged_out(self):
        """ validate admin page """
        adminpage=BaseAdmin(Planet,mm.db.session).is_accessible()
        self.assertFalse(BaseAdmin(Planet,mm.db.session).is_accessible())

    def test_baseadmin_accssible_logged_in_no_oauth(self):
        """ validate admin page """
        adminpage=BaseAdmin(Planet,mm.db.session).is_accessible()
        mm.session['logged_in']=True
        self.assertFalse(BaseAdmin(Planet,mm.db.session).is_accessible())

    def test_baseadmin_accssible_logged_in_w_oauth(self):
        """ validate admin page """
        adminpage=BaseAdmin(Planet,mm.db.session).is_accessible()
        mm.session['logged_in']=True
        mm.session['oauth_id']=111
        self.assertFalse(BaseAdmin(Planet,mm.db.session).is_accessible())

    def test_baseadmin_accssible_success(self):
        """ validate admin page """
        adminpage=BaseAdmin(Planet,mm.db.session).is_accessible()
        self.bob.access_level=1
        mm.session['logged_in']=True
        mm.session['oauth_id']=111
        self.assertTrue(BaseAdmin(Planet,mm.db.session).is_accessible())
