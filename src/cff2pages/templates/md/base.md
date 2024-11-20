{%- from 'md/authors_macro.md' import authors_block -%}
{%- from 'md/identifiers_macro.md' import identifier_block -%}
{%- from 'md/reference_macro.md' import references_block -%}
# {{ title }}

{{ authors_block(authors, unique_affiliations) -}}
{{- identifier_block(identifiers, repository) -}}

## Keywords

- Keyword 1
- Keyword 2
- Keyword 3

{{ references_block(references) }}