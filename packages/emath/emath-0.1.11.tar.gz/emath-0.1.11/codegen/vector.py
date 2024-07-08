__all__ = ["generate_vector_files"]

# codegen
from codegen.template import get_template

# python
from datetime import datetime
from pathlib import Path
from typing import Generator
from typing import Sequence


def generate_vector_files(build_dir: Path, doc_dir: Path) -> Generator[str, None, None]:
    types: list[tuple[str, int, str]] = []
    b = build_dir
    d = doc_dir
    for i in range(1, 5):
        types.append(_generate_vector_files(b, d, "bool", i, f"BVector{i}", "?"))
        types.append(_generate_vector_files(b, d, "double", i, f"DVector{i}", "d"))
        types.append(_generate_vector_files(b, d, "float", i, f"FVector{i}", "f"))
        types.append(_generate_vector_files(b, d, "int8_t", i, f"I8Vector{i}", "=b"))
        types.append(_generate_vector_files(b, d, "uint8_t", i, f"U8Vector{i}", "=B"))
        types.append(_generate_vector_files(b, d, "int16_t", i, f"I16Vector{i}", "=h"))
        types.append(_generate_vector_files(b, d, "uint16_t", i, f"U16Vector{i}", "=H"))
        types.append(_generate_vector_files(b, d, "int32_t", i, f"I32Vector{i}", "=i"))
        types.append(_generate_vector_files(b, d, "uint32_t", i, f"U32Vector{i}", "=I"))
        types.append(_generate_vector_files(b, d, "int", i, f"IVector{i}", "i"))
        types.append(_generate_vector_files(b, d, "unsigned int", i, f"UVector{i}", "I"))
        types.append(_generate_vector_files(b, d, "int64_t", i, f"I64Vector{i}", "=q"))
        types.append(_generate_vector_files(b, d, "uint64_t", i, f"U64Vector{i}", "=Q"))
    yield from (t[0] for t in types)
    generate_vector_type_file(build_dir, types)


def generate_vector_type_file(build_dir: Path, types: Sequence[tuple[str, int, str]]) -> None:
    template = get_template("_vectortype.hpp")
    with open(build_dir / f"_vectortype.hpp", "w") as f:
        f.write(template.render(types=types, when=datetime.utcnow()))


def _generate_vector_files(
    build_dir: Path,
    doc_dir: Path,
    c_type: str,
    component_count: int,
    name: str,
    struct_format: str,
) -> tuple[str, int, str]:
    template = get_template("_vector.hpp")
    with open(build_dir / f"_{name.lower()}.hpp", "w") as f:
        f.write(
            template.render(
                name=name,
                component_count=component_count,
                c_type=c_type,
                struct_format=struct_format,
            )
        )
    template = get_template("api_vector.rst")
    with open(doc_dir / f"api_{name.lower()}.rst", "w") as f:
        f.write(
            template.render(
                name=name,
                component_count=component_count,
                c_type=c_type,
                struct_format=struct_format,
            )
        )
    template = get_template("api_vector_array.rst")
    with open(doc_dir / f"api_{name.lower()}_array.rst", "w") as f:
        f.write(
            template.render(
                name=name,
                component_count=component_count,
                c_type=c_type,
                struct_format=struct_format,
            )
        )
    return name, component_count, c_type
