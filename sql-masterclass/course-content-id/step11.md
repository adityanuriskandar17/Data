<p align="center">
    <img src="./../images/sql-masterclas-banner.png" alt="sql-masterclass-banner">
</p>

[![forthebadge](./../images/badges/version-1.0.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/ctrl-c-ctrl-v.svg)]()

# Langkah 11 - Strategi Trader

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step10.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step12.md)

# Skenario 3: Trader

![trader](assets/trader.jpeg)

Nandita adalah Ratu trading kripto - ia ingin mengikuti pepatah trader populer yaitu **BELI MURAH, JUAL MAHAL**

## Riwayat Transaksi Nandita

* Ia juga memulai dengan pembelian 50 BTC dan ETH seperti Leah dan Vikram
* Ia terus membeli lebih banyak kripto selama 4 tahun
* Ia mulai menjual sebagian portofolio kriptonya untuk merealisasikan keuntungan

## Data Nandita

Skenario 3 yang terakhir ini sebenarnya persis sama dengan dataset `trading.transactions` asli kita!

Untuk menyelesaikan skenario individu kita sebelum menghitung semua metrik untuk semua mentor - mari kita siapkan temp table lain bernama `nandita_trading_strategy`

```sql
CREATE TEMP TABLE nandita_trading_strategy AS
SELECT * FROM trading.transactions
WHERE member_id = 'a87ff6';
```

Anda dapat memeriksa data dengan menjalankan query berikut setelah membuat temp table di atas:

```sql
SELECT * FROM nandita_trading_strategy LIMIT 10;
```

| txn_id | member_id | ticker |  txn_date  | txn_type |     quantity     | percentage_fee |          txn_time          |
| ------ | --------- | ------ | ---------- | -------- | ---------------- | -------------- | -------------------------- |
|      3 | a87ff6    | BTC    | 2017-01-01 | BUY      |               50 |           0.00 | 2017-01-01 00:00:00        |
|     19 | a87ff6    | ETH    | 2017-01-01 | BUY      |               50 |           0.20 | 2017-01-01 00:00:00        |
|     41 | a87ff6    | ETH    | 2017-01-01 | BUY      | 1.98666102006509 |           0.30 | 2017-01-01 17:39:10.894181 |
|     49 | a87ff6    | ETH    | 2017-01-02 | BUY      | 8.78673520720906 |           0.30 | 2017-01-02 04:48:50.044665 |
|     53 | a87ff6    | BTC    | 2017-01-02 | BUY      | 5.95980481918755 |           0.30 | 2017-01-02 09:55:27.347188 |
|     60 | a87ff6    | BTC    | 2017-01-02 | BUY      | 9.01117722642621 |           0.30 | 2017-01-02 17:16:29.062839 |
|     64 | a87ff6    | ETH    | 2017-01-02 | BUY      | 1.37715908309016 |           0.01 | 2017-01-02 20:49:33.771818 |
|     77 | a87ff6    | BTC    | 2017-01-03 | BUY      | 3.80769453794553 |           0.30 | 2017-01-03 12:30:20.779105 |
|     89 | a87ff6    | BTC    | 2017-01-04 | BUY      | 5.68677206948404 |           0.00 | 2017-01-04 08:13:07.752195 |
|     93 | a87ff6    | BTC    | 2017-01-04 | BUY      | 8.13772499730359 |           0.30 | 2017-01-04 12:25:48.367139 |
<br>

## Metrik Evaluasi Akhir

Pada akhir periode penilaian kami pada 29 Agustus 2021 - kita dapat menghitung metrik Nandita sebagai berikut untuk setiap portofolio BTC dan ETH:

* Jumlah transaksi beli dan jual
* Total jumlah investasi pembelian
* Jumlah dolar biaya untuk transaksi pembelian
* Rata-rata biaya dolar pembelian
* Total pendapatan kotor dari transaksi penjualan
* Rata-rata harga jual untuk setiap unit yang terjual
* Nilai dan jumlah portofolio akhir
* Profitabilitas diukur sebagai (nilai portofolio akhir + pendapatan penjualan kotor - biaya pembelian - biaya penjualan) / jumlah investasi awal

**Pertanyaan Bonus**

Kami juga ingin menghitung perbedaan jika Nandita tidak menjual kriptonya sama sekali dan membandingkannya dengan nilai akhir pada akhir Agustus - seberapa besar dampaknya terhadap profitabilitas keseluruhannya?

## Solusi

### Pertanyaan 1

> Hitung metrik pembelian Nandita untuk setiap portofolio BTC dan ETH:
>
> * Jumlah transaksi pembelian
> * Investasi awal
> * Biaya pembelian
> * Rata-rata biaya dolar pembelian

