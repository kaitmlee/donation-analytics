# -*- coding: utf-8 -*-
import donation_analytics
import unittest

class TestDonationAnalytics(unittest.TestCase):
    def test_find_percentile(self):
        amounts = [1.1, 2.2, 3.5, 4.4, 5]
        percentile = 80
        expected = 4
        actual = donation_analytics.find_percentile(amounts,percentile)
        self.assertEqual(expected, actual)  
    
    def test_find_percentile(self):
        amounts = [1.1, 2.2, 3.5, 4.5, 5]
        percentile = 80
        expected = 5
        actual = donation_analytics.find_percentile(amounts,percentile)
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()
