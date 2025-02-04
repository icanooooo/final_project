{{
    config(
        materialized='incremental',
        unique_key='id',
            partition_by={
                "field": "created_at",
                "data_type": "timestamp"
            }
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
{% if is_incremental() %}
    WHERE created_at > (
        SELECT MAX(created_at)
        FROM {{ this }}
    )
{% endif %}