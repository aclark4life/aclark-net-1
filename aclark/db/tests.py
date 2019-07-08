from django.test import TestCase
from aclark.db.models import SiteConfiguration

# Create your tests here.

from django.test import TestCase

# class SiteConfiguration(SingletonModel):
# class BaseModel(models.Model):
# class Client(BaseModel):
# class Contact(BaseModel):
# class Estimate(BaseModel):
# class Invoice(BaseModel):
# class Note(BaseModel):
# class Profile(BaseModel):
# class Project(BaseModel):
# class Report(BaseModel):
# class Testimonial(BaseModel):
# class Task(BaseModel):
# class Time(BaseModel):


class SiteConfigurationTestCase(TestCase):
    def setUp(self):
        self.config = SiteConfiguration.get_solo()

    def test_config(self):
        """
        """
        self.assertEqual(self.config.company_name, "Company Name")
        self.assertEqual(self.config.site_name, "Site Name")
