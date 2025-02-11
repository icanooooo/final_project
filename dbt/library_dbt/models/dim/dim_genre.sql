{{
    config(
        materialized='table'
    )
}}

with books_dims AS (
    SELECT
        *
    FROM {{ ref('production_library_books_source') }}
)

SELECT
    DISTINCT(genre) as genre,
    COUNT(genre) as genre_count
FROM books_dims
GROUP BY genre