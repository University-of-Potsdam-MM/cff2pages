Testing Strategy
================

Overview
--------

The testing routine for `cff2pages` ensures that `.cff` files are correctly converted into their respective HTML or Markdown outputs.
The test systematically verifies that the transformation is both **structurally accurate** and **visually consistent**
by comparing actual output with predefined expected results.

Test Workflow
-------------

The function `test_cff_files` implements the core testing strategy using `unittest`. It performs the following:

1. **Iterate Through Fixture Files**
   All `.cff` files in the `fixtures` directory are collected and tested one by one.

2. **HTML Conversion Subtest**
   For each `.cff` file:

   - It is converted to an HTML output using the main conversion routine.
   - The output HTML is parsed to extract the `<div class="container">` body.
   - The result is cleaned by removing `<script>` tags and prettified for comparison.
   - It is then compared with a known good `expected_*.html` file.

3. **Markdown Conversion Subtest**
   Similarly:

   - The `.cff` file is converted to a Markdown output.
   - The result and its expected Markdown file are converted to HTML using the `markdown` Python module.
   - The rendered HTMLs are compared directly.

4. **Subtest Separation**
   Each `.cff` file is run as a separate subtest for both formats (`html` and `md`), allowing clear test reports and isolation of failures.

Fixtures Used
-------------

Currently, the test suite includes **three `.cff` files** in the `fixtures/` directory:

- **`current.cff`**  `see here <_static/citation/current.html>`_
  A rich example with up-to-date metadata using all common fields. This represents a typical well-documented project file.

- **`diacritics.cff`** `see here <_static/citation/diacritics.html>`_
  Focuses on handling of special characters and diacritical marks to ensure proper Unicode and HTML rendering.

- **`minimal.cff`** `see here <_static/citation/minimal.html>`_
  A reduced file that only includes required fields, validating that even minimal metadata can be processed correctly.

Each fixture file has corresponding expected output files in both HTML and Markdown formats for regression testing.

Key Components
--------------

- **Fixtures**: Input `.cff` files to test various metadata combinations.
- **Expected Files**: Pre-rendered outputs (`expected_*.html`, `expected.md`) serve as baselines.
- **Temporary Directory**: Each test runs in isolation within a temporary directory.
- **HTML Structure Comparison**: Uses BeautifulSoup to normalize and compare the structure of HTML outputs.
- **Script Tag Removal**: Script content is stripped to avoid dynamic noise during testing.

Example Output Naming
---------------------

- For a file `example.cff`, the test will compare:

  - HTML: `expected_example_body.html`
  - Markdown: `expected_example.md`

