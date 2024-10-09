# cff2pages

[![pypi](https://img.shields.io/pypi/v/cff2pages.svg)](https://pypi.org/project/cff2pages/)
[![SWH](https://archive.softwareheritage.org/badge/origin/https://github.com/University-of-Potsdam-MM/cff2pages/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/University-of-Potsdam-MM/cff2pages)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8213987.svg)](https://doi.org/10.5281/zenodo.8213986)
[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu)

## Motivation

The Citation.cff is a fantastic format that combines human-readable and machine-readable metadata
about its repository. It provides linking systems with important metadata about the
presented project and gives people the ability to reference the project, among other things.
However, for a wide range of users, the YAML file format can seem intimidating, whereas a clean
website is generally more readable. This project aims to automate the conversion of cff files,
so that maintaining the cff file pays off for developers in terms of the project's presentation,
thereby ensuring that the website representation is retained.

## Project Description

cff2pages is envisioned as a Python package, designed to automate the extraction of metadata from
your project's Citation.cff file, and swiftly generate a sleek, static HTML page. This versatile
page can serve as a vivid representation of your project on Github/Gitlab Pages.

## Usage

```` bash
cd project_folder
pip install cff2pages
cff2pages
````

### Gitlab CI Runner

````yaml
stages:
  - Pages

pages:
  stage: Pages
  image: python:3.11
  script:
    - python -m pip install cff2pages
    - cff2pages -o public/index.html
  artifacts:
    paths:
      - public
````

### Github Workflow

````yaml
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Set up Python 3.11
        uses: actions/setup-python@v3
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install cff2pages
          cff2pages -o public/index.html
      - name: Setup Pages
        uses: actions/configure-pages@v3
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v2
        with:
          path: './public'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v2
````

## Roadmap

- [x] 0.0.1 version in pypi
- [ ] convert all cff-attributes
  - [x] abstract
  - [x] authors
  - [ ] cff-version
  - [ ] commit
  - [ ] contact
  - [ ] date
  - [ ] doi
  - [ ] identifiers
    - [x] doi
    - [x] swh
    - [ ] url
  - [x] keywords
  - [x] license
  - [ ] license-url
  - [ ] message
  - [ ] preferred-citation
  - [x] references (new, but not published!)
  - [ ] repository
  - [ ] repository-artifact
  - [x] repository-code
  - [x] title
  - [ ] type
  - [ ] url
  - [ ] version
- [x] simple conversion from cff to html
- [x] working samples for GitHub and gitlab
- [ ] integrate cff2pages into given html
- [ ] change styles