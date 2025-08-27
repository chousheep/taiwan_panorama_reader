from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import re
import sys


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# Supported language codes (expand as needed)
LANGS = ["zh", "en", "ja", "vi", "th", "id"]

# Labels 
LANG_LABEL = {
    "zh": "繁體中文",
    "en": "English",
    "ja": "日本語",
    "vi": "Tiếng Việt",
    "th": "ภาษาไทย",
    "id": "Bahasa Indonesia",
}

# =================== Utilities ===================

def detect_lang_from_url(url: str):
    m = re.search(r"/(zh|en|ja|vi|th|id)/", url)
    return m.group(1) if m else None

def fetch(url: str):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    return resp

def get_title(url: str):
    resp = fetch(url)
    soup = BeautifulSoup(resp.text, "html5lib")
    title = (soup.title.text if soup.title else "").strip()
    if " - " in title:
        title = title.rsplit(" - ", 1)[0].strip()
    return title or "Untitled"

# =================== Tab parsing ===================

TAB_SELECTOR = ".TabContent"
TAB_ID_REGEX = re.compile(r"Tab(\d+)", re.IGNORECASE)

def _remove_noise(root):
    for tag in root.find_all(["script", "style", "noscript"]):
        tag.decompose()

def _inside_artifoto(node):
    return node.find_parent(class_="artiFoto") is not None or node.find_parent(class_="artiFotoIf") is not None

def _text(node):
    return node.get_text(" ", strip=True)

def extract_tabs_blocks(url: str):
    """
    Return a list of strings, one per Tab.
    Rules inside a Tab:
      - If a paragraph starts with <strong>, treat it as subheading.
      - Subheading and its following text separated by '\n'.
      - Multiple subsections inside the same Tab joined with '\n'.
    Exclude any text inside 'artiFoto' / 'artiFotoIf'.
    If the page has no Tab structure, return None.
    """
    resp = fetch(url)
    soup = BeautifulSoup(resp.text, "html5lib")
    _remove_noise(soup)

    # order Tabs by TabN
    tabs = []
    for el in soup.select(TAB_SELECTOR):
        tab_id = el.get("id") or ""
        m = TAB_ID_REGEX.search(tab_id)
        order = int(m.group(1)) if m else 10**9
        tabs.append((order, el))
    tabs.sort(key=lambda x: x[0])

    if not tabs:
        return None

    tab_texts = []

    for _, tab in tabs:
        blocks = tab.find_all(["p", "li", "blockquote"], recursive=True)
        if not blocks:
            continue

        sections = []
        current_heading = None
        current_parts = []

        for node in blocks:
            if _inside_artifoto(node):
                continue

            full_text = _text(node)
            if not full_text:
                continue

            st = node.find("strong")
            used_as_heading = False
            if st:
                strong_text = _text(st)
                if strong_text and full_text.startswith(strong_text):
                    # close previous section
                    if current_heading is not None:
                        body = " ".join(current_parts).strip()
                        sections.append(current_heading + ("\n" + body if body else ""))
                    current_heading = strong_text
                    remainder = full_text[len(strong_text):].lstrip(" ：:—-–\u3000 ")
                    current_parts = []
                    if remainder:
                        current_parts.append(remainder)
                    used_as_heading = True

            if not used_as_heading:
                current_parts.append(full_text)

        # flush last
        if current_heading is not None:
            body = " ".join(current_parts).strip()
            sections.append(current_heading + ("\n" + body if body else ""))
        else:
            if current_parts:
                sections = [" ".join(current_parts).strip()]

        if sections:
            tab_texts.append("\n".join(sections))

    return tab_texts if tab_texts else []

# =================== Fallback: flat article (no Tabs) ===================

def extract_article_flat(url: str):
    """
    Fallback when there is no Tab structure:
    - Collect paragraph text from common containers.
    - Exclude anything inside 'artiFoto' / 'artiFotoIf'.
    - Return a single concatenated string.
    """
    resp = fetch(url)
    soup = BeautifulSoup(resp.text, "html5lib")

    for wrap in soup.find_all(class_="artiFotoIf"):
        for p in wrap.find_all("p"):
            p.decompose()
    for wrap in soup.find_all(class_="artiFoto"):
        for p in wrap.find_all("p"):
            p.decompose()

    candidates = soup.select(".article, .artiBox, .text, article, .artiCont, .artiTxt, .artiCon")
    nodes = []
    if candidates:
        for node in candidates:
            nodes.extend(node.find_all("p"))
    else:
        nodes = soup.find_all("p")

    paras = []
    for p in nodes:
        if p.find_parent(class_="artiFoto") or p.find_parent(class_="artiFotoIf"):
            continue
        txt = p.get_text(" ", strip=True)
        if not txt:
            continue
        paras.append(txt.strip())

    return " ".join(paras) if paras else ""

