# Summary of Ensemble

[<< Go back](../README.md)


## Ensemble structure
| Model       |   Weight |
|:------------|---------:|
| 11_CatBoost |        2 |
| 17_CatBoost |        2 |
| 25_CatBoost |        4 |
| 26_CatBoost |        3 |
| 9_CatBoost  |        3 |

### Metric details
|           |         -1 |           0 |          1 |   accuracy |   macro avg |   weighted avg |   logloss |
|:----------|-----------:|------------:|-----------:|-----------:|------------:|---------------:|----------:|
| precision |   0.819549 |   0.5       |   0.63986  |   0.753012 |    0.653136 |       0.719777 |  0.621013 |
| recall    |   0.917895 |   0.0441176 |   0.835616 |   0.753012 |    0.59921  |       0.753012 |  0.621013 |
| f1-score  |   0.865938 |   0.0810811 |   0.724752 |   0.753012 |    0.557257 |       0.700083 |  0.621013 |
| support   | 475        | 136         | 219        |   0.753012 |  830        |     830        |  0.621013 |


## Confusion matrix
|               |   Predicted as -1 |   Predicted as 0 |   Predicted as 1 |
|:--------------|------------------:|-----------------:|-----------------:|
| Labeled as -1 |               436 |                3 |               36 |
| Labeled as 0  |                63 |                6 |               67 |
| Labeled as 1  |                33 |                3 |              183 |

## Learning curves
![Learning curves](learning_curves.png)
## Confusion Matrix

![Confusion Matrix](confusion_matrix.png)


## Normalized Confusion Matrix

![Normalized Confusion Matrix](confusion_matrix_normalized.png)


## ROC Curve

![ROC Curve](roc_curve.png)


## Precision Recall Curve

![Precision Recall Curve](precision_recall_curve.png)



[<< Go back](../README.md)
