{{
    config(
        materialized='table')
}}

with book_source AS (
    SELECT
        *
    FROM {{ source('purwadika', 'books_data') }}
)

SELECT
    *
FROM book_source