# =================== Multi-language link discovery ===================

def collect_lang_links(seed_url: str):
    """
    From any language page, discover sibling language pages.
    1) Crawl <a href> for '/{lang}/Article(s)/Details'
    2) If missing, try swapping the language segment and validate with HTTP 200
    Return only languages that actually exist.
    """
    urls = {lang: None for lang in LANGS}
    parsed = urlparse(seed_url)
    base = f"{parsed.scheme}://{parsed.netloc}/"

    try:
        resp = fetch(seed_url)
        soup = BeautifulSoup(resp.text, "html5lib")
        for a in soup.find_all("a", href=True):
            abs_url = urljoin(base, a["href"])
            for lang in LANGS:
                if re.search(rf"/{lang}/Article[s]?/Details", abs_url):
                    urls[lang] = abs_url
    except Exception:
        pass

    seed_lang = detect_lang_from_url(seed_url)
    if seed_lang in LANGS:
        urls[seed_lang] = seed_url

    def swap_lang(u: str, target_lang: str):
        return re.sub(r"/(zh|en|ja|vi|th|id)/", f"/{target_lang}/", u, count=1)

    source_url = urls.get(seed_lang) or seed_url

    for lang in LANGS:
        if urls[lang]:
            continue
        candidate = swap_lang(source_url, lang)
        if "taiwan-panorama.com" in urlparse(candidate).netloc:
            try:
                test = requests.get(candidate, headers=HEADERS, timeout=10)
                if test.status_code == 200 and re.search(r"/Article", candidate):
                    urls[lang] = candidate
            except Exception:
                continue

    return {k: v for k, v in urls.items() if v}

# =================== Rendering helpers ===================

def render_full_from_tabs(tab_blocks):
    """Join all Tab strings with one blank paragraph between Tabs."""
    return "\n\n".join(tab_blocks)

def print_full_article(lang_code: str, title: str, body_text: str):
    """
    Specified format:
    == Language Label ==
    Title

    Article Content
    """
    label = LANG_LABEL.get(lang_code, lang_code.upper())
    print(f"== {label} ==")
    print(title)
    print("")
    print(body_text if body_text else "(No content found)")
    print("")

def print_paragraph_by_paragraph(selected_langs, lang_tabs_map):
    """
    Paragraph-by-paragraph (interleaved by Tab) output.
    Assumes all selected languages share the same non-zero Tab count.
    Do NOT print language names or titles; just the content.
    - Between languages inside the same Tab: one blank paragraph.
    - Between Tabs: one blank paragraph.
    """
    n_tabs = len(next(iter(lang_tabs_map.values())))
    for t in range(n_tabs):
        for i, lang in enumerate(selected_langs):
            tab_text = lang_tabs_map[lang][t]
            print(tab_text if tab_text else "(No content found)")
            if i != len(selected_langs) - 1:
                print("")  # blank paragraph between languages within the same Tab
        if t != n_tabs - 1:
            print("")      # blank paragraph between Tabs

# =================== UI helpers ===================

def normalize_code_list(s: str):
    parts = re.split(r"[,\s/|-]+", s.strip())
    return [p.lower() for p in parts if p.strip()]

def print_header():
    print("=== Taiwan Panorama Multi-language Article Tool ===")
    print("Please prepare a URL from any Taiwan Panorama story and paste it below")
    print("")

def choose_mode():
    print("\n=== Reading Mode Selection ===")
    print("This tool can lay out articles in two modes:")
    print("1) full-article mode: reads the entire article in one go.")
    print("2) paragraph-by-paragraph mode: interleaves paragraphs from multiple languages.")

    while True:
        raw = input("Enter 1 or 2 → ").strip().lower()
        if raw in ("1", "full", "full-article", "full article"):
            return "full"
        if raw in ("2", "paragraph", "paragraph-by-paragraph", "paragraph by paragraph"):
            return "paragraph"
        print("Invalid choice. Please type 1 or 2.")

def prompt_languages_full(found_map: dict):
    """Prompt for languages in full-article mode."""
    available_codes = [c for c in LANGS if c in found_map]
    labels = [LANG_LABEL.get(c, c.upper()) for c in available_codes]
    print("\nAvailable language versions:")
    print("Codes :", " ".join(available_codes))
    print("Labels:", " / ".join(labels))
    print('Enter language codes to output, or press Enter for ALL.')
    while True:
        raw = input("Languages -> ").strip()
        if raw == "" or raw.lower() == "all":
            return [c for c in LANGS if c in found_map]
        requested = normalize_code_list(raw)
        selected = []
        for c in requested:
            if c in found_map and c not in selected:
                selected.append(c)
        if selected:
            return selected
        print("No valid language codes. Try again.")

