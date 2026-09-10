#!/usr/bin/env python3
"""Regenerate _data/contributors.yml from the #awesome-contributors Slack channel.

Slack gives us who is in the channel; the membership form exports give us their
real names and LinkedIn URLs, joined on email address. The xlsx export carries
LinkedIn but is missing some members, so the older CSV is used as a name
fallback, and _data/team-members.yml fills in LinkedIn for people already on
the team page.

Usage:  SLACK_TOKEN=xoxp-... python3 scripts/build_contributors.py
Needs the token scopes: conversations.members, users:read, users:read.email
"""
import base64, json, os, re, subprocess, sys, csv, urllib.parse, urllib.request

CHANNEL = "C09SH7ABLP5"  # #awesome-contributors
# Local paths to the two form exports; override with env vars if they move.
XLSX = os.environ.get(
    "MEMBERSHIP_XLSX",
    "/media/owusus/Godstestimo/Downloads/NLPGhana Membership details (Responses).xlsx")
CSV_ = os.environ.get(
    "MEMBERS_CSV",
    "/home/owusus/Dropbox/Mich/Projects/Ghana-NLP/CRM/mail merge/members_latest.csv")
OUT = os.path.join(os.path.dirname(__file__), "..", "_data", "contributors.yml")
PHOTO_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "contributors")
TEAM = os.path.join(os.path.dirname(__file__), "..", "_data", "team-members.yml")

# LinkedIn URLs for contributors whose form response has none. Keyed by the name
# this script produces, so add an entry here rather than hand-editing the
# generated YAML, which is overwritten on every run.
EXTRA_LINKEDIN = {
    # from the contributor credits in our own repos: GhanaNLP/nsanku,
    # ghana-corpus-builder, GhanaTopics, GhanaNouns
    "bernard adjei":        "https://www.linkedin.com/in/bernardmarfoadjei/",
    "chantelle amoako-atta": "https://www.linkedin.com/in/chantelleaa/",
    "elias dzobo":          "https://www.linkedin.com/in/eliasdzobo/",
    "gerhardt datsomor":    "https://www.linkedin.com/in/gerhardt-datsomor/",
    "john ayernor":         "https://www.linkedin.com/in/john-kwabena-ayernor-45b497186/",
    "jonathan markin":      "https://www.linkedin.com/in/atomarkin/",
    "kelvin newman":        "https://www.linkedin.com/in/kelvin-newman-09b961255/",
    "onesimus addo appiah": "https://www.linkedin.com/in/onesimus-appiah/",
    "tyra koranteng":       "https://www.linkedin.com/in/tyrakoranteng46/",
    # supplied by hand
    "abubakari alidu":      "https://www.linkedin.com/in/alidu-abubakari-2612bb57/",
    "priscilla lartey":     "https://www.linkedin.com/in/larteypriscilla/",
    "akwasi asare":         "https://www.linkedin.com/in/nana-akwasi-asare-1301481b0/",
}

# Repos whose README credits contributors by name and LinkedIn URL. Parsed at
# generation time so the attribution follows whatever the repos currently say.
CREDIT_REPOS = {
    "nsanku":               "Nsanku",
    "ghana-corpus-builder": "Ghana Corpus Builder",
    "GhanaTopics":          "Ghana Topics",
    "GhanaNouns":           "Ghana Nouns",
    "Ghana-QA":             "Ghana QA",
    "Ghana-Named-Entities": "Ghana Named Entities",
}

