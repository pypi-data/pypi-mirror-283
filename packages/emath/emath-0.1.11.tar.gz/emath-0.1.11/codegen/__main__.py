__all__ = ()

# codegen
from codegen import generate_math_files

# python
from pathlib import Path

EMATH_DIR = Path(__file__).parent.parent

if __name__ == "__main__":
    generate_math_files(
        EMATH_DIR / "src/emath",
        EMATH_DIR / "include",
        EMATH_DIR / "doc",
    )
