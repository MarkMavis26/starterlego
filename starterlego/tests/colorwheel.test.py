with patch.dict('sys.modules', {
    'pybricks.hubs': MagicMock(),
    'pybricks.ev3devices': MagicMock(),
    'pybricks.parameters': MagicMock(),
    'pybricks.tools': MagicMock(),
}): 
    import sys
    print("Mocked modules:", [k for k in sys.modules if k.startswith('pybricks')])
    from colorwheel import handle_color_action
    import unittest
    from unittest.mock import MagicMock, patch
    print("Python paths:", sys.path)

    class TestColorWheel(unittest.TestCase):
        def test_handle_color_action(self):
            # Example test to ensure handle_color_action can be called
            self.assertTrue(callable(handle_color_action))

    # Test class
    class TestColorActionMap(unittest.TestCase):

        @patch("colorwheel.medium_motor")  # Mock medium_motor
        @patch("builtins.print")  # Mock print
        def test_handle_color_action_yellow(self, mock_print, mock_medium_motor):
            # Arrange
            mock_medium_motor.run_angle.return_value = None

            # Act
            handle_color_action("Color.YELLOW")

            # Assert
            mock_print.assert_called_once_with("Color.YELLOW...counter clockwise!")
            mock_medium_motor.run_angle.assert_called_once_with(500, 360)

    if __name__ == "__main__":
        unittest.main()
