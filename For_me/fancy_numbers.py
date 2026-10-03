"""Fetch numbers in parallel, create a PDF, and optionally WhatsApp that PDF.

Install once: python -m pip install playwright
Run:          python fancy_numbers.py
Offline PDF:  python fancy_numbers.py --from-file --series TN42BY
Send existing PDF: python fancy_numbers.py --send-only

Edit the CONFIGURATION block below; no .env or other source files are read.
Running the script uses those settings without prompts. CLI flags override
settings; --interactive explicitly enables prompts. Numbers stay in memory;
--from-file optionally reads a saved file instead of accessing the website.
Chrome fetches headlessly. Edge reuses a CDP-enabled session if available or a
saved profile (one-time QR login), to send the PDF and message automatically.
Playwright, Chrome/Edge, and their browser session data are still required.
"""

import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from html import escape
from math import ceil
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from urllib.parse import urlparse
from urllib.request import urlopen

# ===================== CONFIGURATION — EDIT HERE =====================
DEFAULT_STATE = "TN"
DEFAULT_RTO = "593"
DEFAULT_SERIES = "first"  # First live option, or a prefix such as "TN42BY".
LETTER_VALUES = {"C": 1}  # C has two entries in the unchanged letter mapping.
WORKERS = 3              # 1–3 independent browser sessions.
PAUSE_SECONDS = 1.5      # At least 1 second between requests per worker.
PDF_PATH = "vehicle_numerology.pdf"

WHATSAPP_DEFAULT = "yes"  # "yes" sends automatically; "no" disables sending.
WHATSAPP_NUMBERS = "+919942744817"  # Comma-separated numbers WITH country codes.
WHATSAPP_MESSAGE = (
    "This is an automated message from the user about vehicle number availability "
    "and fancy options with numerology. Please see the attached PDF."
)
EDGE_CDP_URL = ""  # Set to http://127.0.0.1:9222 only for CDP-enabled Edge.
EDGE_PROFILE_PATH = Path.home() / ".vehicle-numerology-edge"
WHATSAPP_SEND_TIMEOUT_SECONDS = 30
# =================== END CONFIGURATION ===============================

# Copied verbatim from analyse.py. Do not change the mappings when updating the
# reporting logic. The source file is not imported; this script stands alone.
categories = {
    1: [1, 3, 5, 6, 9, 10, 14, 15, 16, 18, 21, 24, 27, 32, 33, 36, 42, 46, 50, 51],
    2: [19, 23, 37, 41, 45],
    3: [2, 12, 30, 38, 39, 48, 54, 57],
    4: [20, 52, 55],
    5: [26, 29, 35, 44, 53],
    6: [11, 13, 17, 22, 28, 31, 40, 49, 58],
    7: [56],
    8: [25, 34, 43, 47]
}
category_names = {
    1: "அதிர்ஷ்டம்",
    2: "மிக அதிர்ஷ்டம்",
    3: "சுமார்",
    4: "எதிரியை அழிப்பது",
    5: "ஆதரவு",
    6: "துரதிர்ஷ்டம்",
    7: "எமகண்டம்",
    8: "சோதனை"
}
number_for_letters = {
    1: "AIJCY",
    2: "BKR",
    3: "CGLS",
    4: "DMT",
    5: "EHNX",
    6: "UVW",
    7: "OZ",
    8: "FP"
}


HERE = Path(__file__).resolve().parent
LOGIN_URL = "https://fancy.parivahan.gov.in/fancy/faces/public/login.xhtml"
AVAILABLE_URL = "https://fancy.parivahan.gov.in/fancy/faces/public/availableAllNumbers.xhtml"
ICON = 'a[id="loginForm:grplnkSearchByNumber3"]'
SELECTS = {"State": "#ib_state123_input", "RTO": "#ib_rto123_input", "Series": "#ib_Veh_Seri_input"}
GRID = "#dtgAvailableNumber"
COUNTER = f"{GRID}_paginator_top .ui-paginator-current"
NUMBER_LABELS = f"{GRID}_content .ui-outputlabel-label"
NEXT = f"{GRID}_paginator_top .ui-paginator-next"
FIRST = f"{GRID}_paginator_top .ui-paginator-first"
PAGE_PATTERN = re.compile(r"\(\s*(\d+)\s+of\s+(\d+)\s*\)", re.I)


def options(page, selector):
    """Read values from PrimeFaces' (visually hidden) real select element."""
    return page.locator(f"{selector} option").evaluate_all(
        "elements => elements.filter(o => o.value && o.value !== '-1')"
        ".map(o => [o.value, o.textContent.trim().replace(/\\s+/g, ' ')])"
    )


