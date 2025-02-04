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

with book_source AS (
    SELECT
        *
    FROM {{ source('purwadika', 'books_data') }}
)

SELECT
    *
FROM book_source
{% if is_incremental() %}
    WHERE created_at > (
        SELECT MAX(created_at)
        FROM {{ this }}
    )
{% endif %}