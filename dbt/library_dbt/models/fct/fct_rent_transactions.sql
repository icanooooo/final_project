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

WITH rent_transaction AS (
    SELECT
        *
    FROM {{ source('source', 'rent_data') }}
)

SELECT
    *,
    date_diff(return_date, rent_date, DAY) as no_rent_days,
FROM rent_transaction
{% if is_incremental() %}
    WHERE created_at > (
        SELECT MAX(created_at)
        FROM {{ this }}
    )
{% endif %}