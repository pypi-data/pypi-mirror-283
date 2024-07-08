__all__ = ["generate_pod_files"]

# codegen
from codegen.template import get_template

# python
from datetime import datetime
from pathlib import Path
from typing import Generator
from typing import Sequence


def generate_pod_files(build_dir: Path) -> Generator[str, None, None]:
    types: list[tuple[str, str]] = []
    b = build_dir
    types.append(generate_pod_file(b, "bool", "B", "?"))
    types.append(generate_pod_file(b, "double", "D", "d"))
    types.append(generate_pod_file(b, "float", "F", "f"))
    types.append(generate_pod_file(b, "int8_t", "I8", "=b"))
    types.append(generate_pod_file(b, "uint8_t", "U8", "=B"))
    types.append(generate_pod_file(b, "int16_t", "I16", "=h"))
    types.append(generate_pod_file(b, "uint16_t", "U16", "=H"))
    types.append(generate_pod_file(b, "int32_t", "I32", "=i"))
    types.append(generate_pod_file(b, "uint32_t", "U32", "=I"))
    types.append(generate_pod_file(b, "int", "I", "i"))
    types.append(generate_pod_file(b, "unsigned int", "U", "I"))
    types.append(generate_pod_file(b, "int64_t", "I64", "=q"))
    types.append(generate_pod_file(b, "uint64_t", "U64", "=Q"))
    yield from (t[0] for t in types)
    generate_pod_type_file(build_dir, types)


def generate_pod_type_file(build_dir: Path, types: Sequence[tuple[str, str]]) -> None:
    template = get_template("_podtype.hpp")
    with open(build_dir / f"_podtype.hpp", "w") as f:
        f.write(template.render(types=types, when=datetime.utcnow()))


def generate_pod_file(
    build_dir: Path,
    c_type: str,
    name: str,
    struct_format: str,
) -> tuple[str, str]:
    template = get_template("_pod.hpp")
    with open(build_dir / f"_{name.lower()}.hpp", "w") as f:
        f.write(
            template.render(
                name=name, c_type=c_type, struct_format=struct_format, when=datetime.utcnow()
            )
        )
    return name, c_type
