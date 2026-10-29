# Rendering contract

The Markdown file is immutable input. The helper hashes it before recording a successful
manifest and never asks a model to rewrite it during rendering.

## Supported content

- CommonMark headings, paragraphs, lists, blockquotes, rules, links, and emphasis.
- Pipe tables and strikethrough.
- Fenced and indented code blocks with Pygments syntax highlighting. Long lines wrap rather
  than clip.
- Local, data-URI, and HTTPS images. Local and remote images are copied into an isolated
  staging directory. Missing or non-image assets fail the render instead of disappearing.
- Mermaid fenced blocks. A pinned local Mermaid browser bundle parses them first, then
  Playwright waits for SVG rendering before Edge creates the PDF. Mermaid errors fail the
  render.

Raw HTML is disabled. This prevents response content from executing arbitrary script. PDF
page wrapping necessarily differs from chat layout, but visible wording, punctuation, code,
link labels, and document order are not intentionally changed.

## Verification

The helper reopens every PDF with `pypdf`, requires at least one page, extracts text, and
checks visible Markdown fragments against the extracted text. It records source and PDF
SHA-256 hashes in a manifest and verifies external hyperlink targets. When `--qa-dir` is
supplied, Poppler renders every page to PNG; the invoking agent must inspect all of them
visually.

Text extraction cannot prove visual correctness, and raster inspection cannot prove source
identity. Both checks are required for a delivered PDF.
