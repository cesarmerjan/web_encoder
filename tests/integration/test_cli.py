import unittest
import argparse
from src.web_encoder.__main__ import (
    main,
    create_parser,
    add_arguments,
    process_data,
)


class TestStringSigner(unittest.TestCase):
    def setUp(self):
        self.message = "Test message."
        self.expected_encoded_message = "VGVzdCBtZXNzYWdlLg"
        self.compressive_message = "aaaaaaaaaaaaaaaaaaaaaaaaa"
        self.expected_encoded_message_compressive_message = (
            "YWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYQ"
        )
        self.expected_compressed_encoded_message = ".eJxLTMQBAHs-CXo"
        self.program = "test"
        self.usage = "test"
        self.description = "test"
        self.epilog = "test"
        self.valid_options = ("e", "d")

    def test_create_parser(self):
        parser = create_parser(
            self.program,
            self.usage,
            self.description,
            self.epilog
        )
        self.assertIsInstance(parser, argparse.ArgumentParser)

    def test_add_args_to_parcer(self):
        parser = create_parser(
            self.program,
            self.usage,
            self.description,
            self.epilog
        )
        add_arguments(parser)

    def test_parse_arguments(self):
        parser = create_parser(
            self.program,
            self.usage,
            self.description,
            self.epilog
        )
        add_arguments(parser)

        args = parser.parse_args([self.valid_options[0], self.message])
        self.assertTrue(args)
        self.assertEqual(args.option, self.valid_options[0])
        self.assertEqual(args.data, self.message)
        self.assertTrue(args.compress)

        args = parser.parse_args([self.valid_options[1], self.expected_encoded_message])
        self.assertTrue(args)
        self.assertEqual(args.option, self.valid_options[1])
        self.assertEqual(args.data, self.expected_encoded_message)
        self.assertTrue(args.compress)

    def test_process_data(self):
        parser = create_parser(
            self.program,
            self.usage,
            self.description,
            self.epilog
        )
        add_arguments(parser)

        args = parser.parse_args([self.valid_options[0], self.message])
        result = process_data(args)
        self.assertEqual(result, self.expected_encoded_message)

        args = parser.parse_args([self.valid_options[1], self.expected_encoded_message])
        result = process_data(args)
        self.assertEqual(result, self.message)

        args = parser.parse_args([self.valid_options[0], self.compressive_message])
        result = process_data(args)
        self.assertEqual(result, self.expected_compressed_encoded_message)

        args = parser.parse_args([self.valid_options[1], self.expected_compressed_encoded_message])
        result = process_data(args)
        self.assertEqual(result, self.compressive_message)

        args = parser.parse_args([self.valid_options[0], self.compressive_message])
        args.compress = False
        result = process_data(args)
        self.assertEqual(result, self.expected_encoded_message_compressive_message)

    def test_cli(self):

        result = main([self.valid_options[0], self.message])
        self.assertEqual(result, self.expected_encoded_message)

        result = main([self.valid_options[1], self.expected_encoded_message])
        self.assertEqual(result, self.message)
