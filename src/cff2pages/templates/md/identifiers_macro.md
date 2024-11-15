{% macro identifier_block(identifiers, repository) %}

## Identifiers

{%- if identifiers is defined %}
- [repository]({{ repository }})

    {%- for identifier in identifiers -%}
        {%- if identifier['type'] == 'swh' -%}
            {%- if repository is defined %}
- [SWH - Archive](https://archive.softwareheritage.org/browse/origin/?origin_url={{ repository }})
            {%- else -%}
- [SWH - Archive](https://archive.softwareheritage.org/{{ identifier['value'] }})
            {%- endif -%}
        {%- elif identifier['type'] == 'doi' %}
- [{{ identifier['value'] }}](https://doi.org/{{ identifier['value'] }})
        {%- endif -%}
    {%- endfor %}
{%- endif %}
{% endmacro %}