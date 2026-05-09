"""Tests for tree_sitter_parser.py — multi-language AST parsing."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from tree_sitter_parser import MultiLanguageParser, parse_code_file, scan_directory


@pytest.fixture
def parser() -> MultiLanguageParser:
    return MultiLanguageParser()


# ── Basic infrastructure ──


def test_singleton_pattern(parser: MultiLanguageParser) -> None:
    p2 = MultiLanguageParser()
    assert parser is p2


def test_detect_language(parser: MultiLanguageParser) -> None:
    assert parser.detect_language("foo.py") == "python"
    assert parser.detect_language("foo.cpp") == "cpp"
    assert parser.detect_language("foo.cc") == "cpp"
    assert parser.detect_language("foo.cxx") == "cpp"
    assert parser.detect_language("foo.c") == "c"
    assert parser.detect_language("foo.rs") == "rust"
    assert parser.detect_language("foo.go") == "go"
    assert parser.detect_language("foo.ts") == "typescript"
    assert parser.detect_language("foo.js") == "javascript"
    assert parser.detect_language("foo.h") == "cpp"
    assert parser.detect_language("foo.hpp") == "cpp"
    assert parser.detect_language("foo.txt") == "unknown"


def test_supported_languages(parser: MultiLanguageParser) -> None:
    langs = parser.supported_languages()
    assert "python" in langs
    assert "cpp" in langs


def test_parse_unsupported_file(parser: MultiLanguageParser) -> None:
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
        f.write("hello")
        path = f.name
    result = parser.parse_file(path)
    Path(path).unlink()
    assert "error" in result
    assert result["language"] == "unknown"


def test_parse_missing_file(parser: MultiLanguageParser) -> None:
    result = parser.parse_file("/nonexistent/file.py")
    assert "error" in result


# ── Python parsing ──


PYTHON_SAMPLE = '''\
"""Demo module."""

import os
from typing import List

MAX_TORQUE = 10.5  # N·m

class RobotArm:
    """A robot arm."""

    def move(self, angle: float) -> None:
        pass

    def _private(self) -> None:
        pass

def helper() -> None:
    move(1.0)
    arm = RobotArm()
    arm.move(2.0)
'''


def test_parse_python_file(parser: MultiLanguageParser) -> None:
    if "python" not in parser.supported_languages():
        pytest.skip("tree-sitter-python not available")

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write(PYTHON_SAMPLE)
        path = f.name

    result = parser.parse_file(path)
    Path(path).unlink()

    assert result["language"] == "python"
    assert result["file"] == path
    funcs = [fn["name"] for fn in result["functions"]]
    assert "move" in funcs
    assert "helper" in funcs

    classes = [cls["name"] for cls in result["classes"]]
    assert "RobotArm" in classes

    consts = [c["name"] for c in result["constants"]]
    assert "MAX_TORQUE" in consts

    imports = result["imports"]
    assert len(imports) >= 1

    calls = [c["target"] for c in result["calls"]]
    assert "move" in calls


def test_parse_python_via_module_function() -> None:
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write("def foo(): pass\n")
        path = f.name

    result = parse_code_file(path)
    Path(path).unlink()
    if "error" in result:
        pytest.skip("tree-sitter-python not available")
    funcs = [fn["name"] for fn in result["functions"]]
    assert "foo" in funcs


# ── C++ parsing ──


CPP_SAMPLE = '''\
#include <iostream>

#define MAX_FORCE 100.0

class Manipulator {
public:
    void setVelocity(double v);
    double getVelocity() const;
private:
    double velocity_;
};

void Manipulator::setVelocity(double v) {
    velocity_ = v;
}

double globalHelper() {
    return 0.0;
}
'''


def test_parse_cpp_file(parser: MultiLanguageParser) -> None:
    if "cpp" not in parser.supported_languages():
        pytest.skip("tree-sitter-cpp not available")

    with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False, mode="w") as f:
        f.write(CPP_SAMPLE)
        path = f.name

    result = parser.parse_file(path)
    Path(path).unlink()

    assert result["language"] == "cpp"
    funcs = [fn["name"] for fn in result["functions"]]
    assert "setVelocity" in funcs or "getVelocity" in funcs or "globalHelper" in funcs

    classes = [cls["name"] for cls in result["classes"]]
    assert "Manipulator" in classes


def test_parse_header_file(parser: MultiLanguageParser) -> None:
    if "cpp" not in parser.supported_languages():
        pytest.skip("tree-sitter-cpp not available")

    with tempfile.NamedTemporaryFile(suffix=".h", delete=False, mode="w") as f:
        f.write("class Sensor {};\n")
        path = f.name

    result = parser.parse_file(path)
    Path(path).unlink()
    assert result["language"] == "cpp"


# ── Go parsing ──


GO_SAMPLE = '''\
package main

import "fmt"

const MaxSpeed = 100

type Robot struct {
    Name string
}

func (r *Robot) Move() {
    fmt.Println("moving")
}

func helper() int {
    return 0
}
'''


def test_parse_go_file(parser: MultiLanguageParser) -> None:
    if "go" not in parser.supported_languages():
        pytest.skip("tree-sitter-go not available")

    with tempfile.NamedTemporaryFile(suffix=".go", delete=False, mode="w") as f:
        f.write(GO_SAMPLE)
        path = f.name

    result = parser.parse_file(path)
    Path(path).unlink()

    assert result["language"] == "go"
    funcs = [fn["name"] for fn in result["functions"]]
    assert "Move" in funcs or "helper" in funcs

    classes = [cls["name"] for cls in result["classes"]]
    assert "Robot" in classes

    consts = [c["name"] for c in result["constants"]]
    assert "MaxSpeed" in consts


# ── TypeScript parsing ──


TS_SAMPLE = '''\
import { Robot } from './robot';

const MAX_ACCEL = 5.0;

class Controller {
    update(target: number): void {
        console.log(target);
    }
}

function reset(): void {
    return;
}
'''


def test_parse_typescript_file(parser: MultiLanguageParser) -> None:
    if "typescript" not in parser.supported_languages():
        pytest.skip("tree-sitter-typescript not available")

    with tempfile.NamedTemporaryFile(suffix=".ts", delete=False, mode="w") as f:
        f.write(TS_SAMPLE)
        path = f.name

    result = parser.parse_file(path)
    Path(path).unlink()

    assert result["language"] == "typescript"
    funcs = [fn["name"] for fn in result["functions"]]
    assert "update" in funcs or "reset" in funcs

    classes = [cls["name"] for cls in result["classes"]]
    assert "Controller" in classes

    consts = [c["name"] for c in result["constants"]]
    assert "MAX_ACCEL" in consts


# ── JavaScript parsing ──


JS_SAMPLE = '''\
const MAX_DEPTH = 10;

class Arm {
    extend() {
        this.move();
    }

    move() {
        console.log('move');
    }
}

function init() {
    return new Arm();
}
'''


def test_parse_javascript_file(parser: MultiLanguageParser) -> None:
    if "javascript" not in parser.supported_languages():
        pytest.skip("tree-sitter-javascript not available")

    with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode="w") as f:
        f.write(JS_SAMPLE)
        path = f.name

    result = parser.parse_file(path)
    Path(path).unlink()

    assert result["language"] == "javascript"
    funcs = [fn["name"] for fn in result["functions"]]
    assert "extend" in funcs or "move" in funcs or "init" in funcs

    classes = [cls["name"] for cls in result["classes"]]
    assert "Arm" in classes

    consts = [c["name"] for c in result["constants"]]
    assert "MAX_DEPTH" in consts


# ── Directory scanning ──


def test_scan_directory(parser: MultiLanguageParser) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        Path(tmpdir, "a.py").write_text("def foo(): pass\n")
        Path(tmpdir, "b.js").write_text("function bar() {}\n")
        Path(tmpdir, "readme.txt").write_text("hello\n")

        results = scan_directory(tmpdir)
        paths = [r["file"] for r in results]
        assert any("a.py" in p for p in paths)
        assert any("b.js" in p for p in paths)
        assert not any("readme.txt" in p for p in paths)


# ── Result shape ──


def test_result_has_expected_keys(parser: MultiLanguageParser) -> None:
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write("x = 1\n")
        path = f.name

    result = parser.parse_file(path)
    Path(path).unlink()
    if "error" in result:
        pytest.skip("python parser not available")

    for key in ("language", "file", "functions", "classes", "constants", "imports", "calls"):
        assert key in result

    assert isinstance(result["functions"], list)
    assert isinstance(result["classes"], list)
    assert isinstance(result["constants"], list)
    assert isinstance(result["imports"], list)
    assert isinstance(result["calls"], list)


# ── Call extraction ──


def test_python_call_extraction(parser: MultiLanguageParser) -> None:
    if "python" not in parser.supported_languages():
        pytest.skip("tree-sitter-python not available")

    code = "foo()\nbar.baz()\n"
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write(code)
        path = f.name

    result = parser.parse_file(path)
    Path(path).unlink()

    targets = [c["target"] for c in result["calls"]]
    assert "foo" in targets
    assert "baz" in targets


def test_javascript_call_extraction(parser: MultiLanguageParser) -> None:
    if "javascript" not in parser.supported_languages():
        pytest.skip("tree-sitter-javascript not available")

    code = "foo();\nobj.method();\n"
    with tempfile.NamedTemporaryFile(suffix=".js", delete=False, mode="w") as f:
        f.write(code)
        path = f.name

    result = parser.parse_file(path)
    Path(path).unlink()

    targets = [c["target"] for c in result["calls"]]
    assert "foo" in targets
    assert "method" in targets


# ── Line numbers present ──


def test_lineno_present(parser: MultiLanguageParser) -> None:
    if "python" not in parser.supported_languages():
        pytest.skip("tree-sitter-python not available")

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as f:
        f.write("\n\ndef foo():\n    pass\n")
        path = f.name

    result = parser.parse_file(path)
    Path(path).unlink()

    for fn in result["functions"]:
        assert "lineno" in fn
        assert isinstance(fn["lineno"], int)
        assert fn["lineno"] > 0
