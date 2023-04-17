from typing import List

from binaryninja.binaryview import BinaryView
from binaryninja.log import Logger
from binaryninja.types import (
    ArrayType,
    EnumerationBuilder,
    IntegerType,
    StructureBuilder,
    StructureType,
    StructureVariant,
    Type,
    VoidType,
)

from ..parse import Discriminant, Field, Padding, Variant
from ..parse import Type as RustType

logger = Logger(session_id=0, logger_name=__name__)


def _create_bn_type_from_field_size(field_size: int) -> Type:
    if field_size == 0:
        return VoidType.create()
    elif field_size in (1, 2, 4, 8, 16):
        return IntegerType.create(field_size)
    else:
        return ArrayType.create(Type.char(), field_size)


def _create_variant_struct(rust_variant: Variant) -> StructureType:
    bn_struct = StructureBuilder.create(packed=True)

    if rust_variant.fields is not None:
        for rust_struct_field in rust_variant.fields:
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

    if bn_struct.width != rust_variant.variant_size:
        logger.log_error(
            f"Size of created variant struct ({bn_struct.width} bytes) does not match size of parsed Rust variant struct ({rust_variant.variant_size} bytes)"
        )

    return bn_struct.immutable_copy()


def _create_bn_types_for_rust_type(bv: BinaryView, rust_type: RustType):
    """
    Note that for Rust enums, i.e. `RustType`s which hold
    a `Discriminant` and `Variant`(s),
    this function creates the following Binary Ninja types,
    - A new enum type for the discriminant.
    - A new struct type for each variant.
    - A new struct type containing:
        - The enum type for the discriminant.
        - A union whose members are the struct types for each variant.
    """

    bn_struct = StructureBuilder.create(packed=True)
    rust_field_types = [type(field) for field in rust_type.fields]
    if Variant in rust_field_types:  # The Rust type is a sum type, i.e. a Rust enum
        # TODO: Handle the case where there is only variant, and no discriminant!
        # This shows up in cases like (ironically)
        # repr(C) unions like SocketAddrCRepr: https://github.com/rust-lang/rust/blob/8a778ca1e35e4a8df95c00d800100d95e63e7722/library/std/src/sys_common/net.rs#L725
        bn_variants_union = StructureBuilder.create(
            packed=True, type=StructureVariant.UnionStructureType
        )
        for rust_type_field in rust_type.fields:
            if isinstance(rust_type_field, Discriminant):
                bn_discriminant_enum_name = f"{rust_type.type_name}::discriminant"
                bn_discriminant_enum = EnumerationBuilder.create(
                    width=rust_type_field.discriminant_size
                )

                bv.define_user_type(
                    name=bn_discriminant_enum_name,
                    type_obj=bn_discriminant_enum,
                )
                bn_struct.append(
                    type=Type.named_type_from_registered_type(
                        bv, bn_discriminant_enum_name
                    ),
                    name="discriminant",
                )
            elif isinstance(rust_type_field, Variant):
                bn_variant_struct_name = (
                    f"{rust_type.type_name}::{rust_type_field.variant_name}"
                )
                bn_variant_struct = _create_variant_struct(rust_type_field)

                bv.define_user_type(
                    name=bn_variant_struct_name,
                    type_obj=bn_variant_struct,
                )
                bn_variants_union.append(
                    type=Type.named_type_from_registered_type(
                        bv, bn_variant_struct_name
                    ),
                    name=rust_type_field.variant_name,
                )

        bn_struct.append(
            type=bn_variants_union,
            name=f"{rust_type.type_name}::variants",
        )

    else:
        for rust_type_field in rust_type.fields:
            if isinstance(rust_type_field, Field):
                bn_field_type = _create_bn_type_from_field_size(
                    rust_type_field.field_size
                )
                bn_struct.append(type=bn_field_type, name=rust_type_field.field_name)
            elif isinstance(rust_type_field, Padding):
                bn_field_type = _create_bn_type_from_field_size(
                    rust_type_field.padding_size
                )
                bn_struct.append(type=bn_field_type, name="_padding")

    if bn_struct.width != rust_type.type_size:
        logger.log_error(
            f"Created struct for Rust type {rust_type.type_name} has size ({bn_struct.width} bytes) which does not match size of parsed Rust type ({rust_type.type_size} bytes)"
        )

    bv.define_user_type(name=rust_type.type_name, type_obj=bn_struct)


def create_binary_view_types(
    bv: BinaryView,
    rust_types: List[RustType],
):
    for rust_type in rust_types:
        _create_bn_types_for_rust_type(bv=bv, rust_type=rust_type)

    # TODO: If every variant is zero-sized, it can be an enum.
    # The discriminant size is then used to calculate the enum width.
