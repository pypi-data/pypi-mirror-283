from importlib import import_module
from typing import Callable, Literal, Union, cast

from tree_sitter import Language, Parser
from tree_sitter_c_sharp import language as c_sharp_language
from tree_sitter_embedded_template import language as embedded_template_language
from tree_sitter_php import language_php as php_language
from tree_sitter_typescript import language_tsx, language_typescript
from tree_sitter_xml import language_dtd as dtd_language
from tree_sitter_xml import language_xml as xml_language
from tree_sitter_yaml import language as yaml_language

InstalledBindings = Literal[
    "csharp",
    "dtd",
    "embeddedtemplate",
    "php",
    "tsx",
    "typescript",
    "xml",
    "yaml",
]
SupportedLanguage = Union[
    Literal[
        "actionscript",
        "ada",
        "agda",
        "arduino",
        "asm",
        "astro",
        "bash",
        "beancount",
        "bibtex",
        "bicep",
        "bitbake",
        "c",
        "cairo",
        "capnp",
        "chatito",
        "clarity",
        "clojure",
        "cmake",
        "comment",
        "commonlisp",
        "cpon",
        "cpp",
        "css",
        "csv",
        "cuda",
        "d",
        "dart",
        "dockerfile",
        "doxygen",
        "elisp",
        "elixir",
        "elm",
        "erlang",
        "fennel",
        "firrtl",
        "fish",
        "fortran",
        "func",
        "gdscript",
        "gitattributes",
        "gitcommit",
        "gitignore",
        "gleam",
        "glsl",
        "gn",
        "go",
        "gomod",
        "gosum",
        "groovy",
        "gstlaunch",
        "hack",
        "hare",
        "haskell",
        "haxe",
        "hcl",
        "heex",
        "hlsl",
        "html",
        "hyprlang",
        "ispc",
        "janet",
        "java",
        "javascript",
        "jsdoc",
        "json",
        "jsonnet",
        "julia",
        "kconfig",
        "kdl",
        "kotlin",
        "latex",
        "linkerscript",
        "llvm",
        "lua",
        "luadoc",
        "luap",
        "luau",
        "magik",
        "make",
        "markdown",
        "matlab",
        "mermaid",
        "meson",
        "ninja",
        "nix",
        "nqc",
        "objc",
        "odin",
        "org",
        "pascal",
        "pem",
        "perl",
        "pgn",
        "po",
        "pony",
        "powershell",
        "printf",
        "prisma",
        "properties",
        "psv",
        "puppet",
        "purescript",
        "pymanifest",
        "python",
        "qmldir",
        "qmljs",
        "query",
        "r",
        "racket",
        "re2c",
        "readline",
        "requirements",
        "ron",
        "rst",
        "ruby",
        "rust",
        "scala",
        "scheme",
        "scss",
        "smali",
        "smithy",
        "solidity",
        "sql",
        "squirrel",
        "starlark",
        "svelte",
        "swift",
        "tablegen",
        "tcl",
        "terraform",
        "test",
        "thrift",
        "toml",
        "tsv",
        "twig",
        "typst",
        "udev",
        "ungrammar",
        "uxntal",
        "v",
        "verilog",
        "vhdl",
        "vim",
        "vue",
        "wgsl",
        "xcompose",
        "yuck",
        "zig",
    ],
    InstalledBindings,
]

installed_bindings_map: dict[InstalledBindings, Callable[[], int]] = {
    "csharp": c_sharp_language,
    "dtd": dtd_language,
    "embeddedtemplate": embedded_template_language,
    "php": php_language,
    "tsx": language_tsx,
    "typescript": language_typescript,
    "xml": xml_language,
    "yaml": yaml_language,
}


def get_binding(language_name: SupportedLanguage) -> int:
    """Get the binding for the given language name.

    Args:
        language_name (SupportedLanguage): The name of the language.

    Raises:
        LookupError: If the language is not found.

    Returns:
        int: The binding for the language.
    """
    if language_name in installed_bindings_map:
        return installed_bindings_map[cast(InstalledBindings, language_name)]()

    try:
        module = import_module(name=f".bindings.{language_name}", package=__package__)
        return cast(int, module.language())
    except ModuleNotFoundError as e:
        raise LookupError(f"Language not found: {language_name}") from e


def get_language(language_name: SupportedLanguage) -> Language:
    """Get the language with the given name.

    Args:
        language_name (SupportedLanguage): The name of the language.

    Raises:
        LookupError: If the language is not found.

    Returns:
        Language: The language as a tree-sitter Language instance.
    """
    binding = get_binding(language_name)
    return Language(binding)


def get_parser(language_name: SupportedLanguage) -> Parser:
    """Get a parser for the given language name.

    Args:
        language_name (SupportedLanguage): The name of the language.

    Raises:
        LookupError: If the language is not found.

    Returns:
        Parser: The parser for the language as a tree-sitter Parser instance.
    """
    return Parser(get_language(language_name=language_name))


__all__ = ["get_language", "get_parser", "SupportedLanguage"]
