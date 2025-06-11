# Changelog

## 0.2.1 (2025-06-11) Conversion to md

* created jinja templates to convert into md files in the same style as HTML files
* reworked tests, based on cff files in tests/fixtures a test searches for md and html files in tests/expected
* rework documentation that Github Actions produces documentations as well and link to the cff2pages generated page
  * generated docs from README
  * integrated changelog into docs
* updated toml to give more metadata

## 0.2.0 (2024-10-09) Starting to convert to md output

* Added support for HTML and Markdown output.
  * Implemented argument parsing for input file and output path.
  * **Behavior change**: The default output file is now `public/citation.html`.
  * Markdown output is not yet fully supported.
* Included a "Cite As" box in the HTML output.
* Fixed issue allowing authors without affiliations.
* Refactored templates to encapsulate all modules.
* Added docstrings; Sphinx documentation to be added in the future.

## 0.1.0 (2023-09-06) Added references

* convert references
* added tests for new conversion

## 0.0.3 (2023-08-11) Tested all features

* added Zenodo DOI to Citation.cff
* moved CSS-styles to its own file
* made generated html more readable
* added unit tests

## 0.0.2 (2023-08-04)

* added version test
* added publish action
* rework README

## 0.0.1 (2023-07-30) First Release

* create first html-page based on cff attributes:
  * title
  * authors
  * keywords
  * identifiers
  * licence
  * abstract