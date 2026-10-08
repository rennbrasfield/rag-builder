"""Automated tests for tools/quote_check.py.

Every case is planted on purpose: some must pass, some must fail, some must ask for a manual
check. Test builds are created in a temporary folder at run time and deleted afterwards, so no
build-like files ever live in this repository (the commit guard would block them anyway).

Run from the repository root:
    .venv/bin/python -m unittest discover -s tests -v
"""

import contextlib
import hashlib
import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import quote_check  # noqa: E402

from pypdf import PdfWriter  # noqa: E402

POLICY_TEXT = (
    "Travel Policy\n"
    "Employees must book flights\n"
    "through the approved portal.\n"
    "Policy owner: Operations.\n"
)
PDF_TEXT = "Data retention: customer records are deleted after 24 months."


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_docx(path, text_runs):
    runs = "".join(f'<w:r><w:t xml:space="preserve">{t}</w:t></w:r>' for t in text_runs)
    xml = f'<?xml version="1.0"?><w:document xmlns:w="w"><w:body><w:p>{runs}</w:p></w:body></w:document>'
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", xml)


def write_text_pdf(path, text):
    """A minimal one-page PDF whose page contains real, extractable text."""
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = b"%PDF-1.4\n", []
    for i, obj in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + obj + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    Path(path).write_bytes(out)


def write_scanned_pdf(path):
    """A PDF page with no text layer, like a scan."""
    writer = PdfWriter()
    writer.add_blank_page(612, 792)
    with open(path, "wb") as f:
        writer.write(f)


class QuoteCheckTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self._tmp.name)
        (self.ws / "inputs").mkdir()
        (self.ws / "correspondence" / "responses").mkdir(parents=True)

        (self.ws / "inputs" / "policy.txt").write_text(POLICY_TEXT)
        write_docx(self.ws / "inputs" / "contracts.docx", ["All contracts are stored in the", " legal drive."])
        write_text_pdf(self.ws / "inputs" / "retention.pdf", PDF_TEXT)
        write_scanned_pdf(self.ws / "inputs" / "scan.pdf")
        (self.ws / "correspondence" / "responses" / "it-reply.txt").write_text(
            "Hi, our data must stay in the EU region only.\nThanks"
        )

        files = ["policy.txt", "contracts.docx", "retention.pdf", "scan.pdf"]
        inputs = "\n".join(
            f"  - {{file: inputs/{f}, sha256: {sha(self.ws / 'inputs' / f)}}}" for f in files
        )
        (self.ws / "build.yaml").write_text(
            "build: {name: test-build}\n"
            f'tool: {{path: "{REPO}", variable_catalog: v1.1.0}}\n'
            f"inputs:\n{inputs}\n"
        )

    def tearDown(self):
        self._tmp.cleanup()

    def run_check(self, entries):
        (self.ws / "evidence.yaml").write_text("evidence:\n" + "".join(f"  - {e}\n" for e in entries))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = quote_check.main(["quote_check.py", str(self.ws)])
        return code, buf.getvalue()

    def section(self, output, label):
        """Return the lines listed under one result heading (e.g., 'FAIL')."""
        lines, capture = [], False
        for line in output.splitlines():
            if line.startswith(f"{label}:"):
                capture = True
                continue
            if capture:
                if not line.startswith("  "):
                    break
                lines.append(line.strip())
        return lines

    # --- must PASS -------------------------------------------------------------------------

    def test_exact_quote_from_text_file_passes(self):
        code, out = self.run_check(
            ['{id: EV-1, source: {type: document, file: inputs/policy.txt}, quote: "Policy owner: Operations.", supports: [B21]}']
        )
        self.assertEqual(code, 0)
        self.assertIn("EV-1: inputs/policy.txt", self.section(out, "PASS"))

    def test_quote_with_different_line_breaks_passes_as_whitespace_only(self):
        code, out = self.run_check(
            ['{id: EV-2, source: {type: document, file: inputs/policy.txt}, quote: "Employees must book flights through the approved portal.", supports: [B15]}']
        )
        self.assertEqual(code, 0)
        self.assertTrue(any(l.startswith("EV-2:") for l in self.section(out, "PASS (whitespace only)")))

    def test_quote_from_word_document_passes(self):
        code, out = self.run_check(
            ['{id: EV-3, source: {type: document, file: inputs/contracts.docx}, quote: "All contracts are stored in the legal drive.", supports: [I1]}']
        )
        self.assertEqual(code, 0)
        self.assertIn("EV-3: inputs/contracts.docx", self.section(out, "PASS"))

    def test_quote_from_logged_reply_passes(self):
        code, out = self.run_check(
            ['{id: EV-4, source: {type: person, person: P-001, response_file: correspondence/responses/it-reply.txt}, quote: "our data must stay in the EU region only.", supports: [E2]}']
        )
        self.assertEqual(code, 0)
        self.assertIn("EV-4: correspondence/responses/it-reply.txt", self.section(out, "PASS"))

    def test_quote_from_text_pdf_passes(self):
        code, out = self.run_check(
            ['{id: EV-5, source: {type: document, file: inputs/retention.pdf}, quote: "customer records are deleted after 24 months.", supports: [E5]}']
        )
        self.assertEqual(code, 0)
        self.assertIn("EV-5: inputs/retention.pdf", self.section(out, "PASS"))

    # --- must FAIL -------------------------------------------------------------------------

    def test_invented_quote_fails(self):
        code, out = self.run_check(
            ['{id: EV-6, source: {type: document, file: inputs/policy.txt}, quote: "Employees may book any airline.", supports: [B15]}']
        )
        self.assertEqual(code, 1)
        self.assertTrue(any("EV-6: quote not found" in l for l in self.section(out, "FAIL")))

    def test_invented_quote_from_pdf_fails(self):
        code, out = self.run_check(
            ['{id: EV-7, source: {type: document, file: inputs/retention.pdf}, quote: "customer records are kept forever.", supports: [E5]}']
        )
        self.assertEqual(code, 1)
        self.assertTrue(any(l.startswith("EV-7: quote not found") for l in self.section(out, "FAIL")))

    def test_unknown_variable_id_fails(self):
        code, out = self.run_check(
            ['{id: EV-8, source: {type: document, file: inputs/policy.txt}, quote: "Policy owner: Operations.", supports: [Z9]}']
        )
        self.assertEqual(code, 1)
        self.assertTrue(any("unknown variable IDs ['Z9']" in l for l in self.section(out, "FAIL")))

    def test_document_changed_after_intake_fails_even_if_quote_still_present(self):
        with open(self.ws / "inputs" / "policy.txt", "a") as f:
            f.write("edited\n")
        code, out = self.run_check(
            ['{id: EV-9, source: {type: document, file: inputs/policy.txt}, quote: "Policy owner: Operations.", supports: [B21]}']
        )
        self.assertEqual(code, 1)
        self.assertTrue(any("changed since intake" in l for l in self.section(out, "FAIL")))

    def test_missing_source_file_fails(self):
        code, out = self.run_check(
            ['{id: EV-10, source: {type: document, file: inputs/nope.txt}, quote: "x", supports: [B1]}']
        )
        self.assertEqual(code, 1)
        self.assertTrue(any("source file not found" in l for l in self.section(out, "FAIL")))

    # --- must ask for a MANUAL CHECK -------------------------------------------------------

    def test_statement_without_logged_reply_needs_manual_check(self):
        code, out = self.run_check(
            ['{id: EV-11, source: {type: person, person: me}, quote: "We use Google Workspace.", supports: [F1]}']
        )
        self.assertEqual(code, 0)
        self.assertTrue(any(l.startswith("EV-11:") for l in self.section(out, "MANUAL CHECK")))

    def test_scanned_pdf_needs_manual_check_not_false_fail(self):
        code, out = self.run_check(
            ['{id: EV-12, source: {type: document, file: inputs/scan.pdf}, quote: "anything", supports: [B4]}']
        )
        self.assertEqual(code, 0)
        self.assertTrue(any("likely a scan" in l for l in self.section(out, "MANUAL CHECK")))
        self.assertEqual(self.section(out, "FAIL"), [])

    # --- other behavior --------------------------------------------------------------------

    def test_superseded_entries_are_skipped(self):
        code, out = self.run_check(
            ['{id: EV-13, source: {type: document, file: inputs/policy.txt}, quote: "not in the file", supports: [B1], status: superseded}']
        )
        self.assertEqual(code, 0)
        self.assertIn("0 active evidence entries", out)

    def test_folder_without_build_yaml_is_rejected(self):
        with tempfile.TemporaryDirectory() as empty:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = quote_check.main(["quote_check.py", empty])
        self.assertEqual(code, 2)
        self.assertIn("not a build workspace", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
