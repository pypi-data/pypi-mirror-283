import unittest
from kataCheckout.kataCheckout import Checkout, Product, Rules

class MyTestCase(unittest.TestCase):
    def setUp(self):
        # setting products
        self.A = Product('A', 50)
        self.B = Product('B', 30)
        self.C = Product('C', 20)
        self.D = Product('D', 15)
        self.F = Product('F', 0)
        # setting rules
        self.rules = {
             'A': Rules(self.A, quantity=3, discount=130),
             'B': Rules(self.B, quantity=2, discount=45),
             'C': Rules(self.C),
             'D': Rules(self.D)
        }
        # Initalize the kataCheckout
        self.checkout = Checkout(self.rules)

    def test_scan_single_item(self):
        self.checkout.scan(self.A)
        self.assertEqual(self.checkout.items[self.A], 1)

    def test_scan_multiple_items(self):
        self.checkout.scan(self.A)
        self.checkout.scan(self.A)
        self.checkout.scan(self.A)
        self.assertEqual(self.checkout.items[self.A], 3)

    def test_total_without_discount(self):
        self.checkout.scan(self.D)
        self.assertEqual(self.checkout.total(), 15)

    def test_total_with_discoutn(self):
        self.checkout.scan(self.A)
        self.checkout.scan(self.A)
        self.checkout.scan(self.A)
        self.assertEqual(self.checkout.total(), 130)

    def test_total_multipled_items(self):
        self.checkout.scan(self.A)
        self.checkout.scan(self.B)
        self.checkout.scan(self.B)
        self.checkout.scan(self.C)
        self.checkout.scan(self.D)
        self.checkout.scan(self.A)
        self.checkout.scan(self.A)
        self.assertEqual(self.checkout.total(), 210)

    def test_total_with_no_passed_items(self):
        self.assertEqual(self.checkout.total(), 0)

    def test_item_not_in_rules_lists(self):
        self.assertEqual(self.checkout.scan(self.F), "Item not in list")

if __name__ == '__main__':
    unittest.main()
