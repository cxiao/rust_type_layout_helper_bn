import string
from pprint import pprint

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


def type_definition_line() -> ParserElement:
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


def field_definition_line() -> ParserElement:
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


def padding_definition_line() -> ParserElement:
    line_marker = Keyword("print-type-size")
    padding_marker = Keyword("padding:")
    size = Word(nums).set_results_name("padding_size") + Keyword("bytes")

    padding_definition = line_marker + padding_marker + size

    return padding_definition


def end_padding_definition_line() -> ParserElement:
    line_marker = Keyword("print-type-size")
    padding_marker = Keyword("end padding:")
    size = Word(nums).set_results_name("padding_size") + Keyword("bytes")

    padding_definition = line_marker + padding_marker + size

    return padding_definition


def variant_definition_line() -> ParserElement:
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


def discriminant_definition_line() -> ParserElement:
    line_marker = Keyword("print-type-size")
    discriminant_marker = Keyword("discriminant:")
    size = Word(nums).set_results_name("discriminant_size") + Keyword("bytes")

    discriminant_definition = line_marker + discriminant_marker + size

    return discriminant_definition


def variant() -> ParserElement:
    variant = variant_definition_line() + ZeroOrMore(
        Group(
            field_definition_line()
            | padding_definition_line()
            | end_padding_definition_line()
        )
    ).set_results_name("fields")

    return variant


field_test_data = """
print-type-size type: `miniz_oxide::inflate::core::DecompressorOxide`: 10992 bytes, alignment: 8 bytes
print-type-size     field `.tables`: 10464 bytes
print-type-size     field `.bit_buf`: 8 bytes
print-type-size     field `.num_bits`: 4 bytes
print-type-size     field `.z_header0`: 4 bytes
print-type-size     field `.z_header1`: 4 bytes
print-type-size     field `.z_adler32`: 4 bytes
print-type-size     field `.finish`: 4 bytes
print-type-size     field `.block_type`: 4 bytes
print-type-size     field `.check_adler32`: 4 bytes
print-type-size     field `.dist`: 4 bytes
print-type-size     field `.counter`: 4 bytes
print-type-size     field `.num_extra`: 4 bytes
print-type-size     field `.table_sizes`: 12 bytes
print-type-size     field `.raw_header`: 4 bytes
print-type-size     field `.len_codes`: 457 bytes
print-type-size     field `.state`: 1 bytes
print-type-size     end padding: 6 bytes
"""

variant_test_data = """
print-type-size type: `std::result::Result<u16, std::num::ParseIntError>`: 4 bytes, alignment: 2 bytes
print-type-size     discriminant: 1 bytes
print-type-size     variant `Ok`: 3 bytes
print-type-size         padding: 1 bytes
print-type-size         field `.0`: 2 bytes, alignment: 2 bytes
print-type-size     variant `Err`: 1 bytes
print-type-size         field `.0`: 1 bytes
"""

type_definition = type_definition_line() + ZeroOrMore(
    Group(
        field_definition_line()
        | padding_definition_line()
        | end_padding_definition_line()
        | discriminant_definition_line()
        | variant()
    )
).set_results_name("fields")

print(type_definition.parse_string(variant_test_data).dump())
pprint(type_definition.parse_string(variant_test_data).as_dict())
