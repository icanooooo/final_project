{{
    config(
        materialized='table'
    )
}}

WITH rent_transaction AS (
    SELECT
        *
    FROM {{ ref('fct_rent_transactions') }}
)

SELECT
    *
FROM rent_transaction