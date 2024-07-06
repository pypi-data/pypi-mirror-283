import unittest
import url_adjust.url as url

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_url_decode_and_encode(self):
        url_example = 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc'
        parsed_url = url.Url(url_example)
        self.assertEqual(str(parsed_url), url_example)


    def test_adding_url_query_params(self):
        url_example = 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc'
        parsed_url = url.Url(url_example)
        parsed_url.add_or_update_query_param('new_key', 'new_value')
        self.assertEqual(str(parsed_url), 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc&new_key=new_value')


    def test_updating_url_query_params(self):
        url_example = 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc'
        parsed_url = url.Url(url_example)
        parsed_url.add_or_update_query_param('aws-products-all.sort-order', 'desc')
        self.assertEqual(str(parsed_url),
                         'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=desc')


    def test_update_all_url_query_params_matching(self):
        url_example = 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc'
        parsed_url = url.Url(url_example)
        parsed_url.update_all_query_params_matching('aws-products-all.*', lambda k, v: 'desc')
        self.assertEqual(str(parsed_url),
                         'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=desc&aws-products-all.sort-order=desc')


    def test_deleting_url_query_params(self):
        url_example = 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc'
        parsed_url = url.Url(url_example)
        parsed_url.remove_query_param('aws-products-all.sort-order')
        self.assertEqual(str(parsed_url),
                         'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase')

    def test_deleting_all_url_query_params(self):
        url_example = 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc'
        parsed_url = url.Url(url_example)
        parsed_url.remove_all_query_params()
        self.assertEqual(str(parsed_url), 'https://aws.amazon.com/cn/what-is/blockchain/')

    def test_deleting_all_url_query_params_except(self):
        url_example = 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc'
        parsed_url = url.Url(url_example)
        parsed_url.remove_all_query_params_except(['aws-products-all.sort-order'])
        self.assertEqual(str(parsed_url), 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-order=asc')

    def test_deleting_all_url_query_params_matching(self):
        url_example = 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc'
        parsed_url = url.Url(url_example)
        parsed_url.remove_all_query_params_matching('aws-products-all.*')
        self.assertEqual(str(parsed_url), 'https://aws.amazon.com/cn/what-is/blockchain/')

    def test_deleting_all_url_query_params_not_matching(self):
        url_example = 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc'
        parsed_url = url.Url(url_example)
        parsed_url.remove_all_query_params_not_matching('aws-products-all.*')
        self.assertEqual(str(parsed_url), 'https://aws.amazon.com/cn/what-is/blockchain/?aws-products-all.sort-by=item.additionalFields.productNameLowercase&aws-products-all.sort-order=asc')

if __name__ == '__main__':
    unittest.main()
