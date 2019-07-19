import unittest
from unittest.mock import MagicMock
import pandas_sample as t
import pandas
from pandas.util.testing import assert_frame_equal


class VouchersTest(unittest.TestCase):
    ORDERS = pandas.DataFrame({'order_id': pandas.Series(
        [1., 2., 3.]), 'customer_id': pandas.Series([4., 5., 6.])})

    BARCODES = pandas.DataFrame({'barcode': pandas.Series(
        [1., 2., 3., 4.]), 'order_id': pandas.Series([1., 3., 2., 1.])})

    SUMMARY = pandas.DataFrame({'order_id': pandas.Series(
        [1., 1., 2., 3.]), 'customer_id': pandas.Series([4., 4., 5., 6.]), 'barcode': pandas.Series([1., 4., 3., 2.])})

    GROUPED = pandas.DataFrame({'customer_id': pandas.Series([4., 5., 6.]), 'order_id': pandas.Series(
        [1., 2., 3.]), 'barcodes': pandas.Series([[1., 4.], [3.], [2.]])})

    TOP5_CUSTOMERS = pandas.DataFrame({'customer_id': pandas.Series(
        [4., 5., 6.]), 'total_tickets': pandas.Series([2, 1, 1])})

    def test_read_orders(self):
        '''
        read_csv in read_orders should be called with correct csv file
        and shoud return expected results
        '''
        read_orders_data = self.ORDERS
        pandas.read_csv = MagicMock(return_value=read_orders_data)
        result = t.read_orders()
        pandas.read_csv.assert_called_with('data/orders.csv')
        assert_frame_equal(result, read_orders_data)

    def test_read_barcodes(self):
        '''
        read_csv in read_barcodes should be called with correct csv file
        and shoud return expected results
        '''
        read_barcodes_data = self.BARCODES
        pandas.read_csv = MagicMock(return_value=read_barcodes_data)
        result = t.read_unique_barcodes()
        pandas.read_csv.assert_called_with('data/barcodes.csv')
        assert_frame_equal(result, read_barcodes_data)

    def test_join_datasets(self):
        '''
        join_datasets should return expected merged result
        '''
        result = t.join_datasets(self.ORDERS, self.BARCODES)
        assert_frame_equal(result, self.SUMMARY)

    def test_groupby_summary(self):
        '''
        groupby_summary should return expected grouped result
        '''
        result = t.groupby_summary(self.SUMMARY)
        assert_frame_equal(result, self.GROUPED)

    def test_get_top5_customers(self):
        '''
        get_top5_customers should return expected top 5 customers
        '''
        result = t.get_top5_customers(self.SUMMARY)
        assert_frame_equal(result, self.TOP5_CUSTOMERS)

    def test_get_unused_barcodes(self):
        '''
        get_unused_barcodes should return total 0 (zero) amount of unused barcodes
        '''
        result = t.get_unused_barcodes(self.BARCODES)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
