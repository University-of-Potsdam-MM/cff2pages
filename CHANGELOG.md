# Changelog

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