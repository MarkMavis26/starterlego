from unittest.mock import MagicMock, patch
import sys
import unittest
from unittest import TestCase
from parameterized import parameterized

sys.modules['pybricks'] = MagicMock()
sys.modules['pybricks.hubs'] = MagicMock()
sys.modules['pybricks.ev3devices'] = MagicMock()
sys.modules['pybricks.parameters'] = MagicMock()
sys.modules['pybricks.tools'] = MagicMock()
from colorwheel import handle_color_action

# to run these:
# python -m tests.test_colorwheel
class TestColorActionMap(TestCase):
    @parameterized.expand([
        ("yellow", "Color.YELLOW", "Color.YELLOW...counter clockwise!", 500, 360),
        ("red", "Color.RED", "Color.RED...clockwise!", 500, -360),
    ])
    @patch("colorwheel.medium_motor")  # Mock medium_motor
    @patch("builtins.print")  # Mock print
    def test_handle_color_action(self, _, color, expected_print, expected_speed, expected_angle, mock_print, mock_medium_motor):
        # Arrange
        mock_medium_motor.run_angle.return_value = None

        # Act
        handle_color_action(color)

        # Assert
        mock_print.assert_called_once_with(expected_print)
        mock_medium_motor.run_angle.assert_called_once_with(expected_speed, expected_angle)

if __name__ == "__main__":
    unittest.main()
