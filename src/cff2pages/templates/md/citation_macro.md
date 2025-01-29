{#
File: citation_macro.md
Description: This file defines a macro `cite_as` which generates an APA-style citation block in Markdown.
Usage: `{% from 'citation_macro.md' import cite_as %}`
Parameters:
    - citation (dict): A dictionary that should include at least an 'apa' key for the citation text in APA format.
        Example:
        citation = {
            'apa': 'Author, A. A. (Year). Title of work. Publisher.',
            'mla': 'Author, A. A. "Title of Work." Publisher, Year.'
        }
Features:
    - Displays citation in APA format.
Dependencies:
    - Relies on a `citation['apa']` key in the passed dictionary.
#}
{% macro cite_as(citation) %}
    {%- if citation is defined %}
## Cite as (APA):
{{ citation['apa'] }}
    {%- endif %}
{% endmacro %}