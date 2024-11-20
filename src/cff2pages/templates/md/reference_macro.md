{%- macro references_block(references) -%}
{%- if references is defined %}
## References

{% for reference in references %}
* {% if reference.type == 'article' %}📖{% elif reference.type == 'software' %}💻{%- endif %} {{ reference.title }}, {% for author in reference['authors'] %}{{+ author['given-names'] }} {{ author['family-names'] -}} {%- if author.orcid is defined -%} [![Author ORCID](./assets/img/orcid_16x16.webp)]({{ author.orcid }}){style="margin:3px"}{%- endif %}{%- if not loop.last %}, {% endif %}{%- endfor %}{% if reference.year %} {{- reference.year -}}{% endif %} [{{- reference.doi -}}](https://doi.org/{{ reference.doi }}){% endfor %}
{%- endif %}
{% endmacro %}