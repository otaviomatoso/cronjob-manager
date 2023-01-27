from unittest import TestCase
from django.test import Client
import time
import os


class TestCatScheduleView(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_cat_schedule_given_valid_request_and_2_seconds_delay_when_post_is_called_then_response_is_200_and_file_is_created_and_contains_cat(self):
        # Arrange
        delay = 2
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'cat_file.txt')

        # Act
        response = self.client.post('/api/cat_schedule/', data={'delay': delay})

        # Assert
        self.assertEqual(response.status_code, 200)
        time.sleep(4)
        with open(file_path, 'r') as file:
            self.assertEqual(file.read(), "cat\n")
