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


def slug(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

report = []
for fn, name in sorted(MAP.items(), key=lambda kv: kv[1]):
    path = os.path.join(SRC, fn)
    im = ImageOps.exif_transpose(Image.open(path))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        im = Image.alpha_composite(Image.new("RGBA", im.size, (255,)*4), im)
    im = im.convert("RGB")
    W, H = im.size

    gray = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY) if os.path.exists(path) else None
    faces = cascade.detectMultiScale(gray, 1.1, 6, minSize=(40, 40)) if gray is not None else []
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
        s = min(W, H)
        box, how = ((W - s)//2, (H - s)//2, (W + s)//2, (H + s)//2), "centre (no face)"

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
