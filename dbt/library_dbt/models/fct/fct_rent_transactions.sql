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
    FROM {{ ref('production_library_rent_transaction_source') }}
)

SELECT
    *,
    date_diff(return_date, rent_date, DAY) as no_rent_days,
FROM rent_transaction
{% if is_incremental() %}
    WHERE updated_at > (
        SELECT MAX(updated_at)
        FROM {{ this }}
    )
{% endif %}