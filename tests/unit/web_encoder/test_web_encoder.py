import unittest

from src.web_encoder import WebEncoder
from src.web_encoder.exceptions import (
    InvalidEncodingErrors,
    CannotBeCompressed,
    CannotBeDecompressed,
    DataDecodeError,
    InvalidBytesType,
    InvalidDataType,
    InvalidEncodedDataType,
    InvalidStringType,
)


class TestStringSigner(unittest.TestCase):
    def setUp(self):
        self.message = "Test message."
        self.expected_encoded_message = "VGVzdCBtZXNzYWdlLg"
        self.compressive_message = "aaaaaaaaaaaaaaaaaaaaaaaaa"
        self.expected_encoded_message_compressive_message = (
            "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYQ"
        )
        self.expected_compressed_message = b"x\x9cKL\xc4\x01\x00{>\tz"
        self.expected_compressed_encoded_message = ".eJxLTMQBAHs-CXo"

    def test_web_encoder_representation(self):
        web_encoder = WebEncoder()
        self.assertIsInstance(web_encoder.__str__(), str)
        self.assertIsInstance(web_encoder.__repr__(), str)

    def test_encode_message(self):
        web_encoder = WebEncoder()
        encoded_message = web_encoder.encode(self.message)
        self.assertEqual(encoded_message, self.expected_encoded_message)

    def test_encode_message_with_out_compression(self):
        web_encoder = WebEncoder()
        encoded_message = web_encoder.encode(self.compressive_message, compress=False)
        self.assertEqual(
            encoded_message, self.expected_encoded_message_compressive_message
        )

    def test_decode_message(self):
        web_encoder = WebEncoder()
        message = web_encoder.decode(self.expected_encoded_message)
        self.assertEqual(self.message, message)

    def test_encode_compressive_message(self):
        web_encoder = WebEncoder()
        compressed_encoded_message = web_encoder.encode(self.compressive_message)
        self.assertEqual(
            compressed_encoded_message, self.expected_compressed_encoded_message
        )

    def test_decode_compressive_message(self):
        web_encoder = WebEncoder()
        compressed_encoded_message = web_encoder.encode(self.compressive_message)
        decoded_decompressed_message = web_encoder.decode(compressed_encoded_message)
        self.assertEqual(decoded_decompressed_message, self.compressive_message)

    def test_encode_input_errors(self):
        web_encoder = WebEncoder()

        with self.assertRaises(InvalidDataType):
            web_encoder.encode(1)
        with self.assertRaises(InvalidDataType):
            web_encoder.encode([])
        with self.assertRaises(InvalidDataType):
            web_encoder.encode({})
        with self.assertRaises(InvalidDataType):
            web_encoder.encode(set([]))
        with self.assertRaises(InvalidDataType):
            web_encoder.encode(1.2)
        with self.assertRaises(InvalidDataType):
            web_encoder.encode(lambda: "function")
        with self.assertRaises(InvalidDataType):
            web_encoder.encode(type("MyClass", (object,), {}))
        with self.assertRaises(InvalidDataType):
            web_encoder.encode(True)

    def test_decode_input_errors(self):
        web_encoder = WebEncoder()

        with self.assertRaises(InvalidEncodedDataType):
            web_encoder.decode(1)
        with self.assertRaises(InvalidEncodedDataType):
            web_encoder.decode([])
        with self.assertRaises(InvalidEncodedDataType):
            web_encoder.decode({})
        with self.assertRaises(InvalidEncodedDataType):
            web_encoder.decode(set([]))
        with self.assertRaises(InvalidEncodedDataType):
            web_encoder.decode(1.2)
        with self.assertRaises(InvalidEncodedDataType):
            web_encoder.decode(lambda: "function")
        with self.assertRaises(InvalidEncodedDataType):
            web_encoder.decode(type("MyClass", (object,), {}))
        with self.assertRaises(InvalidEncodedDataType):
            web_encoder.decode(True)

    def test_string_to_bytes_method(self):
        web_encoder = WebEncoder()
        byte_message = web_encoder._string_to_bytes(self.message)
        self.assertEqual(byte_message, self.message.encode())

    def test_string_to_bytes_method_errors(self):
        web_encoder = WebEncoder()

        with self.assertRaises(InvalidStringType):
            web_encoder._string_to_bytes(b"OK")
        with self.assertRaises(InvalidStringType):
            web_encoder._string_to_bytes(1)
        with self.assertRaises(InvalidStringType):
            web_encoder._string_to_bytes([])
        with self.assertRaises(InvalidStringType):
            web_encoder._string_to_bytes({})
        with self.assertRaises(InvalidStringType):
            web_encoder._string_to_bytes(set([]))
        with self.assertRaises(InvalidStringType):
            web_encoder._string_to_bytes(1.2)
        with self.assertRaises(InvalidStringType):
            web_encoder._string_to_bytes(lambda: "function")
        with self.assertRaises(InvalidStringType):
            web_encoder._string_to_bytes(type("MyClass", (object,), {}))
        with self.assertRaises(InvalidStringType):
            web_encoder._string_to_bytes(True)

    def test_bytes_to_string_method(self):
        web_encoder = WebEncoder()
        message = web_encoder._bytes_to_string(self.message.encode())
        self.assertEqual(message, self.message)

    def test_bytes_to_string_method_errors(self):
        web_encoder = WebEncoder()

        with self.assertRaises(DataDecodeError):
            _string = "não".encode("utf-16")
            web_encoder._bytes_to_string(_string)

        with self.assertRaises(InvalidBytesType):
            web_encoder._bytes_to_string("OK")
        with self.assertRaises(InvalidBytesType):
            web_encoder._bytes_to_string(1)
        with self.assertRaises(InvalidBytesType):
            web_encoder._bytes_to_string([])
        with self.assertRaises(InvalidBytesType):
            web_encoder._bytes_to_string({})
        with self.assertRaises(InvalidBytesType):
            web_encoder._bytes_to_string(set([]))
        with self.assertRaises(InvalidBytesType):
            web_encoder._bytes_to_string(1.2)
        with self.assertRaises(InvalidBytesType):
            web_encoder._bytes_to_string(lambda: "function")
        with self.assertRaises(InvalidBytesType):
            web_encoder._bytes_to_string(type("MyClass", (object,), {}))
        with self.assertRaises(InvalidBytesType):
            web_encoder._bytes_to_string(True)

    def test__base64_urlsafe_encode_method(self):
        web_encoder = WebEncoder()

        encoded_message = web_encoder._base64_urlsafe_encode(self.message.encode())

        self.assertEqual(encoded_message, self.expected_encoded_message.encode())

    def test__base64_urlsafe_encode_method_errors(self):
        web_encoder = WebEncoder()

        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_encode("OK")
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_encode(1)
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_encode([])
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_encode({})
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_encode(set([]))
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_encode(1.2)
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_encode(lambda: "function")
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_encode(type("MyClass", (object,), {}))
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_encode(True)

    def test_base64_urlsafe_decode_method(self):
        web_encoder = WebEncoder()

        encoded_message = web_encoder._base64_urlsafe_encode(self.message.encode())

        message = web_encoder._base64_urlsafe_decode(encoded_message)

        self.assertEqual(message, self.message.encode())

    def test_base64_urlsafe_decode_method_errors(self):
        web_encoder = WebEncoder()

        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_decode("OK")
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_decode(1)
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_decode([])
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_decode({})
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_decode(set([]))
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_decode(1.2)
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_decode(lambda: "function")
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_decode(type("MyClass", (object,), {}))
        with self.assertRaises(InvalidBytesType):
            web_encoder._base64_urlsafe_decode(True)

    def test_compress_data_method(self):
        web_encoder = WebEncoder()
        compressed_message = web_encoder._compress_data(
            self.compressive_message.encode()
        )
        self.assertEqual(compressed_message, self.expected_compressed_message)

    def test_compress_data_method_errors(self):
        web_encoder = WebEncoder()

        with self.assertRaises(CannotBeCompressed):
            web_encoder._compress_data(self.message.encode())

        with self.assertRaises(InvalidBytesType):
            web_encoder._compress_data("OK")
        with self.assertRaises(InvalidBytesType):
            web_encoder._compress_data(1)
        with self.assertRaises(InvalidBytesType):
            web_encoder._compress_data([])
        with self.assertRaises(InvalidBytesType):
            web_encoder._compress_data({})
        with self.assertRaises(InvalidBytesType):
            web_encoder._compress_data(set([]))
        with self.assertRaises(InvalidBytesType):
            web_encoder._compress_data(1.2)
        with self.assertRaises(InvalidBytesType):
            web_encoder._compress_data(lambda: "function")
        with self.assertRaises(InvalidBytesType):
            web_encoder._compress_data(type("MyClass", (object,), {}))
        with self.assertRaises(InvalidBytesType):
            web_encoder._compress_data(True)

    def test_decompress_data_method(self):
        web_encoder = WebEncoder()

        compressed_message = web_encoder._compress_data(
            self.compressive_message.encode()
        )

        decompressed_data = web_encoder._decompress_data(compressed_message)

        self.assertEqual(decompressed_data, self.compressive_message.encode())

    def test_decompress_data_method_errors(self):
        web_encoder = WebEncoder()

        with self.assertRaises(CannotBeDecompressed):
            web_encoder._decompress_data(b"jdkfmcvalleifna")

        with self.assertRaises(InvalidBytesType):
            web_encoder._decompress_data("OK")
        with self.assertRaises(InvalidBytesType):
            web_encoder._decompress_data(1)
        with self.assertRaises(InvalidBytesType):
            web_encoder._decompress_data([])
        with self.assertRaises(InvalidBytesType):
            web_encoder._decompress_data({})
        with self.assertRaises(InvalidBytesType):
            web_encoder._decompress_data(set([]))
        with self.assertRaises(InvalidBytesType):
            web_encoder._decompress_data(1.2)
        with self.assertRaises(InvalidBytesType):
            web_encoder._decompress_data(lambda: "function")
        with self.assertRaises(InvalidBytesType):
            web_encoder._decompress_data(type("MyClass", (object,), {}))
        with self.assertRaises(InvalidBytesType):
            web_encoder._decompress_data(True)

    def test_encoding_errors_input_errors(self):

        with self.assertRaises(InvalidEncodingErrors):
            WebEncoder(encoding_errors="OK")
        with self.assertRaises(InvalidEncodingErrors):
            WebEncoder(encoding_errors=1)
        with self.assertRaises(InvalidEncodingErrors):
            WebEncoder(encoding_errors=[])
        with self.assertRaises(InvalidEncodingErrors):
            WebEncoder(encoding_errors={})
        with self.assertRaises(InvalidEncodingErrors):
            WebEncoder(encoding_errors=set([]))
        with self.assertRaises(InvalidEncodingErrors):
            WebEncoder(encoding_errors=1.2)
        with self.assertRaises(InvalidEncodingErrors):
            WebEncoder(encoding_errors=lambda: "function")
        with self.assertRaises(InvalidEncodingErrors):
            WebEncoder(encoding_errors=type("MyClass", (object,), {}))
        with self.assertRaises(InvalidEncodingErrors):
            WebEncoder(encoding_errors=True)
