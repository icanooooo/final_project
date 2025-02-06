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

with member_source AS (
    SELECT
        *
    FROM {{ source('purwadika', 'member_data')}}
)

SELECT
    *
FROM member_source
{% if is_incremental() %}
    WHERE updated_at > (
        SELECT MAX(updated_at)
        FROM {{ this }}
    )
{% endif %}