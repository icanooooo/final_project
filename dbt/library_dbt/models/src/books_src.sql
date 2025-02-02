{{ config(
    materialized='table'
) }}


with book_source AS (
    SELECT
        *
    FROM `purwadika.ihsan_perpustakaan_capstone_project_3.books`
)

SELECT
    *
FROM book_source