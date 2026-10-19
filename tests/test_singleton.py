import unittest

from facade.shopping_facade import ShoppingFacade


class ShoppingFacadeSingletonTest(unittest.TestCase):
    def test_calls_return_the_same_instance(self):
        first = ShoppingFacade()
        second = ShoppingFacade()

        self.assertIs(first, second)

    def test_reinitialization_does_not_reset_shared_state(self):
        facade = ShoppingFacade()
        original_next_list_id = facade.next_list_id

        try:
            facade.next_list_id = original_next_list_id + 10

            another_reference = ShoppingFacade()

            self.assertIs(facade, another_reference)
            self.assertEqual(
                another_reference.next_list_id,
                original_next_list_id + 10
            )
        finally:
            facade.next_list_id = original_next_list_id


if __name__ == "__main__":
    unittest.main()
