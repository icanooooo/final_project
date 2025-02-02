{{
    config (
        materialized='table'
    )
}}

WITH members_dims AS (
    SELECT
        *
    FROM {{ ref('production_library_members_source') }}
)

SELECT
    *
FROM members_dims