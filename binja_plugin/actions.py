from pathlib import Path
from pprint import pformat

from binaryninja.binaryview import BinaryView
from binaryninja.interaction import get_open_filename_input
from binaryninja.log import Logger
from pyparsing import ParseException

from ..parse import parse
from .type_import import create_binary_view_types

logger = Logger(session_id=0, logger_name=__name__)


def action_load_type_layout_file(bv: BinaryView):
    type_layout_file_path = get_open_filename_input(
        prompt="Open a Rust type layout information file"
    )
    logger.log_info(f"{type_layout_file_path}")

    if type_layout_file_path is not None:
        type_layout_file_path = Path(type_layout_file_path)
        with open(type_layout_file_path) as type_layout_file:
            try:
                parsed_rust_types = parse(type_layout_file)
                logger.log_info(f"{pformat(parsed_rust_types)}")
                create_binary_view_types(bv=bv, rust_types=parsed_rust_types)
            except ParseException as err:
                logger.log_error(
                    f"Failed to parse the provided Rust type layout file {type_layout_file_path}: {err.explain()}"
                )
