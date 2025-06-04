from typing import Mapping
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from model.option_handler import OptionHandler


class TestOptionHandler(TestCase):
    def setUp(self) -> None:
        self.__test_path: str = "mock/path/options.json"
        self.__option_method_names: Mapping[str, str] = {
            OptionHandler.TOGGLE_RECORDING_KEY: OptionHandler.get_toggle_recording_key.__name__,
            OptionHandler.RECORD_MOUSE_POSITION_KEY: OptionHandler.get_record_mouse_position_key.__name__,
            OptionHandler.CLEAR_RECORDED_POSITIONS_KEY: OptionHandler.get_clear_recorded_positions_key.__name__,
            OptionHandler.START_KEY: OptionHandler.get_start_key.__name__,
            OptionHandler.STOP_KEY: OptionHandler.get_stop_key.__name__,
            OptionHandler.EXIT_KEY: OptionHandler.get_exit_key.__name__,
            OptionHandler.DELAY_KEY: OptionHandler.get_delay.__name__,
        }

    @patch("model.option_handler.JSONHandler", autospec=True)
    def test_default_options_loaded_when_file_is_empty(
        self, mock_json_handler: MagicMock
    ) -> None:
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
        self.assertEqual(option_handler.get_exit_key(), "esc")
        self.assertEqual(option_handler.get_delay(), 0.1)

        # Assert that default options are written to the file
        mock_json_handler_instance.write_json.assert_called_once_with(
            OptionHandler.get_default_options()
        )

    @patch("model.option_handler.JSONHandler")
    def test_custom_options_loaded_from_file(
        self, mock_json_handler: MagicMock
    ) -> None:
        # Mock JSONHandler to return custom options
        custom_options: Mapping[str, str | float] = {
            OptionHandler.TOGGLE_RECORDING_KEY: "t",
            OptionHandler.RECORD_MOUSE_POSITION_KEY: "m",
            OptionHandler.CLEAR_RECORDED_POSITIONS_KEY: "x",
            OptionHandler.START_KEY: "s",
            OptionHandler.STOP_KEY: "e",
            OptionHandler.EXIT_KEY: "esc",
            OptionHandler.DELAY_KEY: 0.5,
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
        self.assertEqual(option_handler.get_exit_key(), "esc")
        self.assertEqual(option_handler.get_delay(), 0.5)

    @patch("model.option_handler.JSONHandler")
    def test_partial_options_fallback_to_default(
        self, mock_json_handler: MagicMock
    ) -> None:
        # Mock JSONHandler to return partial options
        partial_options: Mapping[str, str | float] = {
            OptionHandler.TOGGLE_RECORDING_KEY: "t",
            OptionHandler.DELAY_KEY: 0.2,
        }
        mock_json_handler = mock_json_handler.return_value
        mock_json_handler.read_json.return_value = partial_options

        option_handler = OptionHandler(self.__test_path)

        # Assert changed options
        self.assertEqual(option_handler.get_toggle_recording_key(), "t")
        self.assertEqual(option_handler.get_delay(), 0.2)

        # Assert default options
        self.assertEqual(option_handler.get_record_mouse_position_key(), "g")
        self.assertEqual(option_handler.get_clear_recorded_positions_key(), "c")
        self.assertEqual(option_handler.get_start_key(), "j")
        self.assertEqual(option_handler.get_stop_key(), "k")
        self.assertEqual(option_handler.get_exit_key(), "esc")

    @patch("model.option_handler.JSONHandler")
    def test_single_option_override_fallback_to_default(
        self, mock_json_handler: MagicMock
    ) -> None:
        default_options: Mapping[str, str | float] = OptionHandler.get_default_options()

        override_values: Mapping[str, str | float] = {
            OptionHandler.TOGGLE_RECORDING_KEY: "z",
            OptionHandler.RECORD_MOUSE_POSITION_KEY: "m",
            OptionHandler.CLEAR_RECORDED_POSITIONS_KEY: "x",
            OptionHandler.START_KEY: "s",
            OptionHandler.STOP_KEY: "e",
            OptionHandler.EXIT_KEY: "a",
            OptionHandler.DELAY_KEY: 0.9,
        }

        self.validate_options_override(
            mock_json_handler, default_options, override_values
        )

    def validate_options_override(
        self,
        mock_json_handler: MagicMock,
        default_options: Mapping[str, str | float],
        override_values: Mapping[str, str | float],
    ) -> None:
        for key, override_value in override_values.items():
            with self.subTest(option=key):
                # Only override one option at a time
                self.mock_partial_options(mock_json_handler, key, override_value)

                option_handler = OptionHandler(self.__test_path)

                self.validate_option_override(
                    self.__option_method_names, key, override_value, option_handler
                )

                self.validate_default_options(
                    default_options, self.__option_method_names, key, option_handler
                )

    def mock_partial_options(
        self, mock_json_handler: MagicMock, key: str, override_value: str | float
    ) -> None:
        partial_options: Mapping[str, str | float] = {key: override_value}
        mock_json_handler_instance: MagicMock = mock_json_handler.return_value
        mock_json_handler_instance.read_json.return_value = partial_options

    def validate_option_override(
        self,
        option_method_names: Mapping[str, str],
        key: str,
        override_value: str | float,
        option_handler: OptionHandler,
    ) -> None:
        result = getattr(option_handler, option_method_names[key])()
        self.assertEqual(
            result,
            override_value if key != OptionHandler.DELAY_KEY else float(override_value),
        )

    def validate_default_options(
        self,
        default_options: Mapping[str, str | float],
        option_method_names: Mapping[str, str],
        key: str,
        option_handler: OptionHandler,
    ) -> None:
        for other_key, method in option_method_names.items():
            if other_key == key:
                continue
            self.assert_default_option(
                default_options[other_key], option_handler, other_key, method
            )

    def assert_default_option(
        self,
        expected: str | float,
        option_handler: OptionHandler,
        other_key: str,
        method: str,
    ) -> None:
        result = getattr(option_handler, method)()
        # Ensure type matches for delay
        if other_key == OptionHandler.DELAY_KEY:
            self.assertEqual(result, float(expected))
        else:
            self.assertEqual(result, expected)

    @patch("model.option_handler.JSONHandler")
    def test_ill_formatted_json_fallbacks_to_default(
        self, mock_json_handler: MagicMock
    ) -> None:
        mock_json_handler_instance: MagicMock = mock_json_handler.return_value
        # Simulate an ill-formatted JSON by return an empty dictionary
        mock_json_handler_instance.read_json.return_value = {}
        mock_json_handler_instance.write_json = MagicMock()

        # OptionHandler should handle the exception and use default options
        option_handler = OptionHandler(self.__test_path)

        self.assertEqual(option_handler.get_toggle_recording_key(), "r")
        self.assertEqual(option_handler.get_record_mouse_position_key(), "g")
        self.assertEqual(option_handler.get_clear_recorded_positions_key(), "c")
        self.assertEqual(option_handler.get_start_key(), "j")
        self.assertEqual(option_handler.get_stop_key(), "k")
        self.assertEqual(option_handler.get_exit_key(), "esc")
        self.assertEqual(option_handler.get_delay(), 0.1)

        # Should write default options to file
        mock_json_handler_instance.write_json.assert_called_once_with(
            OptionHandler.get_default_options()
        )

    @patch("model.option_handler.JSONHandler")
    def test_single_option_invalid_keys_entered_fallback_to_default(
        self, mock_json_handler: MagicMock
    ) -> None:
        default_options: Mapping[str, str | float] = OptionHandler.get_default_options()

        override_values: Mapping[str, str | float] = {
            OptionHandler.TOGGLE_RECORDING_KEY: "ze",
            OptionHandler.RECORD_MOUSE_POSITION_KEY: "me",
            OptionHandler.CLEAR_RECORDED_POSITIONS_KEY: "xe",
            OptionHandler.START_KEY: "se",
            OptionHandler.STOP_KEY: "ee",
            OptionHandler.EXIT_KEY: "ae",
        }

        for key, override_value in override_values.items():
            with self.subTest(option=key):
                # Only check one option at a time
                self.mock_partial_options(mock_json_handler, key, override_value)

                option_handler = OptionHandler(self.__test_path)

                for other_key, method in self.__option_method_names.items():
                    self.assert_default_option(
                        default_options[other_key], option_handler, other_key, method
                    )


if __name__ == "__main__":
    main()