# Contributors to list who are not in the Slack channel at all.
EXTRA_PEOPLE = [
    {"name": "Atsu Agbemabiase",
     "linkedin": "https://www.linkedin.com/in/atsu-agbemabiase-a490b617a/"},
    # moved off the team page when it became the board listing; their photos and
    # LinkedIn URLs come from _data/team-members.yml, where they already lived
    {"name": "Salomey Osei",
     "linkedin": "https://linkedin.com/in/salomey-osei-4b08a5b8"},
    {"name": "Richard Nii Lante Lawson",
     "linkedin": "http://linkedin.com/in/theniilante"},
    {"name": "Franklin Adjei",
     "linkedin": "http://linkedin.com/in/franklin-koomson-adjei-227bb5130/"},
    {"name": "Vincent-Michael Ampadu",
     "linkedin": "https://www.linkedin.com/in/vincentmichaelkampadu/"},
    {"name": "Deborah Dormah Kanubala",
     "linkedin": "https://www.linkedin.com/in/kanubalad/"},
    {"name": "David Sasu",
     "linkedin": "https://www.linkedin.com/in/david-sasu-0667861b7/"},
    {"name": "Bernard Opoku",
     "linkedin": "https://www.linkedin.com/in/bernard-kwabena-opoku-965653b1"},
    {"name": "Benjamin Essilfie-Nyame",
     "linkedin": "https://www.linkedin.com/in/benjamin-essilfie-nyame-14a05b14a"},
    {"name": "Gloria Appiah Nsiah",
     "linkedin": "https://www.linkedin.com/in/gloria-appiah-nsiah"},
    {"name": "Felix Akwerh",
     "linkedin": "https://www.linkedin.com/in/%20felix-akwerh-029314"},
    {"name": "Samuel Nyarko",
     "linkedin": "https://www.linkedin.com/in/samuelnyarko"},
    {"name": "Bernard Adabankah",
     "linkedin": "https://www.linkedin.com/in/bernard-adabankah-3109b015/"},
    {"name": "Daniel Elijah",
     "linkedin": "https://www.linkedin.com/in/daniel-komla-elijah-21384a63/"},
    {"name": "Clara Asare-Nyarko",
     "linkedin": "https://www.linkedin.com/in/clara-asare-nyarko-99a66a72"},
    {"name": "Emile Adotey",
     "linkedin": "https://linkedin.com/in/emile-adotey-47163954"},
    {"name": "Joseph Otoo",
     "linkedin": "https://www.linkedin.com/in/joseph-otoo-8aa82633"},
    {"name": "Salomey Addo",
     "linkedin": "https://http//www.linkedin.com/in/salomey-addo"},
    {"name": "Hussein Suhuyini",
     "linkedin": ""},
    {"name": "Wisdom Ofori",
     "linkedin": "https://www.linkedin.com/in/wizdees/"},
    {"name": "Mark Amoako Marcel",
     "linkedin": ""},
    {"name": "Immanuel Wallace",
     "linkedin": "https://www.linkedin.com/in/emmanuel-agbeli-419008a2/"},
    {"name": "Gideon Brogya",
     "linkedin": ""},
    {"name": "Edwin Munkoh-Buabeng",
     "linkedin": "https://linkedin.com/in/ebmunkoh"},
    {"name": "Naafi Dasana Ibrahim",
     "linkedin": "https://www.linkedin.com/in/naafi-ibrahim-67622a161"},
]

# Channel members with no membership-form response, so there is no name to look
# up. Keyed by email; the value is the name to list them under.
NO_FORM_RESPONSE = {
    "nasare34@yahoo.com": "Akwasi Asare",
}


def norm_email(e):
    """Gmail ignores dots and +tags, so fold those before joining on email."""
    e = str(e or "").strip().lower()
    if "@" not in e:
        return ""
    local, _, domain = e.partition("@")
    local = local.split("+")[0]
    if domain in ("gmail.com", "googlemail.com"):
        local, domain = local.replace(".", ""), "gmail.com"
    return local + "@" + domain


def norm_name(n):
    n = re.sub(r"^(dr|mr|mrs|ms|prof)\.?\s+", "", str(n or "").strip().lower())
    return tuple(sorted(re.sub(r"[^a-z ]", "", n).split()))


def clean(v):
    v = str(v or "").strip()
    return "" if v.lower() in ("", "none", "n/a", "na", "-", "nil") else v


def linkedin_url(v):
    """The form answers are free text: full URLs, bare handles, tracking params,
    double schemes, even whole sentences with the link buried in them. Pull the
    profile slug out and rebuild a canonical URL, or give up and return "".
    """
    v = clean(v)
    if not v:
        return ""
    m = re.search(r"(?:[\w-]+\.)?linkedin\.com/(?:in|pub)/([\w%.-]+)", v, re.I)
    if m:
        return "https://www.linkedin.com/in/" + m.group(1).strip("/")
    if re.fullmatch(r"[\w-]{3,}", v):        # a bare handle
        return "https://www.linkedin.com/in/" + v
    return ""


