# Final Project Data Engineering Bootcamp Purwadhika

Repository ini adalah hasil kerja saya untuk tugas Capstone Project ke-3 Kelas Data Engineering Purwadhika. Secara garis besar saya diminta untuk membuat data pipeline yang mengutilisasi Airflow sebagai *orchestrator* terhadap dua DAG (Directed Acyclic Graph). Kedua DAG tersebut bertujuan untuk:

Project ini bertujuan untuk kebutuhan Final Project untuk kelas Data Engineering Purwadhika Digital School. Untuk menyelesaikan final project ini, kita diminta untuk melanjutkan capstone project 3 kita untuk men-develop Airflow Dags on-failure alert ke dalam discord, melakukan webscraping & memasukkannya ke dalam bigquery, dan terakhir mendevelop dbt untuk transformasi data lalu mengimplementasinya kedalam airflow. Project ini bersikan 4 DAG yait:

1. Generasi *dummy data* dan menyimpannya dalam suatu database (PostgreSQL)
2. melakukan ingestion data tersebut dari database ke Google BigQuery.
3. Menjalankan dbt untuk transformasi data didalam BigQuery memindahkannya ke masing-masing dataset. **[Final Project]**
4. Melakukan webscraping kepada website asetku.com dan menyimpannya didalam BigQuery. **[Final Project]**

Seluruh DAGs diatas juga menggunakan fungsi yang mengirimkan detail error ke discord jika DAG yang dijalankan gagal. **[Final Project]**

Graph dibawah dapat dilihat sebagai gambaran umum project dari ini.

<img src='assets/project_graph.png' alt='project graph' width='50%'>

## Overview

Dalam project, kita diminta membuat seleruh DAG terhadap dalam suatu studi kasus. Studi kasus yang saya pilih adalah sistem data pipeline untuk suatu perpustakaan yang menyimpan data Buku (Books), anggota (Member), dan sewa (Rent). 

Penggunaan airflow adalah untuk orkestrasi *task* dalam suatu satuan waktu yang dapat di otomatisasi. Dalam kasus ini, kita akan mengambil data dari database perpustakaan (yang kita akan generate dummy data seakan database operasional) dan memasukkannya kedalam BigQuery. *Task* tersebut kita akan desain untuk berjalan setiap jam pada menit 15, membantu menghilangkan perlunya laporan manual dari tim operasi dan data didapatkan secara cepat tanpa perlu menunggu anggota tim lain.

Google BigQuery merupakan suatu Data Warehouse, tempat dimana data disimpan untuk kebutuhan analisis. Pemisahan penyimpanan data antara operasional dan analisis ini akan berguna agar proses analisis tidak bisa menganggu proses operasional yang berjalan sangat dinamis. BigQuery juga dioptimisasi untuk kebutuhan analisis dari bagaimana service tersebut melakukan Storage dan Pricing agar lebih cost and time efficient.

dbt adalah suatu tool yang digunakan untuk transfomasi data yang biasanya sudah berada didalam data warehouse, atau lebih sering disebut dengan ELT process berperan sebagai 'T' dalam proses tersebut. Tools ini menggunakan file SQL sebagai dasar untuk proses transformasi dan bisa menggunakan Jinja, suatu *templating language*, untuk membuat kueri SQL menjadi dinamis dan modular. dbt seringkali digunakan oleh para *Analytics Engineer* untuk menyediakan data yang siap digunakan oleh end-users.

Project ini, pada tahapan pertama akan menggenerasi *dummy* data yang lalu akan di ingest ke BigQuery. Setelah itu, menggunakan dbt untuk transformasi data tersebut didalam BigQuery agar lebih siap digunakan. Proses Data Modelling terdapat 3 tahap yaitu membuat (1) source tables, (2) Fact and Dimensional tables, dan (3) Data Marts yang bertujuan untuk memenuhi kebutuhan reporting/analisis tertentu.

kita juga melakukan webscrapping yang dijalankan oleh DAG menggunakan dua tools yaitu BeautifulSoup untuk parsing HTML dan selenium untuk berinteraksi dengan halaman web dengan menggunakan WebDriver. Webscraping adalah suatu teknik dimana kita mengambil informasi melalui halaman web tertentu.

