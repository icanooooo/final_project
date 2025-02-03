{{
    config(
        materialized='table'
    )
}}

WITH rent_transaction AS (
    SELECT
        *
    FROM {{ source('source', 'rent_data') }}
)

SELECT
    *
FROM rent_transaction