<details><summary>Klik di sini untuk melihat solusi!</summary><br>

```sql
WITH cte_purchases AS (
  SELECT
    transactions.ticker,
    COUNT(*) AS purchase_count,
    SUM(transactions.quantity) AS purchase_quantity,
    SUM(transactions.quantity * prices.price) AS initial_investment,
    SUM(transactions.quantity * prices.price * transactions.percentage_fee / 100) AS purchase_fees
  FROM nandita_trading_strategy AS transactions
  INNER JOIN trading.prices
    ON transactions.ticker = prices.ticker
    AND transactions.txn_date = prices.market_date
  WHERE transactions.txn_type = 'BUY'
  GROUP BY transactions.ticker
)
SELECT
  ticker,
  purchase_count,
  purchase_quantity,
  initial_investment,
  purchase_fees,
  initial_investment / purchase_quantity AS dollar_cost_average
FROM cte_purchases;
```

</details><br>

| ticker | purchase_count |    purchase_quantity    |      initial_investment      |        purchase_fees         |    dollar_cost_average    |
| ------ | -------------- | ----------------------- | ---------------------------- | ---------------------------- | ------------------------- |
| BTC    |            954 | 5023.705687783492459935 | 63735345.6973630892576024850 | 162919.943377863222128081502 | 12686.9187126851255182628 |
| ETH    |            756 |   3822.0371970017654265 |   2287096.578215583047801140 |    5783.32678170688531189239 |    598.397257883758534604 |
<br>

### Pertanyaan 2

> Hitung metrik penjualan Nandita untuk setiap portofolio BTC dan ETH:
>
> * Jumlah transaksi penjualan
> * Jumlah pendapatan kotor
> * Biaya penjualan
> * Rata-rata harga jual

<details><summary>Klik di sini untuk melihat solusi!</summary><br>

```sql
WITH cte_sales AS (
  SELECT
    transactions.ticker,
    COUNT(*) AS sales_count,
    SUM(transactions.quantity) AS sales_quantity,
    SUM(transactions.quantity * prices.price) AS gross_revenue,
    SUM(transactions.quantity * prices.price * transactions.percentage_fee / 100) AS sales_fees
  FROM nandita_trading_strategy AS transactions
  INNER JOIN trading.prices
    ON transactions.ticker = prices.ticker
    AND transactions.txn_date = prices.market_date
  WHERE transactions.txn_type = 'SELL'
  GROUP BY transactions.ticker
)
SELECT
  ticker,
  sales_count,
  sales_quantity,
  gross_revenue,
  sales_fees,
  gross_revenue / sales_quantity AS average_selling_price
FROM cte_sales;
```

</details><br>

| ticker | sales_count |    sales_quantity    |       gross_revenue        |         sales_fees         |  average_selling_price  |
| ------ | ----------- | -------------------- | -------------------------- | -------------------------- | ----------------------- |
| BTC    |         167 | 863.4858182768507102 | 10975745.05336688201117242 | 29522.09286188312984442411 | 12710.97315213559195557 |
| ETH    |          70 | 318.1506358514526923 |  172591.915512909206341725 |   447.93810830446683009024 |  542.484898862480594053 |
<br>

### Pertanyaan 3

> Berapa nilai dan jumlah portofolio akhir BTC dan ETH Nandita?

<details><summary>Klik di sini untuk melihat solusi!</summary><br>

```sql
WITH cte_adjusted_transactions AS (
  SELECT
    member_id,
    txn_date,
    txn_type,
    ticker,
    percentage_fee,
    CASE
      WHEN txn_type = 'BUY' THEN quantity
      WHEN txn_type = 'SELL' THEN -quantity
    END as quantity
  FROM nandita_trading_strategy
)
SELECT
  transactions.ticker,
  SUM(transactions.quantity) AS final_quantity,
  SUM(transactions.quantity * prices.price) AS final_portfolio_value
FROM cte_adjusted_transactions AS transactions
INNER JOIN trading.prices
  ON transactions.ticker = prices.ticker
WHERE prices.market_date = '2021-08-29'
GROUP BY transactions.ticker;
```

</details><br>

| ticker |     final_quantity      |     final_portfolio_value     |
| ------ | ----------------------- | ----------------------------- |
| BTC    | 4160.219869506641749735 | 200751409.8030429976334624250 |
| ETH    |   3503.8865611503127342 |   11134790.869485909819250128 |
<br>

### Pertanyaan 4 & 5 (bonus!)

> Berapa profitabilitas keseluruhan Nandita dan profitabilitas teoretis jika ia tidak menjual portofolionya?

Kami akan mencoba meminimalkan berapa kali kita mengakses temp table `nandita_trading_strategy` untuk mengoptimalkan kinerja query!

