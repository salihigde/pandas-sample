from __future__ import print_function
import pandas
import math
import sys

def read_orders():
    return pandas.read_csv('data/orders.csv')


def read_unique_barcodes():
    barcodes = pandas.read_csv('data/barcodes.csv')
    duplicates = get_duplicate_barcodes(barcodes)
    if not duplicates.empty:
        eprint('\n----------------WARNING--------------------')
        eprint('Ignored duplicate barcodes can be found below')
        eprint(duplicates)
        return clear_duplicate_barcodes(barcodes)
    else:
        return barcodes


def join_datasets(orders, barcodes):
    '''
    joins two of the csv files.
    drops orders without barcodes, if any
    '''
    summary = pandas.merge(orders, barcodes, how='left', on='order_id')
    summary_without_barcodes = summary.dropna()

    if not summary.equals(summary_without_barcodes):
        eprint('\n\n------------WARNING----------------')
        eprint('Orders without barcodes will be ignored')
        return summary_without_barcodes
    else:
        return summary


def groupby_summary(summary):
    '''
    gets a list like order_id, customerid, [barcode1, barcode2]
    '''
    return summary.groupby(['customer_id', 'order_id'])[
        'barcode'].apply(list).reset_index(name='barcodes')


def get_top5_customers(summary):
    '''
    gets top 5 customers that bought most amount of tickets
    '''
    return summary.groupby(['customer_id'])['barcode'].count().nlargest(5).reset_index(name='total_tickets')


def get_unused_barcodes(barcodes):
    '''
    gets amount of unused barcodes
    '''
    return barcodes.isnull().sum().sum()


def get_duplicate_barcodes(barcodes):
    '''
    uses groupby to filter the duplicate rows from the barcodes table
    '''
    return barcodes.groupby(['barcode']).filter(lambda x: len(x) > 1)


def clear_duplicate_barcodes(barcodes):
    '''
    clears duplicate barcode numbers (if any)
    '''
    return barcodes.drop_duplicates(subset='barcode', keep='first')


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


if __name__ == "__main__":
    orders = read_orders()
    barcodes = read_unique_barcodes()
    summary = join_datasets(orders, barcodes)

    grouped_summary = groupby_summary(summary)
    top5_summary = get_top5_customers(summary)
    unused_barcodes = get_unused_barcodes(barcodes)

    print('\n---------Grouped Summary-----------')
    print(grouped_summary)

    print('\n---------Top 5 Customers-----------')
    print(top5_summary)

    print('\n-------Total Unused Barcodes-------')
    print(unused_barcodes)
