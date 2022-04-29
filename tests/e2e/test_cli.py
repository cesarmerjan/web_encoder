import subprocess
import unittest


class TestStringSigner(unittest.TestCase):
    def setUp(self):
        self.message = "Test message."
        self.expected_encoded_message = "VGVzdCBtZXNzYWdlLg"
        self.compressive_message = "aaaaaaaaaaaaaaaaaaaaaaaaa"
        self.expected_encoded_message_compressive_message = (
            "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYQ"
        )
        self.expected_compressed_encoded_message = ".eJxLTMQBAHs-CXo"
        self.command = "python3 -m src.web_encoder {option} '{data}' {compress}"

    def test_cli_encode_data(self):
        command = self.command.format(option="e", data=self.message, compress="")
        output = subprocess.check_output(command, shell=True).decode().strip()
        self.assertEqual(output, self.expected_encoded_message)

    def test_cli_decode_data(self):
        command = self.command.format(
            option="d", data=self.expected_encoded_message, compress=""
        )
        output = subprocess.check_output(command, shell=True).decode().strip()
        self.assertEqual(output, self.message)

    def test_cli_enode_data_without_compress(self):
        command = self.command.format(
            option="e", data=self.compressive_message, compress="--no-compress"
        )
        output = subprocess.check_output(command, shell=True).decode().strip()
        self.assertEqual(output, self.expected_encoded_message_compressive_message)

    def test_cli_enode_data_with_compress(self):
        command = self.command.format(
            option="e", data=self.compressive_message, compress=""
        )
        output = subprocess.check_output(command, shell=True).decode().strip()
        self.assertEqual(output, self.expected_compressed_encoded_message)
