import pytest

from django.core.urlresolvers import reverse
from django.test import TestCase


@pytest.mark.django_db
class RecordListViewTests(TestCase):
    """Tests for the RecordListView"""

    def setUp(self):
        self.url = reverse('record_list')

    def test_get(self):
        """Test the RecordListView get method"""
        response = self.client.get(self.url)

        # Test response code and used template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('temperature/record_list.html')
