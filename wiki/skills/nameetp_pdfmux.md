---
id: nameetp_pdfmux
type: concept
title: NameetP/pdfmux
tags:
- pdf-extraction
- mcp-server
- rag
- document-processing
- ocr
confidence: 0.65
created_at: '2026-05-13'
last_reinforced: '2026-05-13'
sources:
- https://github.com/NameetP/pdfmux
section: Server Implementations > 🔎 <a name="search"></a>Search & Data Extraction
---

> [![pdfmux MCP server](https://glama.ai/mcp/servers/NameetP/pdfmux/badges/score.svg)](https://glama.ai/mcp/servers/NameetP/pdfmux) 🐍 🏠 - PDF extraction router with built-in MCP server. Classifies each page (digital, scanned, tables) and routes to the best backend (PyMuPDF, Docling, OCR, or optional LLM fallback). Per-page confidence scoring flags low-quality pages and auto-reextracts them — prevents silent RAG failures. Zero config: `pip install pdfmux`. MIT licensed.

pdfmux is a PDF extraction router that includes a built-in MCP server. It classifies each page as digital, scanned, or containing tables, then routes it to the best backend (PyMuPDF, Docling, OCR, or optional LLM). Per-page confidence scoring flags low-quality pages and automatically re-extracts them, preventing silent RAG failures. It requires zero configuration and can be installed with 'pip install pdfmux'.

**Category:** Server Implementations > 🔎 <a name="search"></a>Search & Data Extraction
**Source:** [https://github.com/NameetP/pdfmux](https://github.com/NameetP/pdfmux)
