{{
    config(
        materialized='table')
}}

with member_source AS (
    SELECT
        *
    FROM {{ source('purwadika', 'member_data')}}
)

SELECT
    *
FROM member_source