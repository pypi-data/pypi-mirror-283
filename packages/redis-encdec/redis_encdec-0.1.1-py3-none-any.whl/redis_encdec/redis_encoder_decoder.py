from typing import Dict, Any
import json
import logging


class RedisEncoderDecoder:
    """
    A utility class to handle encoding and decoding of dictionaries for Redis storage.

    This class provides methods to encode dictionary values into JSON strings for storage in Redis,
    and to decode JSON strings back into their original data types.

    Methods:
    - encoder: Encodes dictionary values to JSON formatted strings.
    - decoder: Decodes JSON formatted string values back to their original data types.
    """

    @classmethod
    def encoder(cls, dictionary: Dict[str, Any]) -> Dict[str, str]:
        """
        Encodes the given dictionary values to JSON formatted strings.

        Args:
            dictionary (Dict[str, Any]): The dictionary to encode. Dictionary keys
                                         must be strings, and values should be JSON
                                         serializable.

        Returns:
            Dict[str, str]: A new dictionary where the values are JSON formatted strings
                            or the original value if it cannot be converted, with keys
                            unchanged.

        Example:
            >>> input_dict = {"a": [1, 2, 3], "b": {"c": "d"}}
            >>> RedisEncoderDecoder.encoder(input_dict)
            {'a': '[1, 2, 3]', 'b': '{"c": "d"}'}
        """
        encoded_dict = {}
        for key, val in dictionary.items():
            try:
                encoded_dict[key] = json.dumps(val)
            except (TypeError, ValueError) as e:
                encoded_dict[key] = str(val)  # Fallback to string representation
                logging.warning(
                    f"Unable to serialize the value of key: '{key}'. The value has been left unchanged. Error: {e}")

        return encoded_dict

    @classmethod
    def decoder(cls, dictionary: Dict[str, str]) -> Dict[str, Any]:
        """
        Decodes the given dictionary values from JSON formatted strings to their original data types.

        Args:
            dictionary (Dict[str, str]): The dictionary to decode. Dictionary keys are
                                         strings, and values are JSON formatted strings.

        Returns:
            Dict[str, Any]: A new dictionary where the values are converted back to
                            their original data types.

        Example:
            >>> input_dict = {'a': '[1, 2, 3]', 'b': '{"c": "d"}'}
            >>> RedisEncoderDecoder.decoder(input_dict)
            {'a': [1, 2, 3], 'b': {'c': 'd'}}

        Note:
            If a value in the dictionary is not a valid JSON formatted string,
            a json.JSONDecodeError will be raised.
        """
        decoded_dict = {}
        for key, val in dictionary.items():
            try:
                decoded_dict[key] = json.loads(val)
            except (json.JSONDecodeError, TypeError) as e:
                decoded_dict[key] = val  # Fallback to original value
                logging.warning(
                    f"Unable to deserialize the value of key: '{key}'. The value has been left unchanged. Error: {e}")

        return decoded_dict


# Example usage:
if __name__ == "__main__":
    input_dict = {"a": [1, 2, 3], "b": {"c": "d"}}
    encoded_dict = RedisEncoderDecoder.encoder(input_dict)
    print(f"Encoded: {encoded_dict}")

    decoded_dict = RedisEncoderDecoder.decoder(encoded_dict)
    print(f"Decoded: {decoded_dict}")
