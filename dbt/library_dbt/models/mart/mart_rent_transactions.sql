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
    FROM {{ ref('fct_rent_transactions') }}
),
books AS (
    SELECT
        *
    FROM {{ ref('dim_books') }}
),
members AS (
    SELECT
        *
    FROM {{ ref('dim_members')}}
),
joint_rent_books AS (
    SELECT
        r.*,
        b.title as book_title,
        b.genre
    FROM rent_transaction AS r
    INNER JOIN books AS b
    ON r.book_id = b.id
),
joint_all AS (
    SELECT
        jrb.*,
        m.name AS renter_name,
        m.age AS renter_age
    FROM joint_rent_books as jrb
    INNER JOIN members as m
    ON jrb.library_member_id = m.id
)

SELECT
    id,
    book_id,
    book_title,
    library_member_id AS renter_id,
    renter_name,
    renter_age,
    FORMAT_DATE('%A', rent_date) AS rent_day,
    FORMAT_DATE('%A', return_date) AS return_day,
    rent_date,
    return_date,
    no_rent_days,
    created_at
FROM joint_all
{% if is_incremental() %}
    WHERE updated_at > (
        SELECT MAX(updated_at)
        FROM {{ this }}
    )
{% endif %}