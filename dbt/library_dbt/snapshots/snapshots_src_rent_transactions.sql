{% snapshot snapshots_src_rent_transactions %}
{{
    config(
        target_schema='ihsan_dwh_perpustakaan_snapshots',
    )
}}
-- dbt snapshots are using timestamp which automatically converts to UTC

SELECT
    *,
    timestamp(updated_at, 'Asia/Jakarta') AS model_updated_at 
FROM {{ ref('production_library_rent_transaction_source') }}

{% endsnapshot %}