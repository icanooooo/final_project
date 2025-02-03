{{
    config(
        materialized='table'
    )
}}

WITH rent_transaction AS (
    SELECT
        *
    FROM {{ source('data_models', 'rent_data') }}
)

SELECT
    *
FROM rent_transaction