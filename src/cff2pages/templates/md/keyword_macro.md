{#
File: keyword_macro.html
Description: This file defines a macro `keyword_block` that generates a list of keywords in an HTML unordered list format. The keywords are displayed as clickable items, styled within a container for better presentation.
Usage: `{% from 'keyword_block_macro.html' import keyword_block %}`
Parameters:
    - keywords (list of strings): A list of keywords to be displayed. Each keyword is rendered as a clickable item.
        Example:
        keywords = ['Python', 'Jinja2', 'Web Development', 'Template Engine']
Features:
    - Displays keywords in a structured list format (`<ul>`), with each keyword enclosed in a `<li>`.
    - Each keyword is wrapped in an anchor tag (`<a>`) for easy styling or linking.
    - If no keywords are provided, the block will not be rendered.
    - Flexible layout for easy integration into different web designs.
Dependencies:
    - Expects a list of strings as the `keywords` parameter. It assumes basic CSS styling classes such as `keyword-container`, `keyword-list`, and `keyword-item` to handle the layout.
#}
{% macro keyword_block(keywords) %}
    {%- if keywords is defined -%}
# Keywords

        {%- for keyword in keywords %}
- {{ keyword }}
        {%- endfor %}
    {% endif %}
{% endmacro %}
