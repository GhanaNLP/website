"""Crop and resize the contributor photos into assets/img/contributors/.

The sources are already square, so a plain centre-crop is a no-op; several are
wide shots where the subject sits off-centre. Detect the largest face, take a
square around it with headroom, and clamp to the image. Falls back to the
centre crop when no face is found.

Output is named after the contributor's slug, which is what
build_contributors.py looks for, so the source filenames only matter here.

Usage:  CONTRIBUTOR_PHOTOS=/path/to/photos python3 scripts/crop_contributor_photos.py
"""
import os, re, sys, yaml
import cv2
from PIL import Image, ImageOps

SRC = os.environ.get("CONTRIBUTOR_PHOTOS", "/home/owusus/Downloads/contributors")
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "assets", "img", "contributors")
SIZE = 400
MIN_SIZE = 240        # avatars render at 52px CSS, so keep 2x headroom
MARGIN = 2.1          # square side as a multiple of the face box
EYE_LINE = 0.42       # put the face centre this far down the crop
MIN_FACE_FRAC = 0.08  # a detection much smaller than the frame is not a face

# Explicit, because several filenames differ from the name we list people under
# (spellings, middle names, or a different given name entirely).
MAP = {
    "akwasi-asare.jpeg":            "Akwasi Asare",
    "alhassan-naporo.jpeg":         "A.Ganiw Naporo Alhassan",
    "alidu-abubakar.jpeg":          "Abubakari Alidu",
    "atsu-agbemabiase.png":         "Atsu Agbemabiase",
    "baffoe-nicholas.png":          "Baffoe Nicholas",
    "bernard-adjei.png":            "Bernard Adjei",
    "chantelle-amoako.png":         "Chantelle Amoako-Atta",
    "elias-elikem.jpeg":            "Elias Dzobo",
    "emmanuel-saah.jpeg":           "Emmanuel Saah",
    "foster-buabeng.jpeg":          "Kwaku Dompreh",
    "gerhardt-datsormor.jpeg":      "Gerhardt Datsomor",
    "issac-donkor.jpeg":            "Isaac Donkoh",
    "joel-budu.jpeg":               "Joel Budu",
    "john-ayernor.jpeg":            "John Ayernor",
    "jonathan-markin.jpeg":         "Jonathan Markin",
    "josephus-bawah.jpeg":          "Josephus Bawah",
    "julius-segbezie.jpeg":         "Julius Segbedzi",
    "kasuadana-sulemana.jpeg":      "Kasuadana Adams",
    "kelvin-newman.jpeg":           "Kelvin Newman",
    "lawrence-edu-gyamfi.jpeg":     "Lawrence Adu-Gyamfi",
    "lucas-kpatah.png":             "Lucas Kpatah",
    "maxwell-sam.jpeg":             "Maxwell Sam",
    "mich-seth-owusu.jpeg":         "Mich-Seth Owusu",
    "onesimus-addo-appiah.jpeg":    "Onesimus Addo Appiah",
    "paul-azunre.jpeg":             "Paul Azunre",
    "prince-nasamu-alhassan.png":   "Prince Alhassan",
    "priscilla-nartey.jpeg":        "Priscilla Lartey",
    "saani-mustapha-deishini.jpeg": "Mustapha Saani",
    "stephen-moore.jpeg":           "Stephen Moore",
    "timothy-aguya-akasiya.jpeg":   "Timothy Aguya Akasiya",
    "tyra-koranteng.jpeg":          "Tyra Koranteng",
}


