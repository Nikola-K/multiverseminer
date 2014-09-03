
from mock import MagicMock, Mock
from unittest import TestCase

from mm.exceptions import CraftingException


class TestLogin(TestCase):

    def setUp(self):
        """ """
        self.message='test Exception'
        self.craftexc=CraftingException(self.message)

    def tearDown(self):
        """ clean up after ourselves. """

    def test_craftException(self):
        """ successfully test CraftingException """
        self.assertEquals(self.message, self.craftexc.message)
        self.assertEquals(self.message, "%s" % self.craftexc)


