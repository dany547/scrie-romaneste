#!/usr/bin/env python3
"""Read-only HTML/Gutenberg preflight; not an HTML or block-render validator."""

import argparse
import json
import re
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

VOID = set("area base br col embed hr img input link meta param source track wbr".split())
BLOCK = set("address article aside blockquote br caption dd details dialog div dl dt "
            "fieldset figcaption figure footer form header hr li main nav ol p pre "
            "section summary table tbody td th thead tfoot tr ul".split())
HEADINGS = {f"h{level}" for level in range(1, 7)}
OMIT = {"script", "style", "template", "noscript", "textarea"}
HEAD_CONTENT = {"base", "link", "meta", "noscript", "script", "style", "template", "title"}
MARKER = re.compile(r"(/?)wp:([^\s]+)(?:\s+(.*))?", re.DOTALL)
BLOCK_NAME = re.compile(r"[a-z][a-z0-9_-]*(?:/[a-z][a-z0-9_-]*)?")


def reject_constant(value):
    raise ValueError(f"Invalid JSON constant: {value}")


class Preflight(HTMLParser):
    # HTMLParser already treats scripts/styles as raw text. Title and textarea
    # also cannot contain actual tags/comments; title entities are decoded below.
    CDATA_CONTENT_ELEMENTS = ("script", "style", "title", "textarea", "noscript")

    def __init__(self, mode):
        super().__init__(convert_charrefs=True)
        self.mode = mode
        self.title = self.meta_description = None
        self.title_parts = None
        self.in_head = False
        self.past_head = False
        self.omitted = None
        self.omitted_depth = 0
        self.parts = []
        self.heading = None
        self.headings = []
        self.issues = []
        self.blocks = []
        self.has_gutenberg = mode == "wp-body"

    def issue(self, category, detail, line=None):
        self.issues.append({"line": self.getpos()[0] if line is None else line,
                            "category": category, "detail": detail})

    def handle_starttag(self, tag, attrs):
        if self.omitted:
            if tag == self.omitted:
                self.omitted_depth += 1
            return
        attrs = dict(attrs)
        if tag == "head" and not self.past_head:
            self.in_head = True
            return
        if tag != "html" and tag not in HEAD_CONTENT:
            self.end_head()
        # The page's head can be implicit. Body and foreign elements (such as
        # SVG) end that window, so their title/meta tags aren't document metadata.
        document_metadata = self.mode == "page" and not self.past_head
        if tag == "title":
            if document_metadata and self.title is None:
                self.title_parts = []
            return
        if (document_metadata and tag == "meta"
                and (attrs.get("name") or "").strip().lower() == "description"
                and attrs.get("content") is not None and self.meta_description is None):
            self.meta_description = " ".join(attrs["content"].split())
        if tag in OMIT or "hidden" in attrs:
            if tag not in VOID:
                self.omitted = tag
                self.omitted_depth = 1
            return
        if self.in_head:
            return
        if tag in HEADINGS:
            self.finish_heading()
            self.parts.append("\n")
            self.heading = (int(tag[1]), self.getpos()[0], len(self.parts))
        elif tag in BLOCK:
            self.parts.append("\n")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in self.CDATA_CONTENT_ELEMENTS and (tag != "title" or self.title_parts is not None):
            # The slash does not close an HTML document title or script.
            # A non-document <title /> may instead be an empty SVG element.
            self.set_cdata_mode(tag)
        elif tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.omitted:
            if tag == self.omitted:
                self.omitted_depth -= 1
                if not self.omitted_depth:
                    self.omitted = None
            return
        if tag == "title" and self.title_parts is not None:
            self.title = " ".join(unescape("".join(self.title_parts)).split())
            self.title_parts = None
        elif tag == "head":
            self.end_head()
        elif not self.in_head:
            if tag in HEADINGS or tag == "body":
                self.finish_heading()
            if tag in HEADINGS or tag in BLOCK:
                self.parts.append("\n")

    def handle_data(self, data):
        if self.omitted:
            return
        if self.title_parts is not None:
            self.title_parts.append(data)
        elif not self.in_head and self.cdata_elem != "title":
            if data.strip():
                self.end_head()
            # Source indentation/newlines are spaces; structural separators aren't.
            self.parts.append(re.sub(r"\s+", " ", data))

    def end_head(self):
        self.in_head = False
        self.past_head = True

    def finish_heading(self):
        if self.heading is not None:
            level, line, start = self.heading
            text = " ".join("".join(self.parts[start:]).split())
            self.headings.append({"level": level, "text": text, "line": line})
            self.heading = None

    def is_block_marker(self, data):
        # Hidden HTML can still contain real block delimiters. Raw-text elements
        # don't dispatch comments in the first place; templates aren't post content.
        return self.omitted != "template" and data.lstrip().startswith(("wp:", "/wp:"))

    def close(self):
        # A pending comment at EOF has no comment callback. Do not emit it as prose.
        if self.cdata_elem is None and self.rawdata.startswith("<!--"):
            if self.is_block_marker(self.rawdata[4:]):
                self.has_gutenberg = True
                self.issue("gutenberg_marker", "Unterminated block comment")
            return
        super().close()

    def handle_comment(self, data):
        if not self.is_block_marker(data):
            return
        marker = data.strip()
        self.has_gutenberg = True
        match = MARKER.fullmatch(marker)
        if not match or not BLOCK_NAME.fullmatch(match[2]):
            self.issue("gutenberg_marker", "Invalid block marker or name")
            return
        closing, name, tail = match.groups()
        name = name if "/" in name else f"core/{name}"
        tail = tail or ""
        if closing:
            if tail:
                self.issue("gutenberg_marker", f"Unexpected content on closing marker for {name}")
            self.close_block(name)
            return
        self_closing = tail.endswith("/")
        attrs = tail[:-1].rstrip() if self_closing else tail
        if attrs:
            try:
                if not isinstance(json.loads(attrs, parse_constant=reject_constant), dict):
                    raise ValueError("Expected an object")
            except (ValueError, RecursionError):
                self.issue("gutenberg_attrs", f"Attributes for {name} must be a valid JSON object")
        if not self_closing:
            self.blocks.append((name, self.getpos()[0]))

    def close_block(self, name):
        if self.blocks and self.blocks[-1][0] == name:
            self.blocks.pop()
            return
        expected = self.blocks[-1][0] if self.blocks else None
        detail = f"Closing {name} while {expected} is open" if expected else f"Unexpected close for {name}"
        self.issue("gutenberg_pairing", detail)
        # If the close belongs to an ancestor, recover past its unclosed children.
        for index in range(len(self.blocks) - 1, -1, -1):
            if self.blocks[index][0] == name:
                del self.blocks[index:]
                break

    def result(self):
        self.finish_heading()
        for name, line in self.blocks:
            self.issue("gutenberg_pairing", f"Unclosed block {name}", line)
        if self.mode == "page":
            h1 = [h for h in self.headings if h["level"] == 1]
            if len(h1) != 1:
                self.issue("h1_count", f"Expected one H1; found {len(h1)}",
                           h1[1]["line"] if len(h1) > 1 else 1)
        for previous, current in zip(self.headings, self.headings[1:]):
            before, after = previous["level"], current["level"]
            if after > before + 1:
                self.issue("heading_skip", f"Heading level skips from H{before} to H{after}",
                           current["line"])
        lines = (" ".join(line.split()) for line in "".join(self.parts).split("\n"))
        return {
            "text": "\n".join(line for line in lines if line),
            "title": self.title,
            "meta_description": self.meta_description,
            "headings": self.headings,
            "issues": sorted(self.issues, key=lambda issue: issue["line"]),
            "gutenberg_compatibility": "unverified" if self.has_gutenberg else "not_applicable",
        }


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--mode", required=True, choices=("page", "fragment", "wp-body"))
    cli.add_argument("file", help="UTF-8 HTML file, or - for stdin")
    args = cli.parse_args()
    try:
        source = (sys.stdin.buffer.read() if args.file == "-" else Path(args.file).read_bytes())
        source = source.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    except (OSError, ValueError) as error:
        cli.error(str(error))
    parser = Preflight(args.mode)
    parser.feed(source)
    parser.close()
    report = parser.result()
    sys.stdout.buffer.write((json.dumps(report, ensure_ascii=False) + "\n").encode("utf-8"))
    return int(bool(report["issues"]))


if __name__ == "__main__":
    sys.exit(main())
