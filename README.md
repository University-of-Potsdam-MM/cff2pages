# cff2pages

[![SWH](https://archive.softwareheritage.org/badge/swh:1:dir:1e3e28077c43ca999f434f29b6a872f5581b48e2/)](https://archive.softwareheritage.org/swh:1:dir:1e3e28077c43ca999f434f29b6a872f5581b48e2;origin=https://github.com/University-of-Potsdam-MM/cff2pages;visit=swh:1:snp:42801fe381a3d143eb5a9b35dc6d144672fe6361;anchor=swh:1:rev:c3b1c832a3d2f5f90e1370fc5b529b3f5507471c)

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

## Roadmap

- [ ] simple conversion from cff to html
- [ ] 0.0.1 version in pypi
- [ ] working samples for GitHub and gitlab
- [ ] open up for discussions