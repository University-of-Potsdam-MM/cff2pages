{%- macro authors_block(authors, unique_affiliations) -%}
## Author(s)
{%- for author in authors %}
- {{ author['given-names'] }} {{ author['family-names'] }} 
    {%- if author.affiliation is defined -%}
[ {{- unique_affiliations.index(author.affiliation) + 1 -}} ]
    {%- endif %}
    {%- if author.orcid is defined -%}
, ORCID: [{{ author.orcid.split('/')[-1] }}]({{ author.orcid }})
    {%- endif %}
{%- endfor %} 

{% for affiliate in unique_affiliations -%}
{{ unique_affiliations.index(affiliate) + 1 }}. {{ affiliate }}
{% endfor -%}
{% endmacro %}