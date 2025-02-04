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

with rent_transactions AS (
    SELECT
        *
    FROM {{ source('purwadika', 'rent_data')}}
)

SELECT
    *
FROM rent_transactions
{% if is_incremental() %}
    WHERE updated_at > (
        SELECT MAX(updated_at)
        FROM {{ this }}
    )
{% endif %}