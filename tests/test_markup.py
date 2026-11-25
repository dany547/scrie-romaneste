"""Standalone markup preflight CLI contract tests (synthetic HTML only)."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def run_script(name, *args, source=b"", **kwargs):
    return subprocess.run([sys.executable, str(SCRIPTS / name), *args],
                          input=source, capture_output=True, **kwargs)


class TestMarkup(unittest.TestCase):
    def report(self, source, mode="fragment", status=0):
        result = run_script("check-markup.py", "--mode", mode, "-",
                            source=source.encode("utf-8"))
        self.assertEqual(result.returncode, status, (result.stdout, result.stderr))
        self.assertEqual(result.stderr, b"")
        self.assertEqual(len(result.stdout.splitlines()), 1)
        return json.loads(result.stdout.decode("utf-8"))

    def test_page_extracts_title_separately_and_keeps_prose(self):
        report = self.report('''<!doctype html>
<html><head><title>Știri &amp; sfaturi &amp;lt;</title>
<meta NAME="Description" content="Azi &quot;pe bune&quot; &amp;amp;"></head>
<body><h1>Ghid de <em>lectură</em></h1>
<p>Prima <strong>zi</strong>, apoi&nbsp;șase.<br>Continuăm.</p>
<ul><li>Unu</li><li>Doi</li></ul>
<div hidden="false"><h2>Nu apare</h2></div>
<!-- Comentariu --><template><p>Șablon</p></template><style>exemplu</style>
<p>Co<em>pil</em> &lt; 12 &amp;lt; 13.</p>
</body></html>''', "page")
        self.assertEqual(report, {
            "text": "Ghid de lectură\nPrima zi, apoi șase.\nContinuăm.\nUnu\nDoi\nCopil < 12 &lt; 13.",
            "title": "Știri & sfaturi &lt;",
            "meta_description": 'Azi "pe bune" &amp;',
            "headings": [{"level": 1, "text": "Ghid de lectură", "line": 4}],
            "issues": [],
            "gutenberg_compatibility": "not_applicable",
        })

    def test_wp_body_keeps_aria_hidden_prose_but_not_svg_title(self):
        report = self.report('<p aria-hidden=true>Text vizibil.</p>'
                             '<svg><title>Pictogramă</title></svg>'
                             '<p hidden>Text ascuns.</p>'
                             '<meta name="description" content="Nu este metadată">', "wp-body")
        self.assertEqual(report["text"], "Text vizibil.")
        self.assertIsNone(report["title"])
        self.assertIsNone(report["meta_description"])

    def test_only_document_head_supplies_page_metadata(self):
        report = self.report('<!doctype html><html><title>Titlu &amp; știri</title>'
                             '<meta name="description" content="Rezumat">'
                             '<h1>Articol</h1></html>', "page")
        self.assertEqual(report["title"], "Titlu & știri")
        self.assertEqual(report["meta_description"], "Rezumat")
        self.assertEqual(report["text"], "Articol")

        report = self.report('<svg><title>Pictogramă</title><title /></svg>'
                             '<math><title>Formulă</title></math>'
                             '<h1>Articol</h1><title>Titlu în corp</title>'
                             '<meta name="description" content="Metadată în corp">', "page")
        self.assertIsNone(report["title"])
        self.assertIsNone(report["meta_description"])
        self.assertEqual(report["text"], "Articol")

    def test_entities_reach_existing_sedilla_scanner(self):
        report = self.report("<p>Solu&#355;ia și &#x15f;coala.</p>")
        self.assertEqual(report["text"], "Soluţia și şcoala.")
        result = run_script("verifica.py", "--fara-seo", "-",
                            source=report["text"].encode("utf-8"))
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(b"critic|sedila", result.stdout)

    def test_body_modes_do_not_assume_an_h1_or_metadata(self):
        for mode, expected in (("fragment", "not_applicable"), ("wp-body", "unverified")):
            with self.subTest(mode=mode):
                report = self.report("<h3>Start</h3><h4>Detalii</h4>", mode)
                self.assertIsNone(report["title"])
                self.assertIsNone(report["meta_description"])
                self.assertEqual(report["issues"], [])
                self.assertEqual(report["gutenberg_compatibility"], expected)
                self.assertEqual(self.report("<h1>A</h1><h1>B</h1>", mode)["issues"], [])

    def test_h1_count_and_relevant_heading_skips(self):
        for source in ("<h2>Subtitlu</h2>", "<h1>A</h1><h1>B</h1>"):
            with self.subTest(source=source):
                issues = self.report(source, "page", status=1)["issues"]
                self.assertEqual([issue["category"] for issue in issues], ["h1_count"])
        for mode, level in (("page", 1), ("fragment", 2), ("wp-body", 2)):
            with self.subTest(mode=mode):
                report = self.report(f"<h{level}>A</h{level}>\n<h4>B</h4>\n<h2>C</h2>",
                                     mode, status=1)
                self.assertEqual(report["issues"], [{"line": 2, "category": "heading_skip",
                                                     "detail": f"Heading level skips from H{level} to H4"}])

    def test_valid_nested_blocks_and_self_closing_blocks(self):
        source = '''<!-- wp:group {"layout":{"type":"constrained"}} -->
<!-- wp:acme/widgets {"label":"https://example.test/a/","flags":[true,null]} -->
<!-- wp:paragraph --><p>Text</p><!-- /wp:core/paragraph -->
<!-- wp:acme/divider /--><!-- wp:spacer {"height":"2em"} /-->
<!-- /wp:acme/widgets --><!-- /wp:group -->'''
        for mode in ("fragment", "wp-body"):
            with self.subTest(mode=mode):
                report = self.report(source, mode)
                self.assertEqual(report["text"], "Text")
                self.assertEqual(report["gutenberg_compatibility"], "unverified")

    def test_marker_names_attrs_and_pairing_with_recovery(self):
        source = '''<!-- wp: -->
<!-- wp:Custom/bad/name -->
<!-- wp:group -->
<!-- wp:paragraph {"broken":} -->
<!-- /wp:group -->
<!-- /wp:orphan -->
<!-- wp:paragraph -->
<!-- /wp:irrelevant -->
<!-- /wp:paragraph surplus -->
<!-- wp:acme/final -->'''
        report = self.report(source, status=1)
        self.assertEqual(report["gutenberg_compatibility"], "unverified")
        self.assertEqual([(issue["line"], issue["category"]) for issue in report["issues"]], [
            (1, "gutenberg_marker"), (2, "gutenberg_marker"), (4, "gutenberg_attrs"),
            (5, "gutenberg_pairing"), (6, "gutenberg_pairing"), (8, "gutenberg_pairing"),
            (9, "gutenberg_marker"), (10, "gutenberg_pairing"),
        ])
        for attrs in ("[1]", "42", "null", '{"a":NaN}', '{"a":Infinity}', '{&quot;a&quot;:1}'):
            with self.subTest(attrs=attrs):
                issues = self.report(f"<!-- wp:test {attrs} /-->", status=1)["issues"]
                self.assertEqual([issue["category"] for issue in issues], ["gutenberg_attrs"])

    def test_unterminated_marker_is_not_prose(self):
        report = self.report("<p>Proză</p>\n<!-- wp:paragraph", status=1)
        self.assertEqual(report["text"], "Proză")
        self.assertEqual(report["issues"][0]["line"], 2)
        self.assertEqual(report["issues"][0]["category"], "gutenberg_marker")
        self.assertEqual(self.report("<p>Proză</p><!-- notă")["text"], "Proză")

    def test_fake_raw_text_and_escaped_markers_are_not_gutenberg(self):
        report = self.report('''<script>"<!-- wp:missing --> <h1>Fake</h1>"</script>
<style>/* <!-- /wp:stray --> */</style>
<script /><!-- wp:fake --></script>
<textarea><!-- wp:fake --></textarea>
<title><!-- wp:fake --></title>
<p>&lt;!-- wp:paragraph --&gt; și &lt;h1&gt;literal&lt;/h1&gt;</p>''')
        self.assertEqual(report["text"], "<!-- wp:paragraph --> și <h1>literal</h1>")
        self.assertEqual(report["headings"], [])
        self.assertEqual(report["gutenberg_compatibility"], "not_applicable")

    def test_file_is_unchanged_and_stdout_is_utf8_independent_of_locale(self):
        source = b"\xef\xbb\xbf" + "<p>Șase</p>\r\n<h2>Încheiere</h2>".encode("utf-8")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "source.html"
            path.write_bytes(source)
            before = path.stat().st_mtime_ns
            result = run_script("check-markup.py", "--mode", "wp-body", str(path),
                                env=dict(os.environ, PYTHONIOENCODING="ascii"))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, b"")
            self.assertIn("Șase".encode("utf-8"), result.stdout)
            self.assertEqual(json.loads(result.stdout)["headings"][0]["line"], 2)
            self.assertEqual(path.read_bytes(), source)
            self.assertEqual(path.stat().st_mtime_ns, before)
            self.assertEqual(list(Path(folder).iterdir()), [path])

    def test_invalid_input_exits_2_with_no_report(self):
        with tempfile.TemporaryDirectory() as folder:
            cases = [((), b""), (("--mode", "unknown", "-"), b""),
                     (("--mode", "fragment", "-"), b"\xff"),
                     (("--mode", "page", str(Path(folder) / "absent.html")), b"")]
            for args, source in cases:
                with self.subTest(args=args, source=source):
                    result = run_script("check-markup.py", *args, source=source)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, b"")
                    self.assertIn(b"error:", result.stderr)
                    self.assertNotIn(b"Traceback", result.stderr)
