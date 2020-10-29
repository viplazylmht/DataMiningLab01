# DataMining Lab 01 - Preprocessing

# Hou to use

Note: Feel free to pass `-h` option to show help each command.

1. List column that missing data

    ```bash
    python3 list_missing.py test/house-prices.csv --extra
    ```

2. Count column that missing data

    ```bash
    python3 count_missing.py test/house-prices.csv
    ``` 

3. Impute
   ```bash
    python3 impute.py test/house-prices.csv --method mode
    ```

 4. Remove rows that have missing rate greater than a constant
    ```bash
    python3 remove_missing.py test/house-prices.csv 50
    ```

5. Remove cols that have missing rate greater than a constant
    ```bash
    python3 remove_missing.py test/house-prices.csv 50 --column
    ```
6. Remove duplicate rows
    ```bash
    python3 remove_dup.py test/house-prices.csv
    ```

7. Feature Scaling dataset
    ```bash
    python3 feature_scaling.py test/house-prices.csv --column PoolArea YrSold
    ```

    ```bash
    python3 feature_scaling.py test/house-prices.csv --column PoolArea YrSold --method zscore
    ```

8. Clustering