def choose(label, available, provided=None, default=None, quiet=False, interactive=False):
    if not available:
        raise ValueError(f"No {label} choices offered by the website")
    if default not in [value for value, _ in available]:
        default = None
    if not quiet and interactive:
        print(f"\n{label}: {len(available)} choice(s). Enter a code or part of a name; ? lists all.", flush=True)
        if len(available) <= 30 and provided is None:
            for value, name in available:
                print(f"  {value:12} {name}")
    query = provided if provided is not None else (None if interactive else default)
    if query is None and not interactive:
        raise ValueError(f"Configured default {label} is not available; update CONFIGURATION or run --interactive")
    while True:
        if query is None:
            query = input(f"{label} [{default}]: " if default else f"{label}: ").strip() or default
        if query == '?':
            for value, name in available:
                print(f"  {value:12} {name}")
        elif query:
            exact = [(v, n) for v, n in available if v.casefold() == query.casefold()
                     or n.casefold() == query.casefold()]
            matches = exact or [(v, n) for v, n in available if query.casefold() in n.casefold()]
            if len(matches) == 1:
                value, name = matches[0]
                if not quiet:
                    print(f"  Selected {value}: {name}", flush=True)
                return value
            if matches:
                print("Matches (enter a code to choose one):")
                for value, name in matches[:40]:
                    print(f"  {value:12} {name}")
                if len(matches) > 40:
                    print(f"  ...and {len(matches) - 40} more; refine your search")
            else:
                print(f"No {label} matches {query!r}")
        if provided is not None or not interactive:
            raise ValueError(f"{label} {query!r} is not a unique available choice")
        query = None


def set_primefaces_select(page, selector, value):
    # select_option() cannot operate on PrimeFaces' hidden <select>. Dispatching
    # its genuine change event triggers the site's own JSF AJAX listener.
    page.locator(selector).evaluate(
        "(element, value) => { element.value = value; "
        "element.dispatchEvent(new Event('change', {bubbles: true})); }", value
    )


def open_available_page(page):
    page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=45_000)
    icon = page.locator(ICON)
    if icon.count() != 1 or not (icon.get_attribute("href") or "").endswith("/availableAllNumbers.xhtml"):
        raise RuntimeError("The 'All Available' icon changed or is missing on the login page")
    # The carousel icon is sometimes CSS-hidden in headless Chrome. Invoke its
    # anchor click in the page so navigation still happens from the live login
    # session, rather than loading availableAllNumbers.xhtml directly.
    icon.evaluate("element => element.click()")
    page.wait_for_url(AVAILABLE_URL, timeout=30_000)
    page.locator(SELECTS["State"]).wait_for(state="attached", timeout=20_000)


def select_filters(page, state=None, rto=None, series=None, quiet=False, interactive=False,
                   state_default=DEFAULT_STATE, rto_default=DEFAULT_RTO, series_default=DEFAULT_SERIES):
    selected_state = choose("State", options(page, SELECTS["State"]), state,
                            default=state_default, quiet=quiet, interactive=interactive)
    set_primefaces_select(page, SELECTS["State"], selected_state)
    page.locator(f'{SELECTS["RTO"]} option:not([value="-1"])').first.wait_for(state="attached", timeout=30_000)

    selected_rto = choose("RTO", options(page, SELECTS["RTO"]), rto,
                          default=rto_default, quiet=quiet, interactive=interactive)
    set_primefaces_select(page, SELECTS["RTO"], selected_rto)
    page.locator(f'{SELECTS["Series"]} option:not([value="-1"])').first.wait_for(state="attached", timeout=30_000)

    available_series = options(page, SELECTS["Series"])
    default_series = (available_series[0][0] if available_series else None) if series_default.lower() == "first" else series_default
    selected_series = choose("Series", available_series, series, default=default_series,
                             quiet=quiet, interactive=interactive)
    set_primefaces_select(page, SELECTS["Series"], selected_series)
    page.locator(NUMBER_LABELS).first.wait_for(state="attached", timeout=45_000)
    return selected_state, selected_rto, selected_series


def status(page):
    text = page.locator(COUNTER).inner_text(timeout=10_000)
    match = PAGE_PATTERN.search(text)
    if not match:
        raise ValueError(f"Unexpected page counter: {text!r}")
    return int(match.group(1)), int(match.group(2))


def grid_row_count(page):
    return page.evaluate("() => PF('widget_dtgAvailableNumber').cfg.paginator.rowCount")


def collect_range(page, start, end, total, pause):
    """One independent JSF session per worker; never paginate concurrently in one session."""
    from playwright.sync_api import expect

    if start != 1:
        # PrimeFaces uses zero-based page indexes; this performs ONE AJAX jump.
        page.evaluate("index => PF('widget_dtgAvailableNumber').paginator.setPage(index)", start - 1)
        expect(page.locator(COUNTER)).to_have_text(f"({start} of {total})", timeout=30_000)
    result = {}
    for page_number in range(start, end + 1):
        actual, new_total = status(page)
        if (actual, new_total) != (page_number, total):
            raise ValueError(f"Page mismatch: expected {page_number}/{total}, got {actual}/{new_total}")
        values = [text.strip() for text in page.locator(NUMBER_LABELS).all_text_contents()]
        if not values or any(not re.fullmatch(r"[0-9]{4}", value) for value in values):
            raise ValueError(f"Invalid or empty results on page {page_number}")
        if len(values) != len(set(values)):
            raise ValueError(f"Duplicate numbers within page {page_number}")
        result[page_number] = values
        print(f"Page {page_number}/{total}: {len(values)} numbers", flush=True)
        if page_number < end:
            time.sleep(pause)
            page.evaluate("index => PF('widget_dtgAvailableNumber').paginator.setPage(index)", page_number)
            # Locator assertions work despite the site's CSP restriction on eval.
            expect(page.locator(COUNTER)).to_have_text(f"({page_number + 1} of {total})", timeout=30_000)
    return result


