from django.test import TestCase
from aclark.db.models import SiteConfiguration
from aclark.db.models import BaseModel
from aclark.db.models import Client
from aclark.db.models import Contact
from aclark.db.models import Estimate


class SiteConfigurationTestCase(TestCase):
    def setUp(self):
        self.config = SiteConfiguration.get_solo()

    def test_config(self):
        """
        """
        self.assertEqual(self.config.company_name, "Company Name")
        self.assertEqual(self.config.site_name, "Site Name")


class BaseModelTestCase(TestCase):
    def setUp(self):
        self.base = BaseModel()

    def test_base(self):
        """
        """
        self.assertTrue(self.base.active)
        self.assertFalse(self.base.hidden)


class ClientTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_client(self):
        """
        """
        self.assertFalse(self.client.published)


class ContactTestCase(TestCase):
    def setUp(self):
        self.contact = Contact(first_name="Alex", last_name="Clark")

    def test_contact(self):
        """
        """
        self.assertEqual(self.contact.first_name, "Alex")
        self.assertEqual(self.contact.last_name, "Clark")


class EstimateTestCase(TestCase):
    def setUp(self):
        self.estimate = Estimate(
            subject="Enthusiastically reinvent plug-and-play platforms"
        )

    def test_contact(self):
        """
        """
        self.assertEqual(
            self.estimate.subject, "Enthusiastically reinvent plug-and-play platforms"
        )
