import os
import shutil
from pathlib import Path

from PIL import Image, UnidentifiedImageError

PHOTO_FOLDER = os.path.abspath(os.path.join('photo'))
RESULT_FOLDER = os.path.abspath(os.path.join('sorted_photo'))
PHOTO_FORMATS = ('.jpg', '.jpeg', '.png')


def get_year(file_path):
    try:
        image = Image.open(file_path)
        exifdata = image.getexif()
        datetime = exifdata.get(306)
        image.close()
        if datetime:
            return datetime[:4]
        return None
    except UnidentifiedImageError:
        pass


def move_photo(photo_path, year_dir):
    photo_name = os.path.basename(photo_path)
    if not os.path.exists(os.path.join(year_dir, photo_name)):
        print(f'✅ moving "{photo_name}" from {photo_path} to {year_dir}')
        shutil.move(photo_path, year_dir)
    else:
        print(f'⛔️ ERROR: "{photo_name}" already exist in {year_dir}')


def go(cur):
    for dr in os.listdir(cur):
        abs_path = os.path.join(cur, dr)
        if os.path.isdir(abs_path):
            go(abs_path)
        else:
            if os.path.isfile(abs_path) and Path(abs_path).suffix.lower() in PHOTO_FORMATS:
                year = get_year(abs_path)
                if year:
                    try:
                        year_dir = os.path.abspath(os.path.join(RESULT_FOLDER, year))
                        os.mkdir(year_dir)
                    except FileExistsError:
                        pass
                    move_photo(abs_path, year_dir)


def del_empty(cur):
    for d in os.listdir(cur):
        a = os.path.join(cur, d)
        if os.path.isdir(a):
            del_empty(a)
            if not os.listdir(a):
                print('removing empty dir:', a)
                os.rmdir(a)


if __name__ == "__main__":
    try:
        os.mkdir(RESULT_FOLDER)
    except FileExistsError:
        pass
    go(PHOTO_FOLDER)
    del_empty(PHOTO_FOLDER)