# Contributors whose photo already lives in the repo, from when they were listed
# on the team page. Cropped the same way as everyone else so the circles match.
REPO_SOURCES = {
    'Benjamin Essilfie-Nyame'   : 'assets/img/team/Benjamin.png',
    'Bernard Adabankah'         : 'assets/img/team/adabankah.jpeg',
    'Bernard Opoku'             : 'assets/img/team/bernard.jpeg',
    'Clara Asare-Nyarko'        : 'assets/img/team/clara.jpg',
    'Daniel Elijah'             : 'assets/img/team/elijah.jpg',
    'David Sasu'                : 'assets/img/team/david.png',
    'Deborah Dormah Kanubala'   : 'assets/img/team/kanubala.jpg',
    'Edwin Munkoh-Buabeng'      : 'assets/img/uploads/img_9753-2__01.jpg',
    'Emile Adotey'              : 'assets/img/team/emile.jpeg',
    'Felix Akwerh'              : 'assets/img/team/felix.jpg',
    'Franklin Adjei'            : 'assets/img/team/FranklinAdjei.jpg',
    'Gideon Brogya'             : 'assets/img/uploads/file.jpg',
    'Gloria Appiah Nsiah'       : 'assets/img/team/gloria.jpeg',
    'Hussein Suhuyini'          : 'assets/img/team/hussein.png',
    'Immanuel Wallace'          : 'assets/img/uploads/pass_2-1-.jpg',
    'Joseph Otoo'               : 'assets/img/team/joseph.jpg',
    'Mark Amoako Marcel'        : 'assets/img/team/mark.jpg',
    'Naafi Dasana Ibrahim'      : 'assets/img/uploads/naafi_2.jpg',
    'Richard Nii Lante Lawson'  : 'assets/img/team/niilante.jpg',
    'Salomey Addo'              : 'assets/img/team/salomey.jpg',
    'Salomey Osei'              : 'assets/img/team/salomeyosei.jpeg',
    'Samuel Nyarko'             : 'assets/img/team/samuel.jpeg',
    'Vincent-Michael Ampadu'    : 'assets/img/uploads/vincent.jpg',
    'Wisdom Ofori'              : 'assets/img/uploads/img_5484.jpg',
}


def slug(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

report = []
jobs = [(os.path.join(SRC, fn), name) for fn, name in MAP.items()]
jobs += [(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", rel), name)
         for name, rel in REPO_SOURCES.items()]

for path, name in sorted(jobs, key=lambda kv: kv[1]):
    im = ImageOps.exif_transpose(Image.open(path))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255,)*4), im)
    im = im.convert("RGB")
    W, H = im.size

    gray = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY) if os.path.exists(path) else None
    faces = []
    if gray is not None:
        # Two guards against false positives. A detection much smaller than the
        # frame is usually a detail rather than a face -- a mouth, or a picture
        # on the wall -- and one low in the frame is something else again: on a
        # full-length portrait the cascade matches shoes down there.
        floor = max(40, int(min(gray.shape[:2]) * MIN_FACE_FRAC))
        faces = [f for f in cascade.detectMultiScale(gray, 1.1, 6, minSize=(floor, floor))
                 if (f[1] + f[3] / 2) < gray.shape[0] * 0.6]
    if len(faces):
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        side = min(int(max(w, h) * MARGIN), W, H)
        cx, cy = x + w / 2, y + h / 2
        left = int(round(cx - side / 2))
        top = int(round(cy - side * EYE_LINE))
        left = max(0, min(left, W - side))
        top = max(0, min(top, H - side))
        box, how = (left, top, left + side, top + side), f"face {w}x{h}"
    else:
        # No usable face. Take the square from the top of a portrait rather than
        # its middle -- heads sit near the top -- and from the middle of a
        # landscape, where there is no vertical crop to get wrong.
        sq = min(W, H)
        top = 0 if H > W else (H - sq) // 2
        box, how = ((W - sq)//2, top, (W + sq)//2, top + sq), "top crop (no face)"

    out_im = im.crop(box)
    target = max(MIN_SIZE, min(SIZE, out_im.size[0]))
    if out_im.size[0] != target:
        out_im = out_im.resize((target, target), Image.LANCZOS)
    out = os.path.join(DST, slug(name) + ".jpg")
    out_im.save(out, "JPEG", quality=85, optimize=True, progressive=True)
    report.append((name, how, out_im.size[0], os.path.getsize(out)//1024))

for n, how, px, kb in report:
    print(f"  {n:<26} {how:<18} {px}px {kb}KB")
print(f"\n{sum(1 for r in report if r[1].startswith('face'))}/{len(report)} cropped to a detected face")
