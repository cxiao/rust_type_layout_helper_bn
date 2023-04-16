from typing import List

from binaryninja.binaryview import BinaryView
from binaryninja.log import Logger
from binaryninja.types import (
    ArrayType,
    IntegerType,
    StructureBuilder,
    StructureType,
    Type,
    VoidType,
)

from ..parse import Field, Padding
from ..parse import Type as RustType

logger = Logger(session_id=0, logger_name=__name__)


def _create_bn_type_from_field_size(field_size: int) -> Type:
    if field_size == 0:
        return VoidType.create()
    elif field_size in (1, 2, 4, 8, 16):
        return IntegerType.create(field_size)
    else:
        return ArrayType.create(Type.char(), field_size)


def _create_struct(rust_struct: RustType) -> StructureType:
    bn_struct = StructureBuilder.create(packed=True)

    for rust_struct_field in rust_struct.fields:
        if isinstance(rust_struct_field, Field):
            bn_field_type = _create_bn_type_from_field_size(
                rust_struct_field.field_size
            )
            bn_struct.append(type=bn_field_type, name=rust_struct_field.field_name)
        elif isinstance(rust_struct_field, Padding):
            bn_field_type = _create_bn_type_from_field_size(
                rust_struct_field.padding_size
            )
            bn_struct.append(type=bn_field_type, name="_padding")

    if bn_struct.width != rust_struct.type_size:
        logger.log_error(
            f"Size of created struct ({bn_struct.width} bytes) does not match size of parsed Rust struct ({rust_struct.type_size} bytes)"
        )

    return bn_struct.immutable_copy()


def create_binary_view_types(
    bv: BinaryView,
    rust_types: List[RustType],
):
    for rust_type in rust_types:
        bv.define_user_type(rust_type.type_name, _create_struct(rust_type))

    # TODO: If every variant is zero-sized, it can be an enum.
    # The discriminant size is then used to calculate the enum width.
