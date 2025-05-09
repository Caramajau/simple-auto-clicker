from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from model.option_handler import OptionHandler


class TestOptionHandler(TestCase):
    def setUp(self) -> None:
        self.__test_path: str = "mock/path/options.json"
    
    @patch("model.option_handler.JSONHandler", autospec=True)
    def test_default_options_loaded_when_file_is_empty(self, mock_json_handler: MagicMock) -> None:
        # Mock JSONHandler to return an empty dictionary
        mock_json_handler_instance: MagicMock = mock_json_handler.return_value
        mock_json_handler_instance.read_json.return_value = {}
        mock_json_handler_instance.write_json = MagicMock()

        option_handler: OptionHandler = OptionHandler(self.__test_path)

        # Assert that default options are loaded
        self.assertEqual(option_handler.get_toggle_recording_key(), "r")
        self.assertEqual(option_handler.get_record_mouse_position_key(), "g")
        self.assertEqual(option_handler.get_clear_recorded_positions_key(), "c")
        self.assertEqual(option_handler.get_start_key(), "j")
        self.assertEqual(option_handler.get_stop_key(), "k")
        self.assertEqual(option_handler.get_delay(), 0.1)

        # Assert that default options are written to the file
        mock_json_handler_instance.write_json.assert_called_once_with(OptionHandler.get_default_options())

    @patch("model.option_handler.JSONHandler")
    def test_custom_options_loaded_from_file(self, mock_json_handler: MagicMock) -> None:
        # Mock JSONHandler to return custom options
        custom_options: dict[str, str | float] = {
            "toggleRecording": "t",
            "recordMousePosition": "m",
            "clearRecordedPosition": "x",
            "start": "s",
            "stop": "e",
            "delay": 0.5
        }
        mock_json_handler_instance: MagicMock = mock_json_handler.return_value
        mock_json_handler_instance.read_json.return_value = custom_options

        option_handler: OptionHandler = OptionHandler(self.__test_path)

        # Assert custom options are loaded
        self.assertEqual(option_handler.get_toggle_recording_key(), "t")
        self.assertEqual(option_handler.get_record_mouse_position_key(), "m")
        self.assertEqual(option_handler.get_clear_recorded_positions_key(), "x")
        self.assertEqual(option_handler.get_start_key(), "s")
        self.assertEqual(option_handler.get_stop_key(), "e")
        self.assertEqual(option_handler.get_delay(), 0.5)

if __name__ == "__main__":
    main()