def prompt_languages_paragraph(found_map: dict, lang_tabs_meta: dict):
    """
    Prompt for languages in paragraph-by-paragraph mode.
    Secretly group languages by identical non-zero Tab counts,
    and show groups (without revealing the counts).
    Only accept a selection that is entirely within one group.
    Return the list of selected language codes, or None if the user wants to cancel/switch mode.
    """
    # Build groups: key = tab count, value = list of language codes (only counts > 0)
    groups = {}
    for code in LANGS:
        if code not in found_map:
            continue
        tabs = lang_tabs_meta[code]["tabs"]
        n = len(tabs) if tabs else 0
        if n > 0:
            groups.setdefault(n, []).append(code)

    print("\nAvailable combinations for interleaving paragraphs:")
    if not groups:
        print("None. No languages have compatible segmentation (Tabs).")
        return None # Indicate no paragraph-by-paragraph options

    # Show groups without counts; keep order by LANGS
    group_list = []
    group_idx = 1
    for n, codes in sorted(groups.items(), key=lambda kv: kv[0]):
        ordered = [c for c in LANGS if c in codes]
        if ordered:
            print(f"- {' '.join(ordered)}")
            group_list.append(set(ordered))
            group_idx += 1

    print('Your selection must come entirely from a single group above.')
    print("Type 'q' to cancel.")

    while True:
        raw = input("Languages → ").strip().lower()
        if raw == "q":
            return [] # Indicate user wants to cancel this mode
        if raw == "":
            # default to all from first group
            first_group = group_list[0] if group_list else set()
            return [c for c in LANGS if c in first_group]

        requested = set(normalize_code_list(raw))
        # Validate: requested must be subset of one group
        for grp in group_list:
            if requested and requested.issubset(grp):
                # preserve order according to LANGS
                return [c for c in LANGS if c in requested]
        print("Invalid selection. Choose languages from exactly one group above.")

# =================== Main ===================

if __name__ == "__main__":
    print_header()
    seed = input("URL -> ").strip()

    if not seed.startswith("http"):
        print("Invalid URL. Please paste a full http(s):// link.")
        sys.exit(1)

    # Discover available language versions
    found = collect_lang_links(seed)
    if not found:
        print("No language versions detected for this URL.")
        sys.exit(1)

    # Choose mode first
    mode = choose_mode()

    # Pre-parse Tabs for each available language (secretly)
    lang_meta = {}
    for code, url in found.items():
        title = get_title(url)
        tabs = extract_tabs_blocks(url)  # List[str] or None
        lang_meta[code] = {"title": title, "tabs": tabs, "url": url}

    if mode == "paragraph":
        selected = prompt_languages_paragraph(found, lang_meta)
        if selected is None: # No paragraph-by-paragraph options available
            print("\nSwitching to full-article mode since no interleavable languages are available.\n")
            mode = "full"
        elif selected == []: # User canceled paragraph-by-paragraph mode
             print("\nCanceled paragraph-by-paragraph mode.\n")
             sys.exit(0)
        else:
            # Build a map code -> tabs for printing; ensure same tab count
            tab_counts = {c: (len(lang_meta[c]["tabs"]) if lang_meta[c]["tabs"] else 0) for c in selected}
            if len(set(tab_counts.values())) != 1 or next(iter(tab_counts.values())) == 0:
                print("\nSelected languages are not compatible for paragraph-by-paragraph. Switching to full-article mode.\n")
                mode = "full"
            else:
                lang_tabs_map = {c: lang_meta[c]["tabs"] for c in selected}
                print("")  # spacing
                print_paragraph_by_paragraph(selected, lang_tabs_map)
                sys.exit(0)

    # Full-article mode path
    selected_full = prompt_languages_full(found)
    print("")
    for code in selected_full:
        # Re-fetch and extract in full-article format
        # This is slightly redundant if tabs were already extracted,
        # but keeps the logic clean for both tabbed and non-tabbed articles.
        title = lang_meta[code]["title"] # Use pre-fetched title
        tabs = lang_meta[code]["tabs"]
        if tabs:
            body = render_full_from_tabs(tabs)
        else:
            body = extract_article_flat(found[code])
        print_full_article(code, title, body)