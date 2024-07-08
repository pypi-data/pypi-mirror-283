__all__ = ["generate_matrix_files"]

# codegen
from codegen.template import get_template

# python
from datetime import datetime
from pathlib import Path
from typing import Generator
from typing import Sequence


def generate_matrix_files(build_dir: Path) -> Generator[str, None, None]:
    types: list[tuple[str, int, int, str]] = []
    b = build_dir
    for r in range(2, 5):
        for c in range(2, 5):
            type = generate_matrix_file(
                b, "double", r, c, f"DMatrix{r}x{c}", "d", f"DVector{c}", f"DVector{r}"
            )
            types.append(type)
            yield type[0]
            type = generate_matrix_file(
                b, "float", r, c, f"FMatrix{r}x{c}", "f", f"FVector{c}", f"FVector{r}"
            )
            types.append(type)
            yield type[0]
    generate_matrix_type_file(build_dir, types)


def generate_matrix_type_file(build_dir: Path, types: Sequence[tuple[str, int, int, str]]) -> None:
    template = get_template("_matrixtype.hpp")
    with open(build_dir / f"_matrixtype.hpp", "w") as f:
        f.write(template.render(types=types, when=datetime.utcnow()))


def generate_matrix_file(
    build_dir: Path,
    c_type: str,
    row_size: int,
    column_size: int,
    name: str,
    struct_format: str,
    column_type: str,
    row_type: str,
) -> tuple[str, int, int, str]:
    template = get_template("_matrix.hpp")
    with open(build_dir / f"_{name.lower()}.hpp", "w") as f:
        f.write(
            template.render(
                name=name,
                row_size=row_size,
                column_size=column_size,
                component_count=row_size * column_size,
                c_type=c_type,
                struct_format=struct_format,
                column_type=column_type,
                row_type=row_type,
                when=datetime.utcnow(),
            )
        )
    return name, column_size, row_size, c_type
