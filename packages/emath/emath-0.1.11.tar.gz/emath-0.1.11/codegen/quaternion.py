__all__ = ["generate_quaternion_files"]

# codegen
from codegen.template import get_template

# python
from datetime import datetime
from pathlib import Path
from typing import Generator
from typing import Sequence


def generate_quaternion_files(build_dir: Path) -> Generator[str, None, None]:
    types: list[tuple[str, str]] = []
    b = build_dir
    type = generate_matrix_file(b, "double", f"DQuaternion", "d")
    types.append(type)
    yield type[0]
    type = generate_matrix_file(b, "float", f"FQuaternion", "f")
    types.append(type)
    yield type[0]
    generate_quaternion_type_file(build_dir, types)


def generate_quaternion_type_file(build_dir: Path, types: Sequence[tuple[str, str]]) -> None:
    template = get_template("_quaterniontype.hpp")
    with open(build_dir / f"_quaterniontype.hpp", "w") as f:
        f.write(template.render(types=types, when=datetime.utcnow()))


def generate_matrix_file(
    build_dir: Path,
    c_type: str,
    name: str,
    struct_format: str,
) -> tuple[str, str]:
    template = get_template("_quaternion.hpp")
    with open(build_dir / f"_{name.lower()}.hpp", "w") as f:
        f.write(
            template.render(
                name=name, c_type=c_type, struct_format=struct_format, when=datetime.utcnow()
            )
        )
    return name, c_type
