import urllib.request
from urllib.parse import urljoin
import json

URL = "https://time.com"
SITE_FILE = "site.txt"

def getData(url, file_name):
    f = urllib.request.urlopen(url)
    try:
        with open(f"{file_name}.txt", "w") as file:
            data = f.read().decode('utf-8')
            file.write(data)
    finally:
        f.close()

def strip_tags(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == '<':
            j = s.find('>', i+1)
            if j == -1:
                break
            i = j + 1
        else:
            out.append(s[i])
            i += 1
    return "".join(out)

def extract_href(a_tag):
    href_pos = a_tag.find("href")
    if href_pos == -1:
        return None

    eq = a_tag.find("=", href_pos)
    if eq == -1:
        return None

    i = eq + 1
    while i < len(a_tag) and a_tag[i].isspace():
        i += 1
    if i >= len(a_tag):
        return None

    if a_tag[i] in ('"', "'"):
        quote = a_tag[i]
        start = i + 1
        end = a_tag.find(quote, start)
    else:
        start = i
        sp = a_tag.find(" ", start)
        gt = a_tag.find(">", start)
        if sp == -1 or (gt != -1 and gt < sp):
            end = gt
        else:
            end = sp

    if end == -1:
        end = len(a_tag)

    href = a_tag[start:end].strip()
    if not href:
        return None
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return urljoin(URL, href)

def extract_span_text(span_tag):
    gt = span_tag.find(">")
    if gt == -1:
        inner = strip_tags(span_tag)
    else:
        end = span_tag.rfind("</span>")
        if end == -1:
            inner = span_tag[gt+1:]
        else:
            inner = span_tag[gt+1:end]
        inner = strip_tags(inner)
    return " ".join(inner.split())

def extract_h3_content(file):
    with open(file, "r", encoding="utf-8", errors="replace") as f:
        data = f.read()
    lower = data.lower()

    h3_list = []
    pos = 0
    while True:
        start = lower.find("<h3", pos)
        if start == -1:
            break
        open_end = lower.find(">", start)
        if open_end == -1:
            break
        close = lower.find("</h3>", open_end)
        if close == -1:
            break
        inner = data[open_end+1 : close]
        h3_list.append(inner)
        pos = close + len("</h3>")
    return h3_list


def build_final_list(h3_data, limit=6):
    final_list = []
    for content in h3_data:
        if len(final_list) == limit:
            break

        start_pos = 0
        while True:
            start_a_tag = content.find("<a", start_pos)
            if start_a_tag == -1:
                break

            tag_end_pos = content.find(">", start_a_tag)
            if tag_end_pos == -1:
                break

            end_a_tag = content.find("</a>", tag_end_pos)
            if end_a_tag == -1:
                break

            a_fragment = content[start_a_tag : end_a_tag + 4]
            link = extract_href(a_fragment)
            span_start = a_fragment.find("<span")
            if span_start != -1:
                span_tag_end = a_fragment.find(">", span_start)
                span_close = a_fragment.find("</span>", span_tag_end)
                if span_tag_end != -1 and span_close != -1:
                    span_fragment = a_fragment[span_start : span_close + 7]
                else:
                    span_fragment = a_fragment
            else:
                span_fragment = a_fragment[tag_end_pos+1 : -4]
            title = extract_span_text(span_fragment)
            if link and title and len(title) >= 3:
                final_list.append({"title": title, "link": link})
                break
            start_pos = end_a_tag + 4
        
    return final_list


def save_json(data, out_file="stories.json"):
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    getData(URL, "site")

    h3_data = extract_h3_content(SITE_FILE)

    final_list = build_final_list(h3_data, limit=6)

    print(json.dumps(final_list, indent=2, ensure_ascii=False))
    save_json(final_list, out_file="stories.json")

if __name__ == "__main__":
    main()
