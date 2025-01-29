{%- from 'md/authors_macro.md' import authors_block -%}
{%- from 'md/identifiers_macro.md' import identifier_block -%}
{%- from 'md/reference_macro.md' import references_block -%}
{%- from 'md/keyword_macro.md' import keyword_block -%}

# {{ title }}

{{ authors_block(authors, unique_affiliations) }}
{{ identifier_block(identifiers, repository) }}

{{ keyword_block(keywords) }}

{{ references_block(references) }}