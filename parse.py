import string
from typing import Dict, TextIO

from pyparsing import (
    Group,
    Keyword,
    Literal,
    Opt,
    ParserElement,
    Word,
    ZeroOrMore,
    nums,
)


def _type_definition_line() -> ParserElement:
    line_marker = Keyword("print-type-size")
    type_marker = Keyword("type:")
    name = (
        Literal("`")
        # Because type names can include spaces,
        # such as in `Result<u8, Err>`,
        # we need to use string.printable rather than
        # pyparsing.printable, which excludes spaces.
        + Word(string.printable, exclude_chars="`").set_results_name("type_name")
        + Literal("`")
        + Literal(":")
    )
    size = Word(nums).set_results_name("type_size") + Keyword("bytes")
    alignment_marker = Keyword("alignment:")
    alignment_bytes = Word(nums).set_results_name("type_alignment_bytes") + Keyword(
        "bytes"
    )
    alignment_information = alignment_marker + alignment_bytes

    type_definition = (
        line_marker + type_marker + name + size + Literal(",") + alignment_information
    )

    return type_definition


def _field_definition_line() -> ParserElement:
    line_marker = Keyword("print-type-size")
    field_marker = Keyword("field")
    name = (
        Literal("`")
        + Word(string.printable, exclude_chars="`").set_results_name("field_name")
        + Literal("`")
        + Literal(":")
    )
    size = Word(nums).set_results_name("field_size") + Keyword("bytes")
    alignment_marker = Keyword("alignment:")
    alignment_bytes = Word(nums).set_results_name("field_alignment_bytes") + Keyword(
        "bytes"
    )
    alignment_information = alignment_marker + alignment_bytes

    field_definition = (
        line_marker
        + field_marker
        + name
        + size
        + Opt(Literal(",") + alignment_information)
    )

    return field_definition


def _padding_definition_line() -> ParserElement:
    line_marker = Keyword("print-type-size")
    padding_marker = Keyword("padding:")
    size = Word(nums).set_results_name("padding_size") + Keyword("bytes")

    padding_definition = line_marker + padding_marker + size

    return padding_definition


def _end_padding_definition_line() -> ParserElement:
    line_marker = Keyword("print-type-size")
    padding_marker = Keyword("end padding:")
    size = Word(nums).set_results_name("padding_size") + Keyword("bytes")

    padding_definition = line_marker + padding_marker + size

    return padding_definition


def _variant_definition_line() -> ParserElement:
    line_marker = Keyword("print-type-size")
    variant_marker = Keyword("variant")
    name = (
        Literal("`")
        + Word(string.printable, exclude_chars="`").set_results_name("variant_name")
        + Literal("`")
        + Literal(":")
    )
    size = Word(nums).set_results_name("variant_size") + Keyword("bytes")

    variant_definition = line_marker + variant_marker + name + size

    return variant_definition


def _discriminant_definition_line() -> ParserElement:
    line_marker = Keyword("print-type-size")
    discriminant_marker = Keyword("discriminant:")
    size = Word(nums).set_results_name("discriminant_size") + Keyword("bytes")

    discriminant_definition = line_marker + discriminant_marker + size

    return discriminant_definition


def _variant() -> ParserElement:
    variant = _variant_definition_line() + ZeroOrMore(
        Group(
            _field_definition_line()
            | _padding_definition_line()
            | _end_padding_definition_line()
        )
    ).set_results_name("fields")

    return variant


def parse(data: TextIO) -> Dict:
    type_definition = _type_definition_line() + ZeroOrMore(
        Group(
            _field_definition_line()
            | _padding_definition_line()
            | _end_padding_definition_line()
            | _discriminant_definition_line()
            | _variant()
        )
    ).set_results_name("fields")

    types = ZeroOrMore(Group(type_definition)).set_results_name("types")
    return types.parse_file(data).as_dict()


if __name__ == "__main__":
    from pprint import pprint

    with open("tests/data/print-type-sizes.txt", "r") as f:
        result = parse(f)
        pprint(result)
