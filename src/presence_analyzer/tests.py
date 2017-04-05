# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
import os.path
import json
import datetime
import unittest


from presence_analyzer import main, views, utils


TEST_DATA_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.csv'
)


# pylint: disable=maybe-no-member, too-many-public-methods
class PresenceAnalyzerViewsTestCase(unittest.TestCase):
    """
    Views tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})
        self.client = main.app.test_client()

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_mainpage(self):
        """
        Test main page redirect.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        assert resp.headers['Location'].endswith('/presence_weekday.html')

    def test_api_users(self):
        """
        Test users listing.
        """
        resp = self.client.get('/api/v1/users')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)
        self.assertDictEqual(data[0], {u'user_id': 10, u'name': u'User 10'})


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """
    Utility functions tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_get_data(self):
        """
        Test parsing of CSV file.
        """
        data = utils.get_data()
        self.assertIsInstance(data, dict)
        self.assertItemsEqual(data.keys(), [10, 11])
        sample_date = datetime.date(2013, 9, 10)
        self.assertIn(sample_date, data[10])
        self.assertItemsEqual(data[10][sample_date].keys(), ['start', 'end'])
        self.assertEqual(
            data[10][sample_date]['start'],
            datetime.time(9, 39, 5)
        )

    def test_seconds_since_midnight_return_correct_time(self):
        midnight_time = datetime.time(0, 0, 0)
        second_after_midnight = datetime.time(0, 0, 1)
        minute_after_midnight = datetime.time(0, 1, 0)
        hour_after_midnight = datetime.time(1, 0, 0)
        self.assertEqual(utils.seconds_since_midnight(midnight_time), 0)
        self.assertEqual(utils.seconds_since_midnight(second_after_midnight), 1)
        self.assertEqual(utils.seconds_since_midnight(minute_after_midnight), 60)
        self.assertEqual(utils.seconds_since_midnight(hour_after_midnight), 3600)

    def test_interval_returns_correct_interval(self):
        start = datetime.time(0, 0, 0)
        stop = datetime.time(1, 1, 1)
        self.assertEqual(utils.interval(start, stop), 3661)

    def test_mean_returns_zero_for_empty_list(self):
        self.assertEqual(utils.mean([]), 0)

    def test_mean_within_1_percent_accuracy_for_non_empty_list(self):
        items = [1, 2]
        self.assertAlmostEqual(utils.mean(items), 1.5, 3)


def suite():  # pragma: no cover
    """
    Default test suite.
    """
    base_suite = unittest.TestSuite()
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerViewsTestCase))
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerUtilsTestCase))
    return base_suite


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
