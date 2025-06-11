CI/CD Integration
=================

GitLab CI Example
-----------------

Add the following snippet to your `.gitlab-ci.yml`:

.. code-block:: yaml

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

GitHub Actions Workflow
-----------------------

Here’s an example GitHub workflow to deploy to GitHub Pages:

.. code-block:: yaml

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
