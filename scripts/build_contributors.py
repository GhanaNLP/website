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
import json, os, re, sys, csv, urllib.parse, urllib.request

CHANNEL = "C09SH7ABLP5"  # #awesome-contributors
# Local paths to the two form exports; override with env vars if they move.
XLSX = os.environ.get(
    "MEMBERSHIP_XLSX",
    "/media/owusus/Godstestimo/Downloads/NLPGhana Membership details (Responses).xlsx")
CSV_ = os.environ.get(
    "MEMBERS_CSV",
    "/home/owusus/Dropbox/Mich/Projects/Ghana-NLP/CRM/mail merge/members_latest.csv")
OUT = os.path.join(os.path.dirname(__file__), "..", "_data", "contributors.yml")
TEAM = os.path.join(os.path.dirname(__file__), "..", "_data", "team-members.yml")

# LinkedIn URLs for contributors whose form response has none, taken from the
# contributor credits in our own GitHub repos (GhanaNLP/nsanku,
# ghana-corpus-builder, GhanaTopics, GhanaNouns). Keyed by the name this script
# produces, so add an entry here rather than hand-editing the generated YAML.
GITHUB_LINKEDIN = {
    "bernard adjei":        "https://www.linkedin.com/in/bernardmarfoadjei/",
    "chantelle amoako-atta": "https://www.linkedin.com/in/chantelleaa/",
    "elias dzobo":          "https://www.linkedin.com/in/eliasdzobo/",
    "gerhardt datsomor":    "https://www.linkedin.com/in/gerhardt-datsomor/",
    "john ayernor":         "https://www.linkedin.com/in/john-kwabena-ayernor-45b497186/",
    "jonathan markin":      "https://www.linkedin.com/in/atomarkin/",
    "kelvin newman":        "https://www.linkedin.com/in/kelvin-newman-09b961255/",
    "onesimus addo appiah": "https://www.linkedin.com/in/onesimus-appiah/",
    "tyra koranteng":       "https://www.linkedin.com/in/tyrakoranteng46/",
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
        else:
            unresolved.append(m)
            continue
        link = link or team.get(norm_name(name), "")
        link = link or linkedin_url(GITHUB_LINKEDIN.get(name.lower(), ""))
        nk = norm_name(name)
        if nk in seen:          # same person, two Slack accounts / two signups
            if link and not seen[nk]["linkedin"]:
                seen[nk]["linkedin"] = link
            continue
        entry = {"name": name, "linkedin": link}
        seen[nk] = entry
        people.append(entry)

    people.sort(key=lambda p: p["name"].lower())
    with open(OUT, "w") as fh:
        fh.write("# Generated by scripts/build_contributors.py -- do not hand-edit.\n")
        fh.write("# Members of the #awesome-contributors Slack channel, joined on email to\n")
        fh.write("# the membership form responses. Re-run the script to refresh.\n")
        for p in people:
            fh.write(f'- name: "{p["name"]}"\n')
            fh.write(f'  linkedin: {p["linkedin"]}\n' if p["linkedin"] else "  linkedin:\n")

    have = sum(1 for p in people if p["linkedin"])
    print(f"{len(members)} in channel -> {len(people)} unique contributors, {have} with LinkedIn")
    for m in unresolved:
        print(f"  no form response for: {m['real']} <{m['email']}>")
    for p in people:
        if not p["linkedin"]:
            print(f"  no LinkedIn: {p['name']}")


if __name__ == "__main__":
    main()