<details><summary>Klik di sini untuk melihat solusi!</summary><br>

```sql
WITH cte_portfolio AS (
  SELECT
    transactions.ticker,
    transactions.txn_type,
    COUNT(*) AS transaction_count,
    SUM(transactions.quantity) AS total_quantity,
    SUM(transactions.quantity * prices.price) AS gross_values,
    SUM(transactions.quantity * prices.price * transactions.percentage_fee / 100) AS fees 
  FROM nandita_trading_strategy AS transactions
  INNER JOIN trading.prices
    ON transactions.ticker = prices.ticker
    AND transactions.txn_date = prices.market_date
  GROUP BY 1,2
),
cte_summary AS (
  SELECT
    ticker,
    SUM(
      CASE
        WHEN txn_type = 'BUY' THEN total_quantity
        WHEN txn_type = 'SELL' THEN -total_quantity
      END
    ) AS final_quantity,
    SUM(CASE WHEN txn_type = 'BUY' THEN gross_values ELSE 0 END) AS initial_investment,
    SUM(CASE WHEN txn_type = 'SELL' THEN gross_values ELSE 0 END) AS sales_revenue,
    SUM(CASE WHEN txn_type = 'BUY' THEN fees ELSE 0 END) AS purchase_fees,
    SUM(CASE WHEN txn_type = 'SELL' THEN fees ELSE 0 END) AS sales_fees,
    SUM(CASE WHEN txn_type = 'BUY' THEN total_quantity ELSE 0 END) AS purchase_quantity,
    SUM(CASE WHEN txn_type = 'SELL' THEN total_quantity ELSE 0 END) AS sales_quantity,
    SUM(CASE WHEN txn_type = 'BUY' THEN transaction_count ELSE 0 END) AS purchase_transactions,
    SUM(CASE WHEN txn_type = 'SELL' THEN transaction_count ELSE 0 END) AS sales_transactions
  FROM cte_portfolio
  GROUP BY ticker
),
cte_metrics AS (
  SELECT
    summary.ticker,
    summary.final_quantity * final.price AS actual_final_value,
    summary.purchase_quantity * final.price AS theoretical_final_value,
    summary.sales_revenue,
    summary.purchase_fees,
    summary.sales_fees,
    summary.initial_investment,
    summary.purchase_quantity,
    summary.sales_quantity,
    summary.purchase_transactions,
    summary.sales_transactions,
    summary.initial_investment / purchase_quantity AS dollar_cost_average,
    summary.sales_revenue / sales_quantity AS average_selling_price
  FROM cte_summary AS summary
  INNER JOIN trading.prices AS final
    ON summary.ticker = final.ticker
  WHERE final.market_date = '2021-08-29'
)
SELECT
  ticker,
  actual_final_value AS final_portfolio_value,
  ( actual_final_value + sales_revenue - purchase_fees - sales_fees ) / initial_investment AS actual_profitability,
  ( theoretical_final_value - purchase_fees ) / initial_investment AS theoretical_profitability,
  dollar_cost_average,
  average_selling_price,
  sales_revenue,
  purchase_fees,
  sales_fees,
  initial_investment,
  purchase_quantity,
  sales_quantity,
  purchase_transactions,
  sales_transactions
FROM cte_metrics;
```

</details><br>

| ticker |     final_portfolio_value     |  actual_profitability   | theoretical_profitability |    dollar_cost_average    |  average_selling_price  |       sales_revenue        |        purchase_fees         |         sales_fees         |      initial_investment      |    purchase_quantity    |    sales_quantity    | purchase_transactions | sales_transactions |
| ------ | ----------------------------- | ----------------------- | ------------------------- | ------------------------- | ----------------------- | -------------------------- | ---------------------------- | -------------------------- | ---------------------------- | ----------------------- | -------------------- | --------------------- | ------------------ |
| BTC    | 200751409.8030429976334624250 | 3.318954506414827841503 |   3.800967820444996477195 | 12686.9187126851255182628 | 12710.97315213559195557 | 10975745.05336688201117242 | 162919.943377863222128081502 | 29522.09286188312984442411 | 63735345.6973630892576024850 | 5023.705687783492459935 | 863.4858182768507102 |                   954 |                167 |
| ETH    |   11134790.869485909819250128 |  4.94126554503705553061 |    5.30805715638391209991 |    598.397257883758534604 |  542.484898862480594053 |  172591.915512909206341725 |    5783.32678170688531189239 |   447.93810830446683009024 |   2287096.578215583047801140 |   3822.0371970017654265 | 318.1506358514526923 |                   756 |                 70 |
<br>

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step10.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step12.md)
