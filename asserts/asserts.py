import softest


class Asserts(softest.TestCase):

    def assert_list_items_text(self, items_list, value):

        for stop in items_list:
            self.soft_assert(self.assertEqual, stop.text, value)
            if stop.text != value:
                print("The text is: " + stop.text)
                print("Test failed")
        self.assert_all()

    def assert_item_text(self, item, value):
        self.soft_assert(self.assertEqual, item.text, value)
        if item.text != value:
            print("The text is: " + item.text)
            print("Test failed")
