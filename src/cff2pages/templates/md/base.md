{%- from 'md/authors_macro.md' import authors_block -%}
{%- from 'md/identifiers_macro.md' import identifier_block -%}
{%- from 'md/citation_macro.md' import cite_as -%}
{%- from 'md/keyword_macro.md' import keyword_block -%}
{%- from 'md/reference_macro.md' import references_block -%}

# {{ title }}

{{ authors_block(authors, unique_affiliations) }}
{{ identifier_block(identifiers, repository) }}

{{ keyword_block(keywords) }}

{{ cite_as(citation) }}

{{ references_block(references) }}