def additional_worker(state, rto, series, start, end, total, expected_count, pause):
    # Sync Playwright objects are not thread-safe. Each thread creates its own
    # browser AND isolated cookies/ViewState before requesting its page range.
    from playwright.sync_api import sync_playwright
    with sync_playwright() as worker_playwright:
        browser = worker_playwright.chromium.launch(channel="chrome", headless=True)
        try:
            tab = browser.new_page()
            open_available_page(tab)
            filters = select_filters(tab, state, rto, series, quiet=True)
            if filters != (state, rto, series):
                raise ValueError(f"Worker selected different filters: {filters}")
            if status(tab)[1] != total or grid_row_count(tab) != expected_count:
                raise ValueError("Availability changed while opening worker sessions; rerun for a fresh snapshot")
            return collect_range(tab, start, end, total, pause)
        finally:
            browser.close()


def scrape_pages(page, state, rto, series, pause=1.5, workers=2):
    current, total = status(page)
    if current != 1 or not 1 <= total <= 200:
        raise ValueError(f"Unexpected initial page: {current} of {total}")
    expected_count = grid_row_count(page)
    worker_count = min(workers, total)
    size = ceil(total / worker_count)
    ranges = [(start, min(start + size - 1, total)) for start in range(1, total + 1, size)]
    print(f"Fetching {total} pages / {expected_count} numbers with {len(ranges)} isolated sessions", flush=True)
    pages = {}
    with ThreadPoolExecutor(max_workers=len(ranges) - 1 or 1) as executor:
        futures = [executor.submit(additional_worker, state, rto, series, start, end, total,
                                   expected_count, pause) for start, end in ranges[1:]]
        pages.update(collect_range(page, *ranges[0], total, pause))
        for future in futures:
            pages.update(future.result())
    if sorted(pages) != list(range(1, total + 1)):
        raise ValueError("A page was missed or repeated; no report will be generated")
    numbers = [number for index in range(1, total + 1) for number in pages[index]]
    if len(numbers) != expected_count or len(numbers) != len(set(numbers)):
        raise ValueError("Page results are inconsistent (count or duplicate mismatch); retry the fetch")
    return numbers


def prefix_value(series, letter_overrides=None):
    """Add *all* characters of the prefix, including RTO digits (TN42BY = 18)."""
    series = series.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]+", series):
        raise ValueError("Series must contain only Latin letters and digits, e.g. TN42BY")
    values = defaultdict(set)
    for value, letters in number_for_letters.items():
        for letter in letters.upper():
            values[letter].add(value)
    parts = []
    total = 0
    resolved = {}
    letter_overrides = LETTER_VALUES if letter_overrides is None else letter_overrides
    for char in series:
        if char.isdigit():
            value = int(char)
            parts.append(char)
        else:
            matches = sorted(values[char])
            if not matches:
                raise ValueError(f"Letter {char} is not defined in the embedded number_for_letters mapping")
            if char in resolved:
                value = resolved[char]
            elif len(matches) > 1:
                configured = str(letter_overrides.get(char, ""))
                if not configured.isdigit() or int(configured) not in matches:
                    raise ValueError(f"Letter {char} has multiple values {matches}; set LETTER_VALUES['{char}'] in CONFIGURATION")
                value = int(configured)
                resolved[char] = value
            else:
                value = matches[0]
            parts.append(f"{char}({value})")
        total += value
    return total, " + ".join(parts)


def categorize(numbers, series_total):
    by_total = {}
    for category, totals in categories.items():
        for total in totals:
            if total in by_total:
                raise ValueError(f"Total {total} belongs to more than one category")
            by_total[total] = category
    grouped = {category: [] for category in category_names}
    ungrouped = []
    for number in numbers:
        if not re.fullmatch(r"[0-9]{4}", number):
            raise ValueError(f"Invalid four-digit number: {number!r}")
        total = sum(int(digit) for digit in number) + series_total
        category = by_total.get(total)
        (ungrouped if category is None else grouped[category]).append(number)
    for values in (*grouped.values(), ungrouped):
        values.sort(key=lambda value: (int(value), value))
    return grouped, ungrouped


def fancy_patterns(number):
    counts = Counter(number)
    patterns = []
    if len(counts) == 1:
        patterns.append("four matching digits")
    elif max(counts.values()) >= 3:
        patterns.append("three matching digits")
    if len(counts) == 2 and sorted(counts.values()) == [2, 2]:
        patterns.append("repeated or mirrored pair")  # ABAB, AABB, ABBA
    digits = [int(digit) for digit in number]
    if all((digits[i + 1] - digits[i]) % 10 == 1 for i in range(3)) or all(
        (digits[i + 1] - digits[i]) % 10 == 9 for i in range(3)
    ):
        patterns.append("ascending or descending run")
    if abs(int(number[:2]) - int(number[2:])) == 1:
        patterns.append("consecutive two-digit pairs")
    if number.endswith("00"):
        patterns.append("round hundred")
    return patterns


