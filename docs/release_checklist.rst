Release Checklist
=================

This checklist ensures consistent and complete steps when preparing a new release of ``cff2pages``.

Required Steps
--------------

- **Update version in code**
  - Edit ``__version__`` in ``src/cff2pages/__init__.py``

- **Update version in CITATION.cff**
  - Ensure it matches the code version exactly

- **Prepare changelog**
  - Add a section to ``CHANGELOG.md`` with bullet points for new features, fixes, or changes

- **Add release date to changelog**
  - Use the format: ``## 0.2.1 (YYYY-MM-DD)``

- **Commit version changes**
  - Stage and commit ``__init__.py``, ``CITATION.cff``, and ``CHANGELOG.md``

- **Create a Git tag for the release**
  - Example::

       git tag v0.2.1
       git push origin v0.2.1

- **Publish a GitHub release**
  - Go to: https://github.com/University-of-Potsdam-MM/cff2pages/releases
  - Create a release based on the Git tag
  - Paste the corresponding changelog section

- **Check the documentation**
  - Ensure GitHub Pages deployment succeeded and the updated docs and citation page are live
