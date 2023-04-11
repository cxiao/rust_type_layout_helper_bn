from pyparsing import Keyword, Literal, Opt, ParseResults, Word, nums, printables


def type_definition_line(data: str) -> ParseResults:
    line_marker = Keyword("print-type-size")
    type_marker = Keyword("type:")
    name = (
        Literal("`")
        + Word(printables, exclude_chars="`").set_results_name("type_name")
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

    return type_definition.parse_string(data)


def field_definition_line(data: str) -> ParseResults:
    line_marker = Keyword("print-type-size")
    field_marker = Keyword("field")
    name = (
        Literal("`")
        + Word(printables, exclude_chars="`").set_results_name("field_name")
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

    return field_definition.parse_string(data)


def variant_definition_line(data: str) -> ParseResults:
    line_marker = Keyword("print-type-size")
    variant_marker = Keyword("variant")
    name = (
        Literal("`")
        + Word(printables, exclude_chars="`").set_results_name("variant_name")
        + Literal("`")
        + Literal(":")
    )
    size = Word(nums).set_results_name("variant_size") + Keyword("bytes")

    variant_definition = line_marker + variant_marker + name + size

    return variant_definition.parse_string(data)


def discriminant_definition_line(data: str) -> ParseResults:
    line_marker = Keyword("print-type-size")
    discriminant_marker = Keyword("discriminant:")
    size = Word(nums).set_results_name("discriminant_size") + Keyword("bytes")

    discriminant_definition = line_marker + discriminant_marker + size

    return discriminant_definition.parse_string(data)


def padding_definition_line(data: str) -> ParseResults:
    line_marker = Keyword("print-type-size")
    padding_marker = Keyword("padding:")
    size = Word(nums).set_results_name("padding_size") + Keyword("bytes")

    padding_definition = line_marker + padding_marker + size

    return padding_definition.parse_string(data)


def end_padding_definition_line(data: str) -> ParseResults:
    line_marker = Keyword("print-type-size")
    padding_marker = Keyword("end padding:")
    size = Word(nums).set_results_name("padding_size") + Keyword("bytes")

    padding_definition = line_marker + padding_marker + size

    return padding_definition.parse_string(data)


print(
    type_definition_line(
        "print-type-size type: `unix::linux_like::linux::gnu::timex`: 208 bytes, alignment: 8 bytes"
    ).as_dict()
)

print(field_definition_line("print-type-size     field `.k1`: 8 bytes").as_dict())
print(
    field_definition_line(
        "print-type-size         field `.0`: 8 bytes, alignment: 8 bytes"
    ).as_dict()
)

print(variant_definition_line("print-type-size     variant `Some`: 40 bytes").as_dict())

print(padding_definition_line("print-type-size         padding: 3 bytes").as_dict())

print(
    discriminant_definition_line("print-type-size     discriminant: 4 bytes").as_dict()
)
