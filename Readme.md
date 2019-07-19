Purpose of this project is to collect various pandas library table operations in one place. You may find examples for following operations

**LEFT JOIN**

`pandas.merge(orders, barcodes, how='left', on='order_id')`

**GROUP BY**

**Create list of following format:**

| customer_id | order_id1 | [barcode1, barcode2, ...] 
| customer_id | order_id2 | [barcode1, barcode2, ...]

`joinResult.groupby(['customer_id', 'order_id'])['barcode'].apply(list).reset_index(name='barcodes')`

**Filter duplicate barcodes:**

`barcodes.groupby(['barcode']).filter(lambda x: len(x) > 1)`

**TOP 5 RECORDS**

**Gets top 5 customers who purchased barcodes**

`joinResult.groupby(['customer_id'])['barcode'].count().nlargest(5).reset_index(name='total_tickets')`

**GETTING STARTED**

- Install pandas: `pip install pandas`
- Install MagicMock: `pip install MagicMock`
- Run application: `python pandas-sample.py`
- Run unit tests: `python pandas-sample_unittest.py`