def slack(method, token, **params):
    url = "https://slack.com/api/" + method + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + token})
    data = json.load(urllib.request.urlopen(req))
    if not data.get("ok"):
        sys.exit(f"slack {method} failed: {data.get('error')}")
    return data


def channel_members(token):
    ids, cursor = [], ""
    while True:
        kw = {"cursor": cursor} if cursor else {}
        d = slack("conversations.members", token, channel=CHANNEL, limit=200, **kw)
        ids += d["members"]
        cursor = d.get("response_metadata", {}).get("next_cursor", "")
        if not cursor:
            break
    people = []
    for uid in ids:
        u = slack("users.info", token, user=uid)["user"]
        if u.get("is_bot") or u.get("deleted"):
            continue
        people.append({"slack": u.get("name"), "real": u.get("real_name"),
                       "email": u.get("profile", {}).get("email", "")})
    return people


def load_xlsx():
    import openpyxl
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    rows = wb["Form responses 1"].iter_rows(values_only=True)
    hdr = list(next(rows))
    out = {}
    for r in rows:
        if not any(r):
            continue
        rec = dict(zip(hdr, r))
        key = norm_email(rec.get("Email address"))
        if key:
            out[key] = rec  # later submissions win
    return out


def load_csv():
    out = {}
    with open(CSV_) as fh:
        for r in csv.DictReader(fh):
            key = norm_email(r.get("Email address"))
            if key:
                out.setdefault(key, r)
    return out


def team_linkedin():
    import yaml
    team = yaml.safe_load(open(TEAM))["team"]
    out = {}
    for m in team:
        url = linkedin_url(m.get("linkedin"))
        if url and m.get("name"):
            out[norm_name(m["name"])] = url
    return out


def slug(name):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")


def photo_for(name):
    """assets/img/contributors/<slug>.jpg if someone has supplied a photo."""
    rel = f"/assets/img/contributors/{slug(name)}.jpg"
    return rel if os.path.exists(os.path.join(PHOTO_DIR, slug(name) + ".jpg")) else ""


def name_tokens(n):
    """Bare word set for loose name matching; drops "(Buabeng)"-style asides."""
    return set(re.sub(r"[^a-z ]", "", re.sub(r"\(.*?\)", "", (n or "").lower())).split())


def repo_credits():
    """{repo: [(linkedin slug, credited name), ...]} from each repo's README.

    Two shapes appear in our READMEs: a list where the person's name is the link
    text, and a table where the name sits in the first column and the link text
    is just "Profile". Both are collected.

    A list rather than a dict keyed by slug, because a slug can repeat -- in
    Ghana-Named-Entities two rows carry the same profile URL -- and keying on it
    silently drops one of the names.

    Uses the gh CLI so it picks up the caller's existing GitHub auth.
    """
    out = {}
    for repo in CREDIT_REPOS:
        r = subprocess.run(["gh", "api", f"repos/GhanaNLP/{repo}/contents/README.md",
                            "--jq", ".content"], capture_output=True, text=True)
        if r.returncode:
            print(f"  warning: could not read {repo} README, skipping", file=sys.stderr)
            continue
        md = base64.b64decode(r.stdout).decode("utf8", "replace")
        found = []

        # [Name](https://linkedin.com/in/slug)
        for name, url in re.findall(
                r"\[([^\]]+)\]\((https?://[^)]*linkedin\.com/in/[^)]+)\)", md):
            m = re.search(r"linkedin\.com/in/([\w%.-]+)", url)
            if m:
                found.append((m.group(1).strip("/"), name.strip()))

        # | Name | [Profile](https://linkedin.com/in/slug) |
        for name, slug in re.findall(
                r"^\|\s*([^|\n]+?)\s*\|[^|\n]*linkedin\.com/in/([\w%.-]+)",
                md, re.M):
            found.append((slug.strip("/"), name.strip()))

        out[repo] = sorted(set(found))
    return out


