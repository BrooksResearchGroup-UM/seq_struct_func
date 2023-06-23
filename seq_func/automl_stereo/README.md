# AutoML Leaderboard

| Best model   | name                                                       | model_type    | metric_type   |   metric_value |   train_time |   single_prediction_time |
|:-------------|:-----------------------------------------------------------|:--------------|:--------------|---------------:|-------------:|-------------------------:|
|              | [1_Default_Xgboost](1_Default_Xgboost/README.md)           | Xgboost       | logloss       |       0.659115 |       146.16 |                   0.4343 |
|              | [2_Default_CatBoost](2_Default_CatBoost/README.md)         | CatBoost      | logloss       |       0.639624 |        93.61 |                   0.0418 |
|              | [3_Default_RandomForest](3_Default_RandomForest/README.md) | Random Forest | logloss       |       0.63676  |       100.42 |                   0.4934 |
|              | [4_Xgboost](4_Xgboost/README.md)                           | Xgboost       | logloss       |       0.65824  |       142.71 |                   0.4512 |
|              | [8_CatBoost](8_CatBoost/README.md)                         | CatBoost      | logloss       |       0.64949  |        40.08 |                   0.0428 |
|              | [12_RandomForest](12_RandomForest/README.md)               | Random Forest | logloss       |       0.635951 |       109.61 |                   0.5056 |
|              | [5_Xgboost](5_Xgboost/README.md)                           | Xgboost       | logloss       |       0.671265 |       149.33 |                   0.452  |
|              | [9_CatBoost](9_CatBoost/README.md)                         | CatBoost      | logloss       |       0.634913 |        83.31 |                   0.0432 |
|              | [13_RandomForest](13_RandomForest/README.md)               | Random Forest | logloss       |       0.642283 |       123.11 |                   0.5203 |
|              | [6_Xgboost](6_Xgboost/README.md)                           | Xgboost       | logloss       |       0.646651 |       151.05 |                   0.4487 |
|              | [10_CatBoost](10_CatBoost/README.md)                       | CatBoost      | logloss       |       0.647652 |       120.52 |                   0.0429 |
|              | [14_RandomForest](14_RandomForest/README.md)               | Random Forest | logloss       |       0.649951 |       116.09 |                   0.5008 |
|              | [7_Xgboost](7_Xgboost/README.md)                           | Xgboost       | logloss       |       0.666183 |       141.49 |                   0.449  |
|              | [11_CatBoost](11_CatBoost/README.md)                       | CatBoost      | logloss       |       0.630375 |       144.64 |                   0.043  |
|              | [15_RandomForest](15_RandomForest/README.md)               | Random Forest | logloss       |       0.648259 |       136.76 |                   0.5343 |
|              | [16_CatBoost](16_CatBoost/README.md)                       | CatBoost      | logloss       |       0.637018 |       238.65 |                   0.0422 |
|              | [17_CatBoost](17_CatBoost/README.md)                       | CatBoost      | logloss       |       0.631446 |       123.5  |                   0.0432 |
|              | [18_CatBoost](18_CatBoost/README.md)                       | CatBoost      | logloss       |       0.640457 |        93.41 |                   0.043  |
|              | [19_RandomForest](19_RandomForest/README.md)               | Random Forest | logloss       |       0.636181 |       134.06 |                   0.5235 |
|              | [20_RandomForest](20_RandomForest/README.md)               | Random Forest | logloss       |       0.636615 |       126.81 |                   0.5047 |
|              | [21_Xgboost](21_Xgboost/README.md)                         | Xgboost       | logloss       |       0.646651 |       162.77 |                   0.4512 |
|              | [22_Xgboost](22_Xgboost/README.md)                         | Xgboost       | logloss       |       0.646651 |       166.19 |                   0.4367 |
|              | [23_Xgboost](23_Xgboost/README.md)                         | Xgboost       | logloss       |       0.656264 |       168.61 |                   0.4373 |
|              | [24_Xgboost](24_Xgboost/README.md)                         | Xgboost       | logloss       |       0.66105  |       171.71 |                   0.4526 |
|              | [25_CatBoost](25_CatBoost/README.md)                       | CatBoost      | logloss       |       0.627906 |       163.93 |                   0.0428 |
|              | [26_CatBoost](26_CatBoost/README.md)                       | CatBoost      | logloss       |       0.628381 |       185.96 |                   0.0434 |
| **the best** | [Ensemble](Ensemble/README.md)                             | Ensemble      | logloss       |       0.621013 |         1.38 |                   0.2106 |

### AutoML Performance
![AutoML Performance](ldb_performance.png)

### AutoML Performance Boxplot
![AutoML Performance Boxplot](ldb_performance_boxplot.png)

### Features Importance
![features importance across models](features_heatmap.png)



### Spearman Correlation of Models
![models spearman correlation](correlation_heatmap.png)

