## UrlAdjust: Url Adjustment Toolkit

### What is it?

UrlAdjust is a Python package that help developer generate get http request url with template and adjustment info. It aims to simplify the url generation process for get http request url. 

### Main Features

Parse template url and update the get request url with the adjustment info.

Allow user to provide higher order function to modify multiple key value pairs matching the same regular expression pattern.

### Where to get it

```python
pip install urlAdjust==<version>
```
example:
```python
pip install urlAdjust==0.1.0
```

### How to use it

```python

Python 3.9.6 (default, Feb  3 2024, 15:58:27) 
[Clang 15.0.0 (clang-1500.3.9.4)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from url_adjust import url
>>> aws_url = url.Url('https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc')
>>> str(aws_url)
'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc'
>>> aws_url.add_or_update_query_param("newkey", "newvalue")
>>> str(aws_url)
'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc&newkey=newvalue'

```

### Dependencies

- Python (>= 3.9)

### License

- MIT
