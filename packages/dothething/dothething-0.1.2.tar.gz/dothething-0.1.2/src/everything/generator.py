import logging
from typing import Callable
import os
import readline
import sys
from pathlib import Path

import black
import click

from everything.utils.openai import generate_function
from everything.utils.scanner import build_context_strings

_LOGGER = logging.getLogger(__name__)


def runtime_generate_function(name, context_radius=4, history=10) -> Callable:
    import __main__ as main

    if not hasattr(main, "__file__"):
        _LOGGER.info("Using REPL mode")
        readline.get_current_history_length()
        last_few_commands = [readline.get_history_item(i) for i in range(1, history)]
        context_string = "\n".join(last_few_commands)
    else:
        _LOGGER.info("Using SOURCE mode")
        source_path = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
        context_string = build_context_strings(source_path, name, context_radius)[name]

    return generate_function(name, context_string)  # pyright: ignore


def build_onefile_module(root_path: Path, module: str, **kwargs) -> str:
    functions = []
    for function_name, context_string in build_context_strings(
        root_path, module, **kwargs
    ).items():
        click.echo(f"Generating {function_name}...")
        functions.append(generate_function(function_name, context_string, True))
    source = "\n\n".join(functions)
    source = black.format_str(source, mode=black.FileMode()).strip()
    return source