### Tools

- Docker
- Airflow
- PostgreSQL
- Pandas
- Google BigQuery
- dbt
- BeautifulSoup
- Selenium


## Cara Menggunakan

Untuk menjalankan project ini, kita menggunakan docker. Dalam project ini, kita menggunakan 5 services yaitu 2 PostgreSQL database yaitu `application_db` dan `airflow_db`. `application_db` untuk menyimpan secara lokal geneasi data kita dan `airflow_db` untuk menyimpan metadata Airflow. Lalu kita menggunakan 3 services Airflow yaitu, `init_airflow` untuk meng*intialize* airflow, `webserver` yang menghost webUI airflow untuk kita berinteraksi dengan airflow, dan `scheduler` yang menjalankan orkestrasi yang telah didesain.

Sebelum menjalankan kita juga harus memastikan bahwa port local yang kita gunakan 5432 sedang tidak dipakai. Jika masih dipakai maka service app_db tidak akan berjalan. Jika memang port 5432 tidak bisa dimatikan kita bisa mengubahnya menjadi local port lain, namun jangan diubah untuk container portnya (e.g. 5433:5432, port kedua jangan diubah) karena tetap bisa berjalan dan sudah sesuai dengan DAG script.

Satu hal yang diperhatikan adalah penggunaan docker network. Docker network dibentuk dalam file docker-compose bersama `airflow_db` Dengan menggunakan network, hal tersebut memudahkan komunikasi antar container. Kita hanya perlu menggunakan nama service sebagai *host* dan menggunakan container port yang kita tuliskan didalam file `docker-compose.yaml`. Hal ini juga meningkatkan security, karena seluruh komunikasi antar service dilakukan dalam suatu internal network, hal ini membantu kita untuk mengawasi dan mengatur external access dengan lebih mudah.

Namun, karena docker network tersebut dibuat dalam file docker compose untuk `airflow_db`, maka kita harus menjalankan docker compose tersebut terlebih dahulu agar network dipersiapkan sebelum digunakan container lain. Hal itu dapat dilakukan dengan menjalankan command dibawah di directory project ini.

```
docker compose -f prod_airflow_db/docker-compose.yaml up -d
docker compose -f prod_airflow_service/docker-compose.yaml up -d
docker compose -f app_db/docker-compose.yaml up -d
docker compose -f dbt/docker-compose.yaml up -d
```

Setelah itu kita bisa membuka webserver airflow di browser dengan membuka `localhost:8080`. Ketika membuka UI kita akan diminta user and password yang bisa kita isi dengan info dibawah:

user: airflow
password: airflow

Di dalam web UI tersebut, karena project kita didesain untuk dijalankan setiap satu jam, kita hanya perlu mengeser tombol yang berada disebelah DAG kita.

<img src='assets/dag_button.png' alt='database design' width='35%'>

jika ingin memberhentikan service kita berikan command:

```
docker compose -f prod_airflow_service/docker-compose.yaml down
docker compose -f app_db/docker-compose.yaml down
docker compose -f dbt/docker-compose.yaml down
docker compose -f prod_airflow_db/docker-compose.yaml down
```

## DAGs (Directed Acyclic Graphs)

### (1) Create data and insert to PostgreSQL

Dalam DAG pertama kita, kita diminta untuk generate database dengan schema seperti:

<img src='assets/database_design.png' alt='database design' width='50%'>

Masing-masing tabel memiliki *primary key* masing-masing yang menjadi *foreign key* didalam table *rent_table*. *primary key* juga berurutan, memudahkan kita untuk menggunakan *primary key* terakhir untuk menggenerasi *primary key* selanjutnya.

<img src='assets/generate_data_dag.png' alt='generate_data_dag' width='90%'>

#### Get ID list
Dari gambar diatas, kita dapat melihat bahwa sebelum kita generate data, kita akan mengambil id list dari masing-masing tabel di PostgreSQL (akan menjadi 0 pada generate pertama), hal ini dilakukan untuk memastikan meng-generate id baru.

#### Generate Data
Cara untuk menggenerate data tersebut adalah dengan menggunakan API random name generator untuk nama member dan OpenLibrary untuk Judul Buku.

