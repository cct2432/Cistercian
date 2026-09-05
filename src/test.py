import unittest

class TestCistercianNumerals(unittest.TestCase):
    
    def test_round_trip_all_numbers(self):
        """Verify that encoding and decoding every number from 0 to 9999 is lossless."""
        for n in range(10000):
            with self.subTest(n=n):
                svg_output = to_cis(n)
                recovered_number = from_cis(svg_output)
                self.assertEqual(
                    recovered_number, 
                    n, 
                    f"Round-trip failed for {n}. Got {recovered_number} back."
                )

    def test_edge_cases_and_bounds(self):
        """Test boundary limits and invalid inputs for to_cis."""
        # Valid boundaries
        self.assertEqual(from_cis(to_cis(0)), 0)
        self.assertEqual(from_cis(to_cis(9999)), 9999)

        # Out of bounds values
        with self.assertRaises(ValueError):
            to_cis(10000)
        with self.assertRaises(ValueError):
            to_cis(-1)

        # Invalid types (including booleans which subclass int in Python)
        with self.assertRaises(TypeError):
            to_cis(123.45)
        with self.assertRaises(TypeError):
            to_cis("1234")
        with self.assertRaises(TypeError):
            to_cis(True)

    def test_invalid_parser_input(self):
        """Test that from_cis rejects non-string inputs."""
        with self.assertRaises(TypeError):
            from_cis(1234)

if __name__ == "__main__":
    unittest.main()
