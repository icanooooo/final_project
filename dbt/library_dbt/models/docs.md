{% docs __overview__ %}
# Final Project (dbt)
Untuk Final Project, kami diminta untuk menggunakan dbt untuk proses data modelling. Kita
### Source
Source merupakan sumber data yang akan kita ambil untuk membuat model kita. Source didefinisikan sebagai dalam dbt untuk mengindentifikasi sumber data yang berasal dari luar project dbt. Kita akan menggunakan berikut dibawah sebagai *source* kita:
- `books`
- `member`
- `rent`

Ketiganya berasal dari dataset `ihsan_perpustakaan_final_project`.

### Source Tables (Preparation Layer)
*Source tables* atau *Preparation Layer* merupakan tabel yang biasa diambil dari *source* kita kedalam data warehouse yang dipilih. Tabel ini biasanya tidak di transform terlebih dahulu, menyediakan data sebagai *raw* untuk ditransformasi di tabel yang lain. 
Dalam project ini, kita menggunakan dataset dan tabel yang berada di final project kita sebagai source untuk *source table* kita. Berikut merupakan tabel *source tables/preparation layer* kita:
- `production_library_books_source`
- `production_library_members_source`
- `production_library_rent_transaction_source`

Kita akan menggunakan dataset `ihsan_dwh_perpustakaan_source`.

### Fact and Dimensional Tables
Fact dan dimensional table merupakan tabel yang sudah ditransformasi dan dibersihkan. Tabel tersebut seharusnya sudah dalam data type yang sesuai dan tidak memiliki data duplikat (oleh karena itu di buat menjadi incremental table).
Facts table merupakan tabel yang menyimpan data terukur dan memiliki *foreign key* kepada dimensional tables. Tabel ini menyimpan data numerikal yang bisa dianalisis dan diagregasi.
Dimensional table adalah tabel yang menyimpan data yang memiliki atribut deskriptif. Membantu untuk mengkategorisasi, filter, dan *grouping* terhadap *fact tables* untuk kebutuhan analisis.
*Facts & Dimensional Table* kita terdiri dari:
- `dim_genre`
- `dim_books`
- `dim_members`
- `fct_rent_transactions`

Tabel kita akan disimpan didalam dataset `ihsan_dwh_perpustakaan_production`.

### Datamarts
*Datamarts* adalah tabel yang dibentuk untuk kebutuhan analisis tertentu (business group or department) menggunakan data yang didapatkan dari *fact* dan *dimensional tables*.
Datamart kita bernama berikut:
- `mart_rent_transactions`

*Datamarts* kita akan disimpan didalam dataset `ihsan_dwh_perpustakaan_mart`.

### Snapshots
*snapshot* adalah cara untuk *tracking* perubahan data dengan menyimpan historical version data tersebut. Hal ini diimplementasikan dengan **type 2 SCD**, dimana perubahan disimpan dan diinfokan melalui kolom tambahan.
Dengan memisahkan tabel *snapshots* dengan tujuan tracking tersendiri, proses analisis tidak dapat terganggu jika kita ingat melihat version history data kita. 
Untuk memastikan data yang dimasukan kedalam data model kita adalah yang terupdate, kita pastika tabel kita merupakan incremental table dengan menggunakan kolom `updated_at` sebagai panduan.
*Snapshot* kita mengambil dari *source tables* terdiri dari 3 tabel yaitu:
- `snapshots_src_books`
- `snapshots_src_members`
- `snapshots_src_rent_transactions`

*Snapshots* akan disimpan dalam dataset `ihsan_dwh_perpustakaan_snapshots`.
{% enddocs %}