Lalu setelah itu kita menjalankan secara bersamaan generate data pada tabel `books_table` dan `library_member`. Hal ini dilakukan terlebih dahulu, karena untuk generate data pada `rent_data` kita akan mengambil id dari dua tabel sebelumnya dan dipilih secara random.

#### Insert to PostgreSQL
setelah semua data di generate, kita akan masing-masing insert datanya kedalam PostgreSQL dengan menggunakan *library* psycopg2 melalui helper file `postgres_app_helper`.

### (2) PostgreSQL to BigQuery

Dalam DAG ini, kita diminta untuk melakukan ingestion dari data yang telah kita generate sebelumnya ke Google BigQuery.

<img src='assets/postgres_to_bigquery_dag.png' alt='postgres_to_bigquery_dag' width='80%'>

Proses dari DAG ini didahulukan dengan menggunakan task `check_dataset` yang akan mememeriksa apakah dataset sudah tersedia pada BigQuery target. Tergantung hasil return dari *check_dataset*, jika `True` maka `create_dataset` task akan menjalankan pembuatan dataset. Bila hasil return `False` , maka task `create_dataset` akan di skip sebagaimana graph diatas.

#### Trigger Rule

Karena task sebelumnya di skip, kita harus memastikan `trigger_rule` untuk task selanjutnya. Karena secara *default* `trigger_rule` yang digunakan adalah `all_success`, yang memastikan bahwa task sebelumnya harus berhasil berjalan. Kita akan mengubah value `trigger_rule` dalam task selanjutanya menjadi `none_failed`, karena dalam kasus ini task sebelumnya di skip namun tidak *failed*.

#### YAML file for dynamic DAGs

Dalam membuat DAG ini, kita menggunakan yaml file sebagai configuration file yang menyimpan detail informasi tabel kita. Penggunaan file yaml membantu karena ini dapat digunakan untuk *dynamic dag*, menggunakan template untuk beberapa table yang berada di configuration file.

Seperti yang kita lihat diatas setiap table diproses dengan template task yang sama. (1) kita melakukan ingestion dari PostgreSQL dengan library pandas dan menyimpannya sebagai csv dalam temporary storage kita, (2) kita melakukan load staging table dengan menggunakan Google Cloud Python API secara incremental, dan (3) kita melakukan upsert ke final table kita secara incremental.

#### Upsert Table

Penggunaan staging table dengan final/production table membantu untuk memastikan bahwa final table sudah siap digunakan dan segala pemrosesan yang belum selesai dilakukan di staging table.

### (3) DAG Failed Alert (Final Project Update)

*contoh gambar failure messsage di discord*

Disini kita membuat fungsi untuk memberikan suatu pesan menuju Discord Server kita apabila suatu DAG menghadapi suatu failure. Untuk mengirimkan pesan melalui discord, kita pertama harus membuat webhook untuk di discord sebagai 'akun' yang akan mengirimkan pesan.

Setelah membuat webhook, kita mengambil urlnya dan menggunakan library `requests` dan method `post` untuk mengirimkan pesan.

Fungsi yang dibuat akan mengambil informasi dari context (*failure* di DAG) lalu mengambil nama, task, dan exception (Error message) dari task dan DAG yang *failed*.

*kegunaan business case*

### (4) Web Scrapping for Asetku Website (Final Project Update)

Untuk melakukan webscraping, kita menggunakan kedua BeautifulSoup untuk parsing html dari halaman yang kita tari dan Selenium untuk menggunakan Webdriver browser kita agar berperan seakan data yang diambil melalui browser.

Kita harus mengambil data menggunakan Selenium karena halaman yang kita ambil menggunakan Javascript untuk menyediakan datanya secara dinamis melainkan menuliskannya di html polos. 

