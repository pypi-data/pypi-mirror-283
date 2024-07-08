import datetime
import hashlib
import re
from collections import OrderedDict, defaultdict
from pathlib import Path
from secrets import token_urlsafe

from PIL import Image


class Toolkit:
    img_exts = tuple(k for k, v in Image.registered_extensions().items() if v in Image.OPEN)

    @staticmethod
    def folders_by_exts(workdir: Path) -> dict:
        exts = defaultdict(int)
        for root, dirs, files in workdir.walk():
            for file in files:
                path = Path(root, file)
                ext_low = path.suffix.lower()
                if ext_low:
                    exts[ext_low] += 1
        return OrderedDict(sorted(exts.items(), key=lambda i: i[0]))

    @staticmethod
    def folders_by_date(workdir: Path, choice_exts: tuple, exif: bool) -> dict:
        dates = defaultdict(set)
        for root, dirs, files in workdir.walk():
            for file in files:
                path = Path(root, file)
                ext_low = path.suffix.lower()
                if ext_low in choice_exts and ext_low in Toolkit.img_exts:
                    date_os = datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()
                    if exif:
                        date_exif = Toolkit.date_by_exif(path)
                        date = date_exif if date_exif else date_os
                    else:
                        date = date_os
                    year, month = date[:4], date[5:7]
                    dates[year].add(month)
        ordered = {year: sorted(months) for year, months in dates.items()}
        return OrderedDict(sorted(ordered.items(), key=lambda i: i[0]))

    @staticmethod
    def make_dirs(newdir: Path, folders: dict, mainfolder: str, only_mainfolder: bool) -> Path:
        if not newdir.joinpath(mainfolder).exists():
            Path.mkdir(newdir.joinpath(mainfolder))
        else:
            for i in range(len(list(newdir.iterdir()))):
                if not newdir.joinpath(f"{mainfolder} ({i + 1})").exists():
                    newdir.joinpath(mainfolder).rename(newdir.joinpath(f"{mainfolder} ({i + 1})"))
                    Path.mkdir(newdir.joinpath(mainfolder))
                    break
        newdir = newdir.joinpath(mainfolder)
        if only_mainfolder:
            return newdir
        for key, values in folders.items():
            if not isinstance(values, int):
                if not newdir.joinpath(key).exists():
                    Path.mkdir(newdir.joinpath(key))
                for value in values:
                    if not newdir.joinpath(key, value).exists():
                        Path.mkdir(newdir.joinpath(key, value))
        return newdir

    @staticmethod
    def date_by_exif(path: Path) -> str | None:
        with Image.open(path) as img:
            exif_dict = img._getexif()
        if not exif_dict:
            return None
        datetime_tags = (306, 36867, 36868)
        dates = [exif_dict[tag] for tag in datetime_tags if tag in exif_dict]
        regex = r"[^0]\d{3}(?:\W\d\d){2}\s\d\d(?:\W\d\d){2}"
        match = [re.fullmatch(regex, item) for item in dates]
        dates = [item[0] for item in match if item]
        if not dates:
            return None
        else:
            date = min(dates)
            return "-".join([date[:4], date[5:7], date[8:10]])

    @staticmethod
    def rename_by_random(workdir: Path, choice_exts: tuple) -> None:
        count_names = 0
        for root, dirs, files in workdir.walk():
            for file in files:
                path = Path(root, file)
                ext_low = path.suffix.lower()
                if ext_low in choice_exts:
                    count_names += 1
                    newname = f"({count_names}) " + token_urlsafe(64) + ext_low
                    path.rename(Path(path.parent, newname))

    @staticmethod
    def rename_by_template(workdir: Path, choice_exts: tuple, template: str) -> int:
        Toolkit.rename_by_random(workdir, choice_exts)
        count = 0
        for root, dirs, files in workdir.walk():
            names_count = defaultdict(int)
            paths = sorted([Path(root, file) for file in files], key=lambda i: i.stat().st_mtime)
            for path in paths:
                ext_low = path.suffix.lower()
                if ext_low in choice_exts:
                    newname = template + ext_low
                    names_count[newname] += 1
                    newname = template + f" ({names_count[newname]})" + ext_low
                    path.rename(Path(path.parent, newname))
                    count += 1
        return count

    @staticmethod
    def rename_by_date(workdir: Path, choice_exts: tuple, exif: bool) -> int:
        Toolkit.rename_by_random(workdir, choice_exts)
        count = 0
        for root, dirs, files in workdir.walk():
            names_count = defaultdict(int)
            paths = sorted([Path(root, file) for file in files], key=lambda i: i.stat().st_mtime)
            for path in paths:
                ext_low = path.suffix.lower()
                if ext_low in choice_exts and ext_low in Toolkit.img_exts:
                    date_os = datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()
                    if exif:
                        date_exif = Toolkit.date_by_exif(path)
                        date = date_exif if date_exif else date_os
                    else:
                        date = date_os
                    newname = date + ext_low
                    names_count[newname] += 1
                    newname = date + f" ({names_count[newname]})" + ext_low
                    path.rename(Path(path.parent, newname))
                    count += 1
        return count

    @staticmethod
    def move_by_exts(workdir: Path, choice_exts: tuple, newdir: Path) -> int:
        Toolkit.rename_by_random(workdir, choice_exts)
        folders = {ext: 0 for ext in choice_exts}
        newdir = Toolkit.make_dirs(newdir, folders, "Files", False)
        count = 0
        for root, dirs, files in workdir.walk():
            for file in files:
                path = Path(root, file)
                ext_low = path.suffix.lower()
                if ext_low in choice_exts:
                    target_dir = newdir.joinpath(ext_low)
                    path.rename(target_dir.joinpath(path.name))
                    count += 1
        return count

    @staticmethod
    def move_by_date(workdir: Path, choice_exts: tuple, newdir: Path, exif: bool) -> int:
        Toolkit.rename_by_random(workdir, choice_exts)
        folders = Toolkit.folders_by_date(workdir, choice_exts, exif)
        newdir = Toolkit.make_dirs(newdir, folders, "Images", False)
        count = 0
        for root, dirs, files in workdir.walk():
            for file in files:
                path = Path(root, file)
                ext_low = path.suffix.lower()
                if ext_low in choice_exts and ext_low in Toolkit.img_exts:
                    date_os = datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()
                    if exif:
                        date_exif = Toolkit.date_by_exif(path)
                        date = date_exif if date_exif else date_os
                    else:
                        date = date_os
                    year, month = date[:4], date[5:7]
                    target_dir = newdir.joinpath(year, month)
                    path.rename(target_dir.joinpath(path.name))
                    count += 1
        return count

    @staticmethod
    def find_duplicates(workdir: Path, choice_exts: tuple) -> list:
        sizes, duplicates = defaultdict(list), defaultdict(list)
        for root, dirs, files in workdir.walk():
            for path in [Path(root, file) for file in files]:
                if path.suffix.lower() in choice_exts:
                    size = path.stat().st_size
                    sizes[size].append(path)
        for path in [path for paths in sizes.values() if len(paths) > 1 for path in paths]:
            hash = hashlib.sha1(path.read_bytes(), usedforsecurity=False).hexdigest()
            duplicates[hash].append(path)
        return [[str(path) for path in paths] for paths in duplicates.values() if len(paths) > 1]

    @staticmethod
    def move_duplicates(newdir: Path, duplicates: list) -> None:
        newdir = Toolkit.make_dirs(newdir, {}, "Duplicates", True)
        for i in range(len(duplicates)):
            for duplicate in duplicates[i]:
                path = Path(duplicate)
                ext_low = path.suffix.lower()
                newname = f"({i+1}) " + token_urlsafe(64) + ext_low
                path.rename(newdir.joinpath(newname))
