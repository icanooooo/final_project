{% snapshot snapshots_src_books %}

{{
    config(
        target_schema='ihsan_dwh_snapshots',
    )
}}

-- dbt snapshots are using timestamp which automatically converts to UTC

SELECT
    *,
    timestamp(updated_at, 'Asia/Jakarta') AS model_updated_at 
FROM {{ source('purwadika', 'books_data') }}

{% endsnapshot %}