def number_chip(number):
    patterns = fancy_patterns(number)
    if patterns:
        return (f'<span class="number fancy" title="{escape(", ".join(patterns), quote=True)}">'
                f'{escape(number)}</span>')
    return f'<span class="number">{escape(number)}</span>'


def append_category_numbers(parts, values):
    """Lay out one ascending list per category; chunks only prevent awkward page breaks."""
    ordered = sorted(values, key=lambda value: (int(value), value))
    for start in range(0, len(ordered), 72):
        parts.append('<div class="numbers">')
        parts.extend(number_chip(value) for value in ordered[start:start + 72])
        parts.append('</div>')


def make_html(numbers, grouped, ungrouped, series, series_total, breakdown, source="fancy.parivahan.gov.in"):
    counts = {cat: len(grouped[cat]) for cat in category_names}
    parts = ["""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Vehicle Number Numerology</title><style>
@page { size: A4; margin: 16mm 15mm 17mm; }
* { box-sizing: border-box; }
body { margin: 0; color: #192d42; font-family: Arial, 'Nirmala UI', sans-serif; font-size: 10pt; }
header { padding: 0 0 15px; border-bottom: 3px solid #164c68; margin-bottom: 18px; }
h1 { font-size: 23pt; color: #123851; margin: 0 0 6px; letter-spacing: -.5px; }
.subtitle { color: #4b6476; margin: 0; font-size: 10.5pt; line-height: 1.5; }
.highlight { background: #e7f3ef; border-left: 4px solid #1c806c; padding: 10px 14px; margin: 16px 0; line-height: 1.5; }
.summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 7px; margin: 14px 0 18px; }
.summary-item { border: 1px solid #d7e2e7; border-radius: 6px; padding: 9px 10px; background: #f7fafb; }
.summary-item .label { display: block; font-size: 9pt; margin-bottom: 5px; }
.summary-item strong { font-size: 14pt; color: #164c68; }
.legend { color: #516b79; font-size: 9pt; line-height: 1.5; margin: 0 0 14px; }
section { margin: 17px 0 22px; }
section.major:not(.first) { break-before: page; page-break-before: always; }
.section-head { display: flex; align-items: baseline; justify-content: space-between; border-bottom: 2px solid #164c68; padding: 0 0 7px; margin: 0 0 13px; break-after: avoid; }
h2 { font-size: 15pt; margin: 0; font-weight: 700; color: #164c68; }
.section-head span { font-size: 9pt; color: #4d6375; }
.numbers { display: grid; grid-template-columns: repeat(8, 1fr); gap: 5px 7px; margin: 0 0 12px; break-inside: avoid; page-break-inside: avoid; }
.number { display: block; text-align: center; background: #edf4f7; padding: 5px 0; border-radius: 4px; font: 10pt Arial, sans-serif; color: #193b50; }
.number.fancy { background: #fff2d5; box-shadow: inset 0 0 0 1px #d9ae64; color: #654415; font-weight: bold; }
.number.fancy::after { content: "★"; color: #a67522; font-size: 7pt; margin-left: 3px; }
.fancy-guide { color: #654c2a; font-size: 9pt; line-height: 1.5; margin: -5px 0 15px; }
.fancy-guide strong { color: #80571e; }
.top-picks { padding-top: 6px; color: #285846; font-size: 9.5pt; }
.empty { color: #697c87; font-style: italic; margin: 5px 0 13px; }
.note { color: #566c79; font-size: 9pt; line-height: 1.45; margin-top: 13px; }
@media print { html { print-color-adjust: exact; -webkit-print-color-adjust: exact; } }
</style></head><body><header><h1>Vehicle Number Numerology</h1>
"""]
    parts.append(f'<p class="subtitle">Series <strong>{escape(series)}</strong> &nbsp;·&nbsp; '
                 'Grouped using the unchanged mappings in analyse.py</p></header>')
    parts.append(f'<div class="highlight"><strong>Selection tip:</strong> The template labels '
                 f'<strong>{escape(category_names[2])}</strong> as “Very lucky” ({counts.get(2, 0)} options) '
                 f'and <strong>{escape(category_names[1])}</strong> as “Lucky” ({counts.get(1, 0)} options). '
                 'It does not rank numbers within a category.')
    choices = []
    for category, label in ((2, "Very lucky"), (1, "Lucky")):
        matches = [value for value in grouped[category] if fancy_patterns(value)]
        if matches:
            examples = ", ".join(escape(value) for value in matches[:8])
            if len(matches) > 8:
                examples += f" (+{len(matches) - 8} more below)"
            choices.append(f"{label} ({len(matches)}): <strong>{examples}</strong>")
    if choices:
        parts.append('<div class="top-picks">★ Fancy options in lucky groups — '
                     + ' &nbsp;·&nbsp; '.join(choices) + '</div>')
    parts.append('</div><div class="summary">')
    for category, name in category_names.items():
        parts.append(f'<div class="summary-item"><span class="label" lang="ta">{escape(name)}</span>'
                     f'<strong>{counts[category]}</strong></div>')
    parts.append('</div>')
    if numbers:
        example = numbers[0]
        digits = ' + '.join(example)
        example_text = f' E.g. {escape(example)} → {digits} + {series_total} = {sum(map(int, example)) + series_total}.'
    else:
        example_text = ''
    parts.append(f'<p class="legend"><strong>{len(numbers)} numbers total.</strong> '
                 f'Series {escape(series)} contributes {escape(breakdown)} = <strong>{series_total}</strong>. '
                 f'Total = sum of the number’s digits + {series_total}.{example_text} '
                 'The total determines the category; numbers within each category are in ascending order. '
                 'Numbers with unmapped totals appear last.</p>')
    fancy_count = sum(bool(fancy_patterns(value)) for value in numbers)
    parts.append(f'<p class="fancy-guide"><strong>★ {fancy_count} fancy numbers highlighted in gold:</strong> '
                 'repeated digits or pairs (including mirrors), digit runs, consecutive two-digit pairs '
                 '(e.g. 86|87 in 8687), and round hundreds. This is a visual preference, not a change '
                 'to the numerology category.</p>')
    first = True
    for category, name in category_names.items():
        count = counts[category]
        parts.append(f'<section class="{"major" if count else "minor"} {"first" if first else ""}">'
                     f'<div class="section-head"><h2 lang="ta">{category:02d} &nbsp; {escape(name)}</h2>'
                     f'<span>{count} number{"s" if count != 1 else ""}</span></div>')
        if count:
            first = False
            append_category_numbers(parts, grouped[category])
        else:
            parts.append('<p class="empty">No available numbers in this category.</p>')
        parts.append('</section>')
    remaining = len(ungrouped)
    parts.append(f'<section class="minor"><div class="section-head"><h2>Ungrouped</h2>'
                 f'<span>{remaining} number{"s" if remaining != 1 else ""}</span></div>')
    if remaining:
        append_category_numbers(parts, ungrouped)
    else:
        parts.append('<p class="empty">None — every available number has a mapped total.</p>')
    parts.append(f'</section><p class="note">Source: {escape(source)} · Category and letter values: analyse.py</p>'
                 '</body></html>')
    return ''.join(parts)


def read_numbers(path):
    values = [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if not values:
        raise ValueError(f"No numbers in {path}")
    if len(set(values)) != len(values):
        raise ValueError(f"Duplicate numbers in {path}")
    return values


def render_pdf(context, html, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".numerology-", suffix=".pdf", dir=path.parent)
    os.close(fd)
    temporary = Path(name)
    tab = context.new_page()
    try:
        tab.set_content(html, wait_until="load", timeout=60_000)
        tab.pdf(path=str(temporary), print_background=True, prefer_css_page_size=True)
        if temporary.stat().st_size == 0:
            raise RuntimeError("Chrome produced an empty PDF")
        return temporary  # commit only after the entire fetch and render succeed
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    finally:
        tab.close()


def whatsapp_numbers():
    raw = WHATSAPP_NUMBERS
    if not raw:
        return []
    result = []
    for entry in raw.split(","):
        entry = entry.strip()
        if not entry:
            raise ValueError("WHATSAPP_NUMBERS contains an empty entry")
        # International format with country code: +919876543210 or 919876543210.
        phone = re.sub(r"[\s()+.-]", "", entry)
        if not re.fullmatch(r"[1-9][0-9]{7,14}", phone):
            raise ValueError("Each WhatsApp recipient must include a country code (8–15 digits)")
        if phone not in result:
            result.append(phone)
    if len(result) > 20:
        raise ValueError("More than 20 recipients; split this into smaller, reviewed batches")
    return result


def prompt_whatsapp(default="no"):
    answer = input(f"Send the PDF and WhatsApp message? [{'Y/n' if default == 'yes' else 'y/N'}]: ").strip().lower()
    if not answer:
        answer = "y" if default == "yes" else "n"
    if answer not in ("y", "yes", "n", "no"):
        raise ValueError("Answer y or n for WhatsApp sending")
    return answer in ("y", "yes")


def edge_cdp_available(endpoint):
    """Only attach to a local debugging endpoint belonging to Microsoft Edge."""
    if urlparse(endpoint).hostname not in ("localhost", "127.0.0.1", "::1"):
        raise ValueError("Edge CDP URL must refer to localhost; do not expose browser debugging remotely")
    try:
        with urlopen(endpoint.rstrip("/") + "/json/version", timeout=2) as stream:
            data = json.load(stream)
    except (OSError, ValueError):
        return False
    return "Edg/" in data.get("User-Agent", "") or "Edge" in data.get("Browser", "")


def upload_pdf(tab, pdf_path):
    """Retry only opening the attachment chooser, never a Send click."""
    from playwright.sync_api import Error as PlaywrightError

    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF attachment not found: {pdf_path}")
    chooser = None
    document_input = None
    last_error = None
    for attempt in range(1, 4):
        try:
            tab.locator('#main footer [contenteditable="true"][role="textbox"]').last.wait_for(
                state="visible", timeout=60_000)
            # The first chat render can replace the menu just after it opens.
            tab.wait_for_timeout(1500 if attempt == 1 else 500)
            attach = tab.locator('[aria-label="Attach"], [title="Attach"], [data-testid="clip"], [data-icon="plus"]').first
            attach.click(timeout=15_000)
            tab.wait_for_timeout(300)
            for candidate in tab.locator('input[type="file"]').all():
                accept = (candidate.get_attribute("accept") or "").lower()
                if accept in ("*", "", "*/*") or "application/" in accept or ".pdf" in accept:
                    document_input = candidate
                    break
            if document_input is not None:
                break
            # Click the actual menuitem, not its animated/detaching label span.
            document = tab.get_by_role("menuitem", name="Document", exact=True).last
            if not document.count():
                document = tab.get_by_text("Document", exact=True).last
            document.wait_for(state="visible", timeout=10_000)
            with tab.expect_file_chooser(timeout=15_000) as event:
                # React handles this bubbling click, without Playwright waiting
                # for the text span's animation to stop or holding a stale node.
                document.dispatch_event("click", timeout=5000)
            chooser = event.value
            break
        except PlaywrightError as exc:
            last_error = exc
            if attempt == 3:
                raise RuntimeError("Could not open WhatsApp's Document chooser after 3 attempts. "
                                   "No file was uploaded or sent.") from last_error
            print(f"WhatsApp: attachment menu changed; reopening it ({attempt}/3).", flush=True)
            tab.keyboard.press("Escape")
    # File selection is outside the retry loop: it happens at most once.
    if document_input is not None:
        document_input.set_input_files(str(pdf_path))
    elif chooser is not None:
        chooser.set_files(str(pdf_path))
    else:
        raise RuntimeError("WhatsApp did not provide a document input or file chooser")


def prepare_pdf(tab, pdf_path, message):
    """Upload the document and type its caption, but do not click Send yet."""
    upload_pdf(tab, pdf_path)
    # WhatsApp currently labels this "Send 1 selected" rather than exactly
    # "Send". Match both, and keep the actual preview button, not the chat button.
    send_button = tab.get_by_role("button", name=re.compile(r"^Send(?:\s|$)", re.I)).last
    send_button.wait_for(state="visible", timeout=60_000)
    caption = None
    for selector in (
        '[data-testid="media-caption-input-container"][contenteditable="true"]',
        '[data-testid="media-caption-input-container"] [contenteditable="true"]',
        '[contenteditable="true"][aria-placeholder*="caption" i]',
        '[contenteditable="true"][data-placeholder*="caption" i]',
        '[role="dialog"] [contenteditable="true"][role="textbox"]',
    ):
        for candidate in tab.locator(selector).all():
            if candidate.is_visible() and candidate.evaluate(
                "el => !el.closest('#side') && (!el.closest('footer') || "
                "!!el.closest('[role=dialog]') || /caption/i.test(" 
                "(el.getAttribute('aria-placeholder') || '') + (el.getAttribute('data-placeholder') || '')))"
            ):
                caption = candidate
                break
        if caption is not None:
            break
    if caption is not None:
        caption.fill(message)
        if message[:40] not in caption.inner_text():
            raise RuntimeError("WhatsApp did not accept the document caption; PDF was not sent")
        print("WhatsApp: PDF ready and message typed into the caption.", flush=True)
    else:
        print("WhatsApp: PDF ready; text will be sent separately after the attachment.", flush=True)
    return send_button, caption is not None


def message_snapshot(tab):
    """Remember existing messages so an older, identical PDF cannot prove a new send."""
    return tab.evaluate("""() => ({
        ids: Array.from(document.querySelectorAll('#main [data-id]')).map(el => el.getAttribute('data-id')),
        legacyCount: document.querySelectorAll('#main .message-out').length
    })""")


def wait_submitted_message(tab, previous, message="", document=False, timeout=None):
    """Recognize new WhatsApp messages, including versions without .message-out.

    This checks submission to the chat, not delivery/read status at the recipient.
    PDF titles may differ from filenames, so document icons + caption are used.
    """
    timeout = WHATSAPP_SEND_TIMEOUT_SECONDS if timeout is None else timeout
    deadline = time.monotonic() + timeout
    expected = " ".join(message.split())[:40]
    while time.monotonic() < deadline:
        found = tab.evaluate("""({previous, expected, documentOnly}) => {
            const oldIds = new Set(previous.ids);
            let candidates = Array.from(document.querySelectorAll('#main [data-id]'))
                .filter(el => !oldIds.has(el.getAttribute('data-id')));
            // Compatibility for older WhatsApp releases and legacy markup.
            candidates.push(...Array.from(document.querySelectorAll('#main .message-out'))
                .slice(previous.legacyCount));
            return candidates.some(el => {
                const text = (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim();
                const isDocument = !!el.querySelector('[data-testid*="document"], [data-icon*="document"]');
                const pending = !!el.querySelector('[data-icon="msg-time"], [data-icon*="clock"], [data-icon="alert-error"]');
                return !pending && (!expected || text.includes(expected)) && (!documentOnly || isDocument);
            });
        }""", {"previous": previous, "expected": expected, "documentOnly": document})
        if found:
            return
        tab.wait_for_timeout(250)
    raise RuntimeError("Send was clicked, but a new message could not be confirmed in the chat. "
                       "It may already have been sent; check the chat rather than automatically resending.")


def attach_pdf(tab, pdf_path, message):
    """Click Send once, then confirm the new document using current WhatsApp markup."""
    tab.locator('#main footer [contenteditable="true"][role="textbox"]').last.wait_for(
        state="visible", timeout=60_000)
    previous = message_snapshot(tab)
    send_button, caption_sent = prepare_pdf(tab, pdf_path, message)
    preview_button = send_button.element_handle()
    print("WhatsApp: sending PDF now...", flush=True)
    send_button.click(timeout=60_000)
    # Do not click again on timeout: the first click may already have sent it.
    preview_button.wait_for_element_state("hidden", timeout=90_000)
    wait_submitted_message(tab, previous, message if caption_sent else "", document=True)
    print("WhatsApp: PDF and caption confirmed in the chat." if caption_sent else
          "WhatsApp: PDF confirmed in the chat.", flush=True)
    return caption_sent


def send_whatsapp(playwright, phones, message, pdf_path, cdp_url=None):
    endpoint = cdp_url or "http://127.0.0.1:9222"
    if edge_cdp_available(endpoint):
        browser = playwright.chromium.connect_over_cdp(endpoint, timeout=15_000)
        if not browser.contexts:
            raise RuntimeError("No browser context available in the CDP-enabled Edge session")
        context = browser.contexts[0]
        print("Connected to your already-open CDP-enabled Edge session.")
    else:
        if cdp_url:
            raise RuntimeError(f"No Microsoft Edge remote-debugging endpoint at {cdp_url}")
        profile = EDGE_PROFILE_PATH
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile), channel="msedge", headless=False, no_viewport=True,
            args=["--no-first-run"]
        )
        browser = None
        print(f"Edge was not started with remote debugging. Using saved Edge profile: {profile}")
        print("Log in to WhatsApp Web once in this profile; subsequent runs reuse that login.")
    tab = context.new_page()
    completed = []
    try:
        tab.goto("https://web.whatsapp.com/", wait_until="domcontentloaded", timeout=90_000)
        try:
            tab.locator("#side").wait_for(state="visible", timeout=60_000)
        except Exception as exc:
            raise RuntimeError("WhatsApp Web is not logged in in this Edge profile. "
                               "Log in with the QR code once, then rerun the script.") from exc
        from playwright.sync_api import expect
        for phone in phones:
            try:
                tab.goto(f"https://web.whatsapp.com/send?phone={phone}",
                         wait_until="domcontentloaded", timeout=90_000)
                caption_sent = attach_pdf(tab, pdf_path, message)
                if not caption_sent:
                    composer = tab.locator('#main footer [contenteditable="true"][role="textbox"]').last
                    composer.wait_for(state="visible", timeout=60_000)
                    composer.fill(message)
                    expect(composer).to_contain_text(message[:40], timeout=10_000)
                    previous = message_snapshot(tab)
                    composer.press("Enter")
                    expect(composer).to_be_empty(timeout=30_000)
                    wait_submitted_message(tab, previous, message)
                completed.append(phone)
                print(f"Submitted PDF and message to +{phone}", flush=True)
                time.sleep(1.5)
            except Exception as exc:
                raise RuntimeError(f"Stopped at +{phone}. Check the chat before retrying: the PDF may "
                                   f"already have been sent. {exc}; already completed: {completed}") from exc
    finally:
        tab.close()
        if browser is not None:
            browser.close()  # disconnect CDP; do not log out or delete the user's profile
        else:
            context.close()


def confirm_whatsapp(phones, message, pdf_path):
    if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        raise FileNotFoundError(f"PDF to attach does not exist: {pdf_path}")
    print("\nWhatsApp preview:")
    print("PDF attachment:", pdf_path)
    print("Recipients:", ", ".join("+" + phone for phone in phones))
    print("Message:\n" + message)
    return input("Type SEND to submit the PDF and message to ALL listed recipients: ").strip() == "SEND"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--state", help="state code/name (otherwise prompt)")
    parser.add_argument("--rto", help="RTO code/name (otherwise prompt)")
    parser.add_argument("--series", help="registration prefix e.g. TN42BY (otherwise prompt)")
    parser.add_argument("--from-file", action="store_true", help="skip fetching; rebuild the PDF from numbers.txt")
    parser.add_argument("--numbers", type=Path, default=HERE / "numbers.txt", help="input file for --from-file only; never overwritten")
    parser.add_argument("--pdf", type=Path, default=HERE / PDF_PATH,
                        help="output PDF file")
    parser.add_argument("--pause", type=float, default=PAUSE_SECONDS,
                        help="seconds between requests PER worker (minimum 1)")
    parser.add_argument("--workers", type=int, default=WORKERS,
                        help=f"independent concurrent browser sessions (1–3; configured default {WORKERS})")
    parser.add_argument("--send", action="store_true", help="send the PDF and message without prompting")
    parser.add_argument("--whatsapp-default", choices=("yes", "no"),
                        default=WHATSAPP_DEFAULT.lower(),
                        help="automatically send when yes, skip when no (unless overridden)")
    parser.add_argument("--interactive", action="store_true", help="prompt for filters and WhatsApp confirmation")
    parser.add_argument("--no-whatsapp", action="store_true", help="skip the optional WhatsApp prompt")
    parser.add_argument("--send-only", action="store_true", help="send the existing PDF and message without fetching")
    parser.add_argument("--message", default=WHATSAPP_MESSAGE,
                        help="custom WhatsApp message (otherwise use the standard automation notice)")
    parser.add_argument("--edge-cdp-url", default=EDGE_CDP_URL or None,
                        help="CDP-enabled Edge URL, e.g. http://127.0.0.1:9222")
    args = parser.parse_args(argv)
    if args.send_only and args.from_file:
        parser.error("--send-only cannot be combined with --from-file")
    if args.no_whatsapp and (args.send or args.send_only):
        parser.error("--no-whatsapp cannot be combined with sending flags")
    if args.whatsapp_default not in ("yes", "no"):
        parser.error("WHATSAPP_DEFAULT must be yes or no")
    if not 1 <= args.workers <= 3:
        parser.error("--workers must be between 1 and 3 to limit load on the public site")
    if not args.from_file and not args.send_only and args.pause < 1:
        parser.error("--pause must be at least 1 second")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        parser.error("Install Playwright: python -m pip install playwright")
    numbers_path = args.numbers.resolve()
    pdf_path = args.pdf.resolve()
    temporary_pdf = None
    try:
        with sync_playwright() as playwright:
            if args.send_only:
                message = args.message or WHATSAPP_MESSAGE
            else:
                browser = playwright.chromium.launch(channel="chrome", headless=True)
                try:
                    context = browser.new_context()
                    if args.from_file:
                        default_series = "TN42BY" if DEFAULT_SERIES.lower() == "first" else DEFAULT_SERIES
                        series = args.series or default_series
                        if args.interactive and not args.series:
                            series = input(f"Series prefix [{default_series}]: ").strip() or default_series
                        numbers = read_numbers(numbers_path)
                    else:
                        tab = context.new_page()
                        open_available_page(tab)
                        state, rto, series = select_filters(
                            tab, args.state, args.rto, args.series, interactive=args.interactive,
                            state_default=DEFAULT_STATE, rto_default=DEFAULT_RTO,
                            series_default=DEFAULT_SERIES)
                    series = series.strip().upper()
                    series_total, breakdown = prefix_value(series)
                    print(f"Series {series}: {breakdown} = {series_total}")
                    if not args.from_file:
                        numbers = scrape_pages(tab, state, rto, series, args.pause, args.workers)
                        print(f"Collected {len(numbers)} numbers in memory; numbers.txt was not changed")
                    grouped, ungrouped = categorize(numbers, series_total)
                    html = make_html(numbers, grouped, ungrouped, series, series_total, breakdown,
                                     source=numbers_path.name if args.from_file else "fancy.parivahan.gov.in")
                    temporary_pdf = render_pdf(context, html, pdf_path)
                finally:
                    browser.close()
                os.replace(temporary_pdf, pdf_path)
                print(f"Created {pdf_path} ({len(numbers)} numbers; {len(ungrouped)} ungrouped)")
                if args.no_whatsapp:
                    print("DONE", flush=True)
                    return 0
                message = args.message or WHATSAPP_MESSAGE
                if not args.send and not (prompt_whatsapp(args.whatsapp_default) if args.interactive
                                          else args.whatsapp_default == "yes"):
                    print("WhatsApp disabled by configuration; PDF is ready. DONE", flush=True)
                    return 0
            phones = whatsapp_numbers()
            if not phones:
                raise ValueError("Set WHATSAPP_NUMBERS in CONFIGURATION (comma-separated, with country codes)")
            if not pdf_path.is_file() or pdf_path.stat().st_size == 0:
                raise FileNotFoundError(f"PDF to attach does not exist: {pdf_path}")
            if args.interactive and not confirm_whatsapp(phones, message, pdf_path):
                print("WhatsApp sending cancelled; report files were not affected.")
                return 0
            print(f"Sending the PDF and message to {len(phones)} WhatsApp recipient(s)")
            send_whatsapp(playwright, phones, message, pdf_path, args.edge_cdp_url)
        print("DONE", flush=True)
        return 0
    except (Exception, KeyboardInterrupt) as exc:
        print(f"Stopped: {exc}", file=sys.stderr)
        return 1
    finally:
        if temporary_pdf is not None:
            temporary_pdf.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
