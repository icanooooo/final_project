{{
    config (
        materialized='table'
    )
}}

WITH members_dims AS (
    SELECT
        *
    FROM {{ source('source', 'member_data') }}
)

SELECT
    *
FROM members_dims