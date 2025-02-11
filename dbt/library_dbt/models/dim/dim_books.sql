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

WITH books_dims AS (
    SELECT
        *
    FROM {{ ref('production_library_books_source') }}
)

SELECT
    *
FROM books_dims
{% if is_incremental() %}
    WHERE updated_at > (
        SELECT MAX(updated_at)
        FROM {{ this }}
    )
{% endif %}