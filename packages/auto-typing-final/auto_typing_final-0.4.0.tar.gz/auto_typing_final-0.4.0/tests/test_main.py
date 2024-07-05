import pytest

from auto_typing_final.transform import transform_file_content


@pytest.mark.parametrize(
    ("before", "after"),
    [
        # Add annotation
        ("a: int", "a: int"),
        ("a = 1", "a: typing.Final = 1"),
        ("a: typing.Final = 1", "a: typing.Final = 1"),
        ("a: int = 1", "a: typing.Final[int] = 1"),
        ("a: typing.Annotated[int, 'hello'] = 1", "a: typing.Final[typing.Annotated[int, 'hello']] = 1"),
        ("b = 1\na = 2\nb = 3", "b = 1\na: typing.Final = 2\nb = 3"),
        ("b = 1\nb = 2\na = 3", "b = 1\nb = 2\na: typing.Final = 3"),
        ("a = 1\nb = 2\nb = 3", "a: typing.Final = 1\nb = 2\nb = 3"),
        ("a = 1\na = 2\nb: int", "a = 1\na = 2\nb: int"),
        ("a = 1\na: int", "a = 1\na: int"),
        ("a: int\na = 1", "a: int\na = 1"),
        ("a: typing.Final\na = 1", "a: typing.Final\na = 1"),
        ("a: int\na: int = 1", "a: int\na: int = 1"),
        ("a, b = 1, 2", "a, b = 1, 2"),
        ("(a, b) = 1, 2", "(a, b) = 1, 2"),
        ("(a, b) = t()", "(a, b) = t()"),
        ("[a, b] = t()", "[a, b] = t()"),
        ("[a] = t()", "[a] = t()"),
        # Remove annotation
        ("a = 1\na: typing.Final[int] = 2", "a = 1\na: int = 2"),
        ("a = 1\na: typing.Final = 2", "a = 1\na = 2"),
        ("a: int = 1\na: typing.Final[int] = 2", "a: int = 1\na: int = 2"),
        ("a: int = 1\na: typing.Final = 2", "a: int = 1\na = 2"),
        ("a: typing.Final = 1\na: typing.Final = 2\na = 3\na: int = 4", "a = 1\na = 2\na = 3\na: int = 4"),
        # Both
        ("a = 1\nb = 2\nb: typing.Final[int] = 3", "a: typing.Final = 1\nb = 2\nb: int = 3"),
    ],
)
def test_variants(before: str, after: str) -> None:
    source = f"""
import typing

def foo():
{"\n".join(f"    {line}" for line in before.splitlines())}
"""

    after_source = f"""
import typing

def foo():
{"\n".join(f"    {line}" for line in after.splitlines())}
"""
    assert transform_file_content(source.strip()) == after_source.strip()


@pytest.mark.parametrize(
    "case",
    [
        """
a = 1
---
a = 1
""",
        """
def foo():
    a = 1
---
def foo():
    a: typing.Final = 1
""",
        """
a = 1

def foo():
    a = 2

    def bar():
        a = 3
---
a = 1

def foo():
    a: typing.Final = 2

    def bar():
        a: typing.Final = 3
""",
        """
a = 1

def foo():
    global a
    a = 2
---
a = 1

def foo():
    global a
    a = 2
""",
        """
def foo():
    from b import bar
    baz = 1
---
def foo():
    from b import bar
    baz: typing.Final = 1
""",
        """
def foo():
    from b import bar as baz
    bar = 1
    baz = 1
---
def foo():
    from b import bar as baz
    bar: typing.Final = 1
    baz = 1
""",
        """
def foo():
    from b import bar
    bar: typing.Final = 1
---
def foo():
    from b import bar
    bar = 1
""",
        """
def foo():
    import bar
    bar: typing.Final = 1
---
def foo():
    import bar
    bar = 1
""",
        """
def foo():
    import baz
    bar: typing.Final = 1
---
def foo():
    import baz
    bar: typing.Final = 1
""",
        """
def foo():
    from b import bar, baz
    bar = 1
    baz = 1
---
def foo():
    from b import bar, baz
    bar = 1
    baz = 1
""",
        """
def foo():
    from b import bar, baz as bazbaz
    bar = 1
    baz = 1
---
def foo():
    from b import bar, baz as bazbaz
    bar = 1
    baz: typing.Final = 1
""",
        """
def foo():
    # Dotted paths are not allowed, but tree-sitter-python grammar permits it
    from b import d.bar, bazbaz as baz
    bar = 1
    baz = 1
---
def foo():
    # Dotted paths are not allowed, but tree-sitter-python grammar permits it
    from b import d.bar, bazbaz as baz
    bar = 1
    baz = 1
""",
        """
def foo():
    from b import (bar, bazbaz)
    bar = 1
    baz = 1
---
def foo():
    from b import (bar, bazbaz)
    bar = 1
    baz: typing.Final = 1
""",
        """
def foo():
    a: typing.Final = 1
    a += 1
---
def foo():
    a = 1
    a += 1
""",
        """
def foo():
    a: typing.Final = 1
    a: int
---
def foo():
    a = 1
    a: int
""",
        """
def foo():
    a: typing.Final = 1
    a: typing.Final
---
def foo():
    a = 1
    a: typing.Final
""",
        """
def foo():
    a, b = 1
---
def foo():
    a, b = 1
""",
        """
def foo():
    a: typing.Final = 1
    b: typing.Final = 2
    a, b = 3
---
def foo():
    a = 1
    b = 2
    a, b = 3
""",
        """
def foo():
    a: typing.Final = 1
    b, c = 2
---
def foo():
    a: typing.Final = 1
    b, c = 2
""",
        """
def foo():
    a, b: typing.Final = 1
---
def foo():
    a, b: typing.Final = 1
""",
        """
def foo():
    a: typing.Final = 1
    (a, b) = 2
---
def foo():
    a = 1
    (a, b) = 2
""",
        """
def foo():
    a: typing.Final = 1
    (a, *other) = 2
---
def foo():
    a = 1
    (a, *other) = 2
""",
        """
def foo():
    def a(): ...
    a: typing.Final = 1
---
def foo():
    def a(): ...
    a = 1
""",
        """
def foo():
    class a: ...
    a: typing.Final = 1
---
def foo():
    class a: ...
    a = 1
""",
        """
def foo():
    a: typing.Final = 1
    if a := 1: ...
---
def foo():
    a = 1
    if a := 1: ...
""",
        """
def foo():
    while True:
        a = 1
---
def foo():
    while True:
        a = 1
""",
        """
def foo():
    while True:
        a: typing.Final = 1
---
def foo():
    while True:
        a = 1
""",
        """
def foo():
    for _ in ...:
        a: typing.Final = 1
---
def foo():
    for _ in ...:
        a = 1
""",
        """
def foo():
    for _ in ...:
        def foo():
            a: typing.Final = 1
---
def foo():
    for _ in ...:
        def foo():
            a = 1
""",
        """
def foo():
    a: typing.Final = 1
    b: typing.Final = 2

    for _ in ...:
        a: typing.Final = 1
---
def foo():
    a = 1
    b: typing.Final = 2

    for _ in ...:
        a = 1
""",
        """
def foo():
    for _ in ...:
        a = 1
---
def foo():
    for _ in ...:
        a = 1
""",
        """
def foo():
    a: typing.Final = 1
    for a in ...: ...
---
def foo():
    a = 1
    for a in ...: ...
""",
        """
def foo():
    a: typing.Final = 1

    match ...:
        case ...: ...
---
def foo():
    a: typing.Final = 1

    match ...:
        case ...: ...
""",
        """
def foo():
    a: typing.Final = 1

    match ...:
        case [] as a: ...
---
def foo():
    a = 1

    match ...:
        case [] as a: ...
""",
        """
def foo():
    a: typing.Final = 1

    match ...:
        case {"hello": a, **b}: ...
---
def foo():
    a = 1

    match ...:
        case {"hello": a, **b}: ...
""",
        """
def foo():
    a: typing.Final = 1

    match ...:
        case {**a}: ...
---
def foo():
    a = 1

    match ...:
        case {**a}: ...
""",
        """
def foo():
    a: typing.Final = 1

    match ...:
        case A(b=a) | B(b=a): ...
---
def foo():
    a = 1

    match ...:
        case A(b=a) | B(b=a): ...
""",
        """
def foo():
    a: typing.Final = 1

    match ...:
        case [b, *a]: ...
---
def foo():
    a = 1

    match ...:
        case [b, *a]: ...
""",
        """
def foo():
    a: typing.Final = 1

    match ...:
        case [a]: ...
---
def foo():
    a = 1

    match ...:
        case [a]: ...
""",
        """
def foo():
    a: typing.Final = 1

    match ...:
        case (a,): ...
---
def foo():
    a = 1

    match ...:
        case (a,): ...
""",
        """
def foo():
    a: typing.Final = 1
    nonlocal a
---
def foo():
    a = 1
    nonlocal a
""",
        """
def foo():
    a = 1
    nonlocal a
---
def foo():
    a = 1
    nonlocal a
""",
        """
def foo():
    a: typing.Final = 1
    global b
---
def foo():
    a: typing.Final = 1
    global b
""",
        """
def foo():
    a: typing.Final = 1
    global a
---
def foo():
    a = 1
    global a
""",
        """
def foo():
    a: typing.Final = 1
    b: typing.Final = 2
    c: typing.Final = 3

    def bar():
        nonlocal a
        b: typing.Final = 4
        c: typing.Final = 5

        class C:
            a = 6
            c = 7

            def baz():
                nonlocal a, b
                b: typing.Final = 8
                c: typing.Final = 9
---
def foo():
    a = 1
    b: typing.Final = 2
    c: typing.Final = 3

    def bar():
        nonlocal a
        b = 4
        c: typing.Final = 5

        class C:
            a = 6
            c = 7

            def baz():
                nonlocal a, b
                b = 8
                c: typing.Final = 9
""",
        """
def foo():
    foo = 1
---
def foo():
    foo: typing.Final = 1
""",
        """
def foo(a, b: int, c=1, d: int = 2):
    a: typing.Final = 1
    b: typing.Final = 2
    c: typing.Final = 3
    d: typing.Final = 4
    e: typing.Final = 5
---
def foo(a, b: int, c=1, d: int = 2):
    a = 1
    b = 2
    c = 3
    d = 4
    e: typing.Final = 5
""",
        """
def foo(self):
    self.me = 1
---
def foo(self):
    self.me = 1
""",
        """
a.b = 1
---
a.b = 1
""",
    ],
)
def test_transform_file_content(case: str) -> None:
    before, _, after = case.partition("---")
    assert transform_file_content("import typing\n" + before.strip()) == "import typing\n" + after.strip()


@pytest.mark.parametrize(
    "case",
    [
        """
import typing
a = 1
---
import typing
a = 1
""",
        """
import typing
a: typing.Final = 1
---
import typing
a: typing.Final = 1
""",
        """
a: typing.Final = 1
---
a: typing.Final = 1
""",
        """
a: typing.Final = 1
a = 2
---
a: typing.Final = 1
a = 2
""",
    ],
)
def test_add_import(case: str) -> None:
    before, _, after = case.partition("---")
    assert transform_file_content(before.strip()) == after.strip()
