import shutil
from pathlib import Path
from typing import Union

from pandas import Series

from .register import register_series_accessor


@register_series_accessor("unix")
class UnixAccessor:
    """Custom accessor for Unix-like file operations on pandas Series."""

    def __init__(self, ser: Series):
        self._validate(ser)
        self._ser = ser.map(Path)

    @staticmethod
    def _validate(ser: Series) -> None:
        if not ser.map(lambda x: isinstance(x, (Path, str))).all():
            raise ValueError("All elements must be Path or str objects")

    @staticmethod
    def _validate_dest(dest: Union[Path, str]) -> Path:
        dest = Path(dest)
        dest.mkdir(parents=True, exist_ok=True)
        return dest

    def rm(self, strict: bool = False) -> None:
        """
        Remove files or directories.

        Args:
            strict: If True, operate on all paths. If False, skip non-existent paths.
        """
        ser = self._ser if strict else self._ser[self._ser.map(Path.exists)]

        def _rm(path: Path) -> None:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

        ser.map(_rm)

    def cp(self, dest: Union[str, Path], strict: bool = False) -> Series:
        """
        Copy files or directories to the destination.

        Args:
            dest: Destination directory
            strict: If True, operate on all paths. If False, skip non-existent paths.

        Returns:
            Series with paths of copied files/directories
        """
        dest = self._validate_dest(dest)
        ser = self._ser if strict else self._ser[self._ser.map(Path.exists)]

        def _cp(path: Path) -> Path:
            dst = dest / path.name
            if path.is_dir():
                shutil.copytree(path, dst)
            else:
                shutil.copy2(path, dst)
            return dst

        return ser.map(_cp)

    def mv(self, dest: Union[str, Path], strict: bool = False) -> Series:
        """
        Move files or directories to the destination.

        Args:
            dest: Destination directory
            strict: If True, operate on all paths. If False, skip non-existent paths.

        Returns:
            Series with paths of moved files/directories
        """
        dest = self._validate_dest(dest)
        ser = self._ser if strict else self._ser[self._ser.map(Path.exists)]

        def _mv(path: Path) -> Path:
            dst = dest / path.name
            path.rename(dst)
            return dst

        return ser.map(_mv)

    def ln(self, dest: Union[str, Path], strict: bool = False) -> Series:
        """
        Create symbolic links in the destination directory.

        Args:
            dest: Destination directory
            strict: If True, operate on all paths. If False, skip non-existent paths.

        Returns:
            Series with paths of created symbolic links
        """
        dest = self._validate_dest(dest)
        ser = self._ser if strict else self._ser[self._ser.map(Path.exists)]

        def _ln(path: Path) -> Path:
            dst = dest / path.name
            dst.symlink_to(path)
            return dst

        return ser.map(_ln)
