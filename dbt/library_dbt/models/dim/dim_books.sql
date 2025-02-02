{{
    config(
        materialized='table'
    )
}}

WITH books_dims AS (
    SELECT
        *
    FROM {{ ref('production_library_books_source') }}
)

SELECT
    *
FROM books_dims