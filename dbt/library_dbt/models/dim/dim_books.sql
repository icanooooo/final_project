{{
    config(
        materialized='table'
    )
}}

WITH books_dims AS (
    SELECT
        *
    FROM {{ source('source', 'books_data') }}
)

SELECT
    *
FROM books_dims