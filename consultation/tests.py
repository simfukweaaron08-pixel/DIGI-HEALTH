from django.test import TestCase, Client
from django.contrib.auth import get_user_model


class ConsultationModuleTests(TestCase):
    """Tests for consultation module functionality."""

    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()

    def test_consultation_module_exists(self):
        """Test that consultation module is properly configured."""
        from django.apps import apps
        consultation_app = apps.get_app_config('consultation')
        self.assertIsNotNone(consultation_app)

    def test_consultation_module_installation(self):
        """Test that consultation app is in INSTALLED_APPS."""
        from django.conf import settings
        self.assertIn('consultation', settings.INSTALLED_APPS)

    def test_consultation_models_import(self):
        """Test that consultation models can be imported."""
        try:
            from consultation.models import *  # noqa
            self.assertTrue(True)
        except ImportError:
            self.fail("Consultation models cannot be imported")
