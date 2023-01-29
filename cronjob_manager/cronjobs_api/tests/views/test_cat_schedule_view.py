from unittest import TestCase
from django.test import Client
from django.urls import reverse
import time


class TestCatScheduleView(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_given_valid_2_seconds_when_post_then_200_and_file_is_created_and_contains_cat(self):
        # Arrange
        delay = 2
        file_path = 'cat_file.txt'

        # Act
        response = self.client.post(reverse('cronjobs_api:cat_schedule'), data={'delay': delay})

        # Assert
        self.assertEqual(response.status_code, 200)
        time.sleep(4)
        with open(file_path, 'r') as file:
            self.assertEqual(file.read(), "cat\n")
