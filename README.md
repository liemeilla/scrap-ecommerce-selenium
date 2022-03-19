# Scrap E-Commerce using Selenium

## Perequisite
- Required packages are writted inside `requirement.txt`
- This project uses python version `3.6.8`

## E-Commerce Website
E-Commerce website used tokopedia website which use 2 parameter, `url` and `topic`. The url is used for accessing tokopedia website and topic is the keyword to search certain product

## How to run

Parameters `url` and `topic` are define inside `app.py`. Run scrapping process by executing this command,
```
python3 app.py
```

## Scrapping Results
Product fields:
```
- product_sequence -> product sequence number
- product_name -> product name or title
- product_category -> product category
- product_price -> product price in thousand rupiah
- product_location -> location of product is being sell
- product_total_sold -> total sold product
```
The mandatory fields are product name, product price and product category. The additional information which are product_location and product_total_sold. Product location and total product sold are useful to identify how many product are sold in particular area.

Scrapping process produce 2 files which are csv files and json files. 
The format for each files are:
```
<ecommerce>_<topic>_<datetime>.csv
<ecommerce>_<topic>_<datetime>.json
```
### CSV Files
This is the example of csv files which has topic "atasan wanita"
| product_sequence  | product_name  | product_category  | product_price | product_location  | product_total_sold|
| ----------------- | -----------   | ----------------- | -----------   | ----------------- | -----------       |
|1|"Terry & Co Original Top /. Atasan Wanita Ke kinian / Blouse Wanita - Putih, S-M"|Fashion Wanita|Rp220.000|Jakarta Barat|2|
|2|blouse wanita|Fashion Wanita|Rp49.500|Kab. Bekasi|3|
|...|...|...|...|...|...|

### JSON Files
This is the example of json files which has topic "atasan wanita"
```
[
    {
        "product_sequence": 1,
        "product_name": "Terry & Co Original Top /. Atasan Wanita Ke kinian / Blouse Wanita - Putih, S-M",
        "product_category": "Fashion Wanita",
        "product_price": "Rp220.000",
        "product_location": "Jakarta Barat",
        "product_total_sold": 2
    },
    {
        "product_sequence": 2,
        "product_name": "blouse wanita",
        "product_category": "Fashion Wanita",
        "product_price": "Rp49.500",
        "product_location": "Kab. Bekasi",
        "product_total_sold": 3
    },
    ...
]
```