Pertama kita load halaman menggunakan `webdriver.Chrome` dari library `selenium. Lalu kita parsing html `page_source` dari halaman yang kita ambil menggunakan BeautifulSoup. Kita akan ambil seluruh `div` tag dengan class `name` dan `amount` didalam `div` tag yang berada didalam class `content-row-1`. Berikut dibawah gambar yang kita akan ambil datanya melalui webscrapping melalui website [asetku](https://www.asetku.co.id/).

*gambar asetku disini*

### (5) dbt-Airflow Implementation (Final Project Update)

#### What is dbt?

dbt adalaj suatu tool yang digunakan untuk transformasi data yang bisa digunakan didalam proses ELT, dimana data di*load* terlebih dahulu sebelum di transformasi. 

dbt menggunakan kueri sql sebagai template model dan Jinja yang bisa membantu kueri bisa digunakan kembali dan menjadi dinamis.

#### Source Tables

*Source tables* merupakan tabel yang biasa diambil dari luar sistem kita kedalam data warehouse yang dipilih. Tabel ini biasanya tidak di transform terlebih dahulu, menyediakan data sebagai *raw* untuk ditransformasi di tabel yang lain. 

Dalam project ini, kita menggunakan dataset dan tabel yang berada di final project kita sebagai source untuk *source table* kita. Karena *source table* merupakan raw, kita akan membiarkan adanya duplikasi didalam tabel tersebut, tanpa dibuat menjadi *incremental table*. Hal ini dilakukan untuk memastikan tidak ada data yang hilang dan karena tidak digunakan untuk end user, hal ini tidak akan menganggu proses analisis.

#### Fact and Dimensional Tables

Fact dan dimensional table merupakan tabel yang sudah ditransformasi dan dibersihkan. Tabel tersebut seharusnya sudah dalam data type yang sesuai dan tidak memiliki data duplikat (oleh karena itu di buat menjadi incremental table).

Facts table merupakan tabel yang menyimpan data terukur dan memiliki *foreign key* kepada dimensional tables. Tabel ini menyimpan data numerikal yang bisa dianalisis dan diagregasi.

Dimensional table adalah tabel yang menyimpan data yang memiliki atribut deskriptif. Membantu untuk mengkategorisasi, filter, dan *grouping* terhadap *fact tables* untuk kebutuhan analisis.

#### Datamarts

*Datamarts* adalah tabel yang dibentuk untuk kebutuhan analisis tertentu (business group or department) menggunakan data yang didapatkan dari *fact* dan *dimensional tables*.

#### Airflow-dbt Implementation

*gambar dag airflow-dbt*

Dalam project ini, untuk menggunakan dbt dalam airflow, kita menggunakan docker compose yang berada directory berbeda dengan Airflow. Kita membentuk docker-compose dengan menggunakan Dockerfile custom untuk instalasi `dbt-core` dan `dbt-bigquery`. Kita juga harus meletakan folder project untuk dbt dalam directory yang sama.

`library_dbt` sebagai directory yang menyimpan project dbt kita, `profiles` sebagai directory yang menyimpan profile dbt kita, dan `logs` untuk menyimpan file logging untuk proses dbt. Kita juga membuat folder `keys` yang menyimpan file service-account.json untuk koneksi dengan BigQUery. 

Setelah kita sukses instalasi dbt dengan docker, kita lalu bisa mengkoneksikan airflow dengannya. Hal ini kita lakukan dengan cara memastikan airflow memiliki akses terhadap docker kita. Hal ini dilakukan dengan cara mounting docker.sock kita ke dalam volume (isi di volume docker compose: `/var/run/docker.sock:/var/run/docker.sock`).

Jika sudah terkoneksi kita bisa langsung menggunakan *BashOperator* untuk memberikan command kepada service dbt kita. Setiap task untuk dag ini menggunakan template berikut:

```
docker exec dbt-dbt-1 dbt run --select {model} --target {target dataset} --profiles-dir {directory profile dbt} --project-dir {director project dbt}
```

Dengan menggunakan file `app_db.yml` sebagai config, kita bisa membuat commandnya secara dinamis. Ketika membuat model baru, kita tidak memerlukan untuk merubah commandnya, hanya perlu menambahkan ke dalam file config kita.

Setelah itu kita akan buat 4 task dalam dag ini untuk masing jenis tabel (`dbt_run_src`,`dbt_run_dim`,`dbt_run_fact`, `dbt_run_mart`) dengan setiap task menjalankan BashOperator untuk command masing-masing.
