"""Multi-language code parser using tree-sitter.

Replaces Python `ast` for non-Python files. Supports:
  .py, .cpp, .cc, .cxx, .c, .rs, .go, .ts, .js, .h, .hpp

Extracts: functions, classes, constants, imports, call edges.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from tree_sitter import Language, Parser, Query

logger = logging.getLogger("rosclaw.tree_sitter")

# Map language keys to their module import info
_LANGUAGE_SPECS: dict[str, dict[str, str]] = {
    "python": {"module": "tree_sitter_python", "attr": "language"},
    "cpp": {"module": "tree_sitter_cpp", "attr": "language"},
    "c": {"module": "tree_sitter_c", "attr": "language"},
    "rust": {"module": "tree_sitter_rust", "attr": "language"},
    "go": {"module": "tree_sitter_go", "attr": "language"},
    "javascript": {"module": "tree_sitter_javascript", "attr": "language"},
    "typescript": {"module": "tree_sitter_typescript", "attr": "language_typescript"},
}

_EXTENSION_MAP = {
    ".py": "python",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c": "c",
    ".rs": "rust",
    ".go": "go",
    ".ts": "typescript",
    ".js": "javascript",
    ".h": "cpp",
    ".hpp": "cpp",
}

# Tree-sitter queries per language for symbol extraction
_QUERIES: dict[str, dict[str, str]] = {
    "python": {
        "functions": """
            (function_definition name: (identifier) @name)
        """,
        "classes": """
            (class_definition name: (identifier) @name)
        """,
        "constants": """
            (assignment left: (identifier) @name)
            (#match? @name "^[A-Z_][A-Z0-9_]*$")
        """,
        "imports": """
            (import_statement) @imp
            (import_from_statement) @imp
        """,
        "calls": """
            (call function: (identifier) @name)
            (call function: (attribute attribute: (identifier) @name))
        """,
    },
    "cpp": {
        "functions": """
            (function_definition
                declarator: (function_declarator
                    declarator: (identifier) @name))
            (function_definition
                declarator: (function_declarator
                    declarator: (field_identifier) @name))
        """,
        "classes": """
            (class_specifier name: (type_identifier) @name)
            (struct_specifier name: (type_identifier) @name)
        """,
        "constants": """
            (declaration
                declarator: (init_declarator
                    declarator: (identifier) @name))
            (#match? @name "^[A-Z_][A-Z0-9_]*$")
        """,
        "imports": """
            (preproc_include) @imp
            (using_declaration) @imp
        """,
        "calls": """
            (call_expression function: (identifier) @name)
            (call_expression function: (field_expression
                field: (field_identifier) @name))
        """,
    },
    "c": {
        "functions": """
            (function_definition
                declarator: (function_declarator
                    declarator: (identifier) @name))
        """,
        "classes": "",
        "constants": """
            (declaration
                declarator: (init_declarator
                    declarator: (identifier) @name))
            (#match? @name "^[A-Z_][A-Z0-9_]*$")
        """,
        "imports": """
            (preproc_include) @imp
        """,
        "calls": """
            (call_expression function: (identifier) @name)
        """,
    },
    "rust": {
        "functions": """
            (function_item name: (identifier) @name)
        """,
        "classes": """
            (struct_item name: (type_identifier) @name)
            (enum_item name: (type_identifier) @name)
            (trait_item name: (type_identifier) @name)
        """,
        "constants": """
            (const_item name: (identifier) @name)
        """,
        "imports": """
            (use_declaration) @imp
        """,
        "calls": """
            (call_expression function: (identifier) @name)
            (call_expression function: (field_expression
                field: (field_identifier) @name))
        """,
    },
    "go": {
        "functions": """
            (function_declaration name: (identifier) @name)
            (method_declaration name: (field_identifier) @name)
        """,
        "classes": """
            (type_spec name: (type_identifier) @name)
        """,
        "constants": """
            (const_spec name: (identifier) @name)
            (#match? @name "^[A-Z_][A-Z0-9_]*$")
        """,
        "imports": """
            (import_spec) @imp
        """,
        "calls": """
            (call_expression function: (identifier) @name)
            (call_expression function: (selector_expression
                field: (field_identifier) @name))
        """,
    },
    "javascript": {
        "functions": """
            (function_declaration name: (identifier) @name)
            (arrow_function)
            (method_definition name: (property_identifier) @name)
        """,
        "classes": """
            (class_declaration name: (identifier) @name)
        """,
        "constants": """
            (lexical_declaration
                (variable_declarator
                    name: (identifier) @name))
            (#match? @name "^[A-Z_][A-Z0-9_]*$")
        """,
        "imports": """
            (import_statement) @imp
        """,
        "calls": """
            (call_expression function: (identifier) @name)
            (call_expression function: (member_expression
                property: (property_identifier) @name))
        """,
    },
    "typescript": {
        "functions": """
            (function_declaration name: (identifier) @name)
            (method_definition name: (property_identifier) @name)
            (arrow_function)
        """,
        "classes": """
            (class_declaration name: (type_identifier) @name)
            (interface_declaration name: (type_identifier) @name)
        """,
        "constants": """
            (lexical_declaration
                (variable_declarator
                    name: (identifier) @name))
            (#match? @name "^[A-Z_][A-Z0-9_]*$")
        """,
        "imports": """
            (import_statement) @imp
        """,
        "calls": """
            (call_expression function: (identifier) @name)
            (call_expression function: (member_expression
                property: (property_identifier) @name))
        """,
    },
}


class MultiLanguageParser:
    """Parse multiple programming languages with tree-sitter."""

    _instance: "MultiLanguageParser | None" = None

    def __new__(cls) -> "MultiLanguageParser":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._languages: dict[str, Language] = {}
            cls._instance._parsers: dict[str, Parser] = {}
            cls._instance._init_languages()
        return cls._instance

    def __init__(self) -> None:
        # __new__ handles actual initialization; __init__ is a no-op for singleton
        pass

    def _init_languages(self) -> None:
        for lang, spec in _LANGUAGE_SPECS.items():
            try:
                mod = __import__(spec["module"])
                lang_func = getattr(mod, spec["attr"])
                language = Language(lang_func())
                self._languages[lang] = language
                self._parsers[lang] = Parser(language)
            except Exception as exc:
                logger.warning("Failed to load tree-sitter language %s: %s", lang, exc)

    def detect_language(self, file_path: str) -> str:
        ext = Path(file_path).suffix.lower()
        return _EXTENSION_MAP.get(ext, "unknown")

    def parse_file(self, file_path: str) -> dict[str, Any]:
        """Parse a code file and return structured symbols."""
        lang = self.detect_language(file_path)
        if lang == "unknown" or lang not in self._parsers:
            return {"error": f"Unsupported language: {lang}", "language": lang}

        try:
            source = Path(file_path).read_bytes()
        except Exception as exc:
            return {"error": str(exc), "language": lang}

        tree = self._parsers[lang].parse(source)
        return self._extract_symbols(tree.root_node, source, lang, file_path)

    def _extract_symbols(
        self, root_node: Any, source: bytes, lang: str, file_path: str
    ) -> dict[str, Any]:
        result: dict[str, Any] = {
            "language": lang,
            "file": file_path,
            "functions": [],
            "classes": [],
            "constants": [],
            "imports": [],
            "calls": [],
        }
        language = self._languages.get(lang)
        if language is None:
            return result

        queries = _QUERIES.get(lang, {})

        def _run_query(query_text: str, capture_key: str) -> list[dict[str, Any]]:
            if not query_text:
                return []
            items: list[dict[str, Any]] = []
            try:
                q = Query(language, query_text)
                captures = q.captures(root_node)
                for node in captures.get("name", []):
                    name = source[node.start_byte:node.end_byte].decode("utf-8", errors="ignore")
                    lineno = source[:node.start_byte].count(b"\n") + 1
                    items.append({"name": name, "lineno": lineno})
            except Exception as exc:
                logger.debug("Query failed for %s (%s): %s", file_path, capture_key, exc)
            return items

        def _run_query_text(query_text: str, capture_key: str) -> list[dict[str, Any]]:
            if not query_text:
                return []
            items: list[dict[str, Any]] = []
            try:
                q = Query(language, query_text)
                captures = q.captures(root_node)
                for node in captures.get("imp", []):
                    text = source[node.start_byte:node.end_byte].decode("utf-8", errors="ignore")
                    lineno = source[:node.start_byte].count(b"\n") + 1
                    items.append({"text": text[:100], "lineno": lineno})
            except Exception as exc:
                logger.debug("Query failed for %s (%s): %s", file_path, capture_key, exc)
            return items

        result["functions"] = _run_query(queries.get("functions", ""), "functions")
        result["classes"] = _run_query(queries.get("classes", ""), "classes")
        result["constants"] = _run_query(queries.get("constants", ""), "constants")
        result["imports"] = _run_query_text(queries.get("imports", ""), "imports")

        # Extract calls
        if queries.get("calls"):
            try:
                q = Query(language, queries["calls"])
                captures = q.captures(root_node)
                for node in captures.get("name", []):
                    name = source[node.start_byte:node.end_byte].decode("utf-8", errors="ignore")
                    lineno = source[:node.start_byte].count(b"\n") + 1
                    result["calls"].append({"target": name, "lineno": lineno})
            except Exception as exc:
                logger.debug("Call query failed for %s: %s", file_path, exc)

        return result

    def supported_languages(self) -> list[str]:
        return list(self._parsers.keys())


def parse_code_file(file_path: str) -> dict[str, Any]:
    """Convenience function: parse a single code file."""
    parser = MultiLanguageParser()
    return parser.parse_file(file_path)


def scan_directory(directory: str) -> list[dict[str, Any]]:
    """Scan a directory for all supported code files."""
    parser = MultiLanguageParser()
    results: list[dict[str, Any]] = []
    root = Path(directory)
    supported_exts = set(_EXTENSION_MAP.keys())

    for file_path in root.rglob("*"):
        if file_path.suffix.lower() in supported_exts:
            result = parser.parse_file(str(file_path))
            if "error" not in result:
                results.append(result)

    return results


__all__ = ["MultiLanguageParser", "parse_code_file", "scan_directory"]
