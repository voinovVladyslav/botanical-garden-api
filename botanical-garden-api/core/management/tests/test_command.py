from unittest.mock import patch

from psycopg2 import OperationalError as OperationalErrorg2

from django.test import SimpleTestCase
from django.db.utils import OperationalError
from django.core.management import call_command


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    def test_wait_for_db_connects_sucessfully(self, patched_check):
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_connects_with_errors(self, patched_sleep, patched_check):
        patched_check.side_effect = [OperationalError] * 2 \
         + [OperationalErrorg2] * 2 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 5)
        patched_check.assert_called_with(databases=['default'])
