from json import load, dump, JSONDecodeError
from os import path

class JSONHandler:
    def __init__(self, file_path: str) -> None:
        self.__file_path: str = file_path

    def read_json(self) -> dict[str, str | float]:
        """Reads JSON data from the file."""
        if not path.exists(self.__file_path):
            print(f"File not found at path {self.__file_path}")
            return {}
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                return load(file)
        except JSONDecodeError as e:
            print(f"JSON decoding error occurred: {e}")
            return {}

    def write_json(self, data: dict[str, str | float]) -> None:
        """Writes JSON data to the file."""
        try:
            with open(self.__file_path, "w", encoding="utf-8") as file:
                dump(data, file, indent=4)
        except TypeError as e:
            print(f"Serialization error occurred: {e}")
        except OSError as e:
            print(f"File operation error occurred: {e}")