def projects_for(person, credits):
    """Match on LinkedIn slug, or on two shared name words when the slug differs
    between a repo credit and the form response (e.g. foster-dompreh vs
    foster-dompreh-8b383b49, Jonathan Ato Markin vs Jonathan Markin)."""
    m = re.search(r"/in/([\w%.-]+)", person["linkedin"] or "")
    slug = m.group(1) if m else ""
    mine = name_tokens(person["name"])
    out = []
    for repo, entries in credits.items():
        for s, credited in entries:
            if (slug and (s == slug or s.startswith(slug) or slug.startswith(s))) \
                    or len(mine & name_tokens(credited)) >= 2:
                out.append(repo)
                break
    return out


def main():
    token = os.environ.get("SLACK_TOKEN")
    if not token:
        sys.exit("set SLACK_TOKEN")
    members, xlsx, csv_, team = channel_members(token), load_xlsx(), load_csv(), team_linkedin()

    people, seen, unresolved = [], {}, []
    for m in members:
        key = norm_email(m["email"])
        x, c = xlsx.get(key), csv_.get(key)
        if x:
            name = " ".join(f'{clean(x.get("First name"))} {clean(x.get("Last name"))}'.split())
            link = linkedin_url(x.get("LinkedIn profile URL") or x.get("LinkedIn profile"))
        elif c:
            name = " ".join(f'{c["First name"]} {c["Last name"]}'.split())
            link = ""
        elif key in NO_FORM_RESPONSE:
            name, link = NO_FORM_RESPONSE[key], ""
        else:
            unresolved.append(m)
            continue
        link = link or team.get(norm_name(name), "")
        link = link or linkedin_url(EXTRA_LINKEDIN.get(name.lower(), ""))
        nk = norm_name(name)
        if nk in seen:          # same person, two Slack accounts / two signups
            if link and not seen[nk]["linkedin"]:
                seen[nk]["linkedin"] = link
            continue
        entry = {"name": name, "linkedin": link}
        seen[nk] = entry
        people.append(entry)

    for extra in EXTRA_PEOPLE:
        nk = norm_name(extra["name"])
        if nk in seen:
            continue
        entry = {"name": extra["name"], "linkedin": linkedin_url(extra.get("linkedin", ""))}
        seen[nk] = entry
        people.append(entry)

    credits = repo_credits()
    for person in people:
        person["projects"] = projects_for(person, credits)
        person["img"] = photo_for(person["name"])

    people.sort(key=lambda p: p["name"].lower())
    with open(OUT, "w") as fh:
        fh.write("# Generated by scripts/build_contributors.py -- do not hand-edit.\n")
        fh.write("# Members of the #awesome-contributors Slack channel, joined on email to\n")
        fh.write("# the membership form responses. Re-run the script to refresh.\n")
        for p in people:
            fh.write(f'- name: "{p["name"]}"\n')
            fh.write(f'  linkedin: {p["linkedin"]}\n' if p["linkedin"] else "  linkedin:\n")
            if p["img"]:
                fh.write(f'  img: {p["img"]}\n')
            if p["projects"]:
                fh.write("  projects:\n")
                for repo in p["projects"]:
                    fh.write(f'    - name: "{CREDIT_REPOS[repo]}"\n')
                    fh.write(f"      url: https://github.com/GhanaNLP/{repo}\n")

    have = sum(1 for p in people if p["linkedin"])
    tagged = sum(1 for p in people if p["projects"])
    photos = sum(1 for p in people if p["img"])
    print(f"{len(members)} in channel + {len(EXTRA_PEOPLE)} listed manually "
          f"-> {len(people)} unique contributors, {have} with LinkedIn, "
          f"{tagged} with project credits, {photos} with a photo")
    for p in people:
        if not p["img"]:
            print(f"  no photo: {p['name']}")
    for m in unresolved:
        print(f"  no form response for: {m['real']} <{m['email']}>")
    for p in people:
        if not p["linkedin"]:
            print(f"  no LinkedIn: {p['name']}")


if __name__ == "__main__":
    main()
