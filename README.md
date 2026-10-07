# 🚀 CLI Data Sanitizer & Validator Engine

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-red.svg)](https://docs.pydantic.dev/latest/)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A interactive Command Line Interface (CLI) application designed to validate and sanitize dataset streams (CSV) against dynamically generated **Pydantic V2** schemas defined in YAML or JSON.

Built with a clean modular architecture separating Core Logic, I/O Operations, and Interactive Terminal UI.

---

## 🎯 Key Features

- **Dynamic Schema Metaprogramming:** Builds type-safe Pydantic models at runtime from human-readable YAML/JSON definitions.
- **Memory-Efficient Streaming:** Processes datasets row-by-row using Python generators, keeping memory footprint low even for large files.
- **Interactive Terminal REPL:** Built with `Questionary` and `Rich` for guided data validation and live schema editing.
- **Robust Field Validation & Sanitization:**
  - Type checking (`str`, `int`, `float`, `bool`, `date`, `datetime`, `email`).
  - Boundary limits (`min`, `max`, `min_length`, `max_length`).
  - Safe null handling and optional field defaults.
- **Encoding & Edge Case Handling:** Automatic UTF-8 with BOM stripping (`utf-8-sig`) for seamless compatibility with Microsoft Excel exports.
- **Detailed Audit & Reporting:** Generates structured JSON output files for valid records (`valid_data.json`) and error logs (`errors.json`).

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Data Validation:** Pydantic V2 (`create_model`, `Field`, `SchemaValidator`)
- **CLI & UI:** `Rich` (tables, status indicators) & `Questionary` (interactive prompts)
- **Configuration & I/O:** `PyYAML`, `json`, `csv`
- **Package Manager & Tooling:** `uv`, `pytest`

---

## 🏗️ Architecture & Project Structure

The project follows solid Object-Oriented and Clean Code practices, enforcing single responsibility for each layer:

```text
src/cli_data_validator/
├── core/               # Domain & Validation Logic
│   ├── engine.py       # Dataset processing engine & metric calculations
│   ├── factory.py      # Dynamic Pydantic model creation
│   └── loader.py       # Configuration schema parsing (YAML/JSON)
├── io/                 # Input/Output Stream Handlers
│   ├── readers.py      # CSV generator-based file streaming
│   └── writers.py      # JSON result and error report export
└── ui/                 # Presentation & REPL Layer
    ├── menu.py         # Main interactive terminal loop
    └── reporter.py     # Rich table rendering for summaries & error logs