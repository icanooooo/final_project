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
    *,
    DATE_DIFF(CURRENT_DATE(), date_of_birth, year) AS age
FROM members_dims
{% if is_incremental() %}
    WHERE updated_at > (
        SELECT MAX(updated_at)
        FROM {{ this }}
    )
{% endif %}