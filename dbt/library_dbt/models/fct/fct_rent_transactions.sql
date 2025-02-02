{{
    config(
        materialized='table'
    )
}}

WITH rent_transaction AS (
    SELECT
        *
    FROM {{ ref('production_library_rent_transaction_source') }}
)

SELECT
    *
FROM rent_transaction