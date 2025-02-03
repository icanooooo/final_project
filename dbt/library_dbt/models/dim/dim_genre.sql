{{
    config(
        materialized='table'
    )
}}

with books_dims AS (
    SELECT
        *
    FROM {{ source('source', 'books_data') }}
)

SELECT
    DISTINCT(genre) as genre,
    COUNT(genre) as genre_count
FROM books_dims
GROUP BY genre