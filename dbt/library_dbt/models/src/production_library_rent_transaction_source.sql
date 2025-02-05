{{
    config(
        materialized='table')
}}

with rent_transactions AS (
    SELECT
        *
    FROM {{ source('purwadika', 'rent_data')}}
)

SELECT
    *
FROM rent_transactions