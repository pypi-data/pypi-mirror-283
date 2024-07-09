"""
Jinja environment to use while generating wrappers
"""

from __future__ import annotations

from pathlib import Path

import jinja2

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(Path(__file__).parent.absolute()),
    autoescape=jinja2.select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=jinja2.StrictUndefined,
)
"""Jinja2 environment to use for template rendering"""


def indent_based_on_first_line(
    code: str,
    indent: str,
) -> str:
    """
    Indent code based on the indent of the first line.

    If the first line does not have indent equal to ``indent``,
    all the code except the first line
    will have an indent added
    such that the first line would have an indent of ``indent``.
    We exclude the first line
    so that the indent can be included in the jinja template too,
    which makes it easier to read what is going on.

    Parameters
    ----------
    code
        Code to indent

    indent
        Indent to ensure that the first line has


    Returns
    -------
        Indented code
    """
    if not code:
        # Empty line
        return code

    code_split = code.splitlines()

    if len(code_split) == 1:
        # Nothing to indent
        return code

    first_line = code_split[0]

    first_line_indent = len(first_line) - len(first_line.lstrip())
    indent_len = len(indent)
    if first_line_indent >= indent_len:
        return code

    required_extra_indent = " " * (indent_len - first_line_indent)

    after_first_line = code_split[1:]
    return "\n".join(
        [first_line, *[f"{required_extra_indent}{line}" for line in after_first_line]]
    )


def strip_empty_lines(inp: str) -> str:
    """
    Strip empty lines

    More specifically, turn lines
    that only have whitespace into a single newline character.
    This is a workaround until we start formatting our Fortran
    as part of the generation process
    (https://gitlab.com/magicc/fgen/-/issues/26).

    Parameters
    ----------
    inp
        Input string

    Returns
    -------
        Input string, with all whitespace lines replaced by a single newline character.
    """
    out = [line if line.strip() else "\n" for line in inp.splitlines()]

    return "\n".join(out)


JINJA_ENV.filters["indent_based_on_first_line"] = indent_based_on_first_line
JINJA_ENV.filters["strip_empty_lines"] = strip_empty_lines


def get_template_in_directory(
    template_name: str, template_directory: Path, env: jinja2.Environment
) -> jinja2.Template:
    """
    Get template that is in the directory specified by ``file_dunder``

    Parameters
    ----------
    template_name
        Name of the template to get

    template_directory
        The directory from which to retrieve the template.

        If you want to retrieve a template in the same directory as the file
        that is calling this function,
        call ``get_template_in_directory(template_name, Path(__file__).parent), env)``.

    env
        Jinja2 environment to use when loading the template.
        This must be using a :obj:`jinja2.loaders.FileSystemLoader` loader.
        The loader must only have one search path.

    Returns
    -------
        Loaded template
    """
    if not isinstance(env.loader, jinja2.loaders.FileSystemLoader):
        raise NotImplementedError(f"{env.loader=}")

    if len(env.loader.searchpath) > 1:
        raise NotImplementedError(
            f"More than one search path: {env.loader.searchpath=}"
        )

    loader_searchpath = env.loader.searchpath[0]

    template_path = (template_directory / template_name).relative_to(loader_searchpath)

    return env.get_template(str(template_path))


def post_process_jinja_rendering(inp: str) -> str:
    """
    Post-process the result from Jinja

    This fixes things we can't work out how to fix with jinja

    Parameters
    ----------
    inp
        Result of formatting with jinja

    Returns
    -------
        Post-processed result
    """
    # Strip out two blank lines in a row
    two_blank_lines = "\n\n\n"
    one_blank_line = "\n\n"
    while two_blank_lines in inp:
        inp = inp.replace(two_blank_lines, one_blank_line)

    # Jinja trims the trailing line-break from the end of the rendered text,
    # add that back in too
    return inp + "\n"
