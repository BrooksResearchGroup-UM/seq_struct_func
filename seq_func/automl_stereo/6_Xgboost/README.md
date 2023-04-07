# Summary of 6_Xgboost

[<< Go back](../README.md)


## Extreme Gradient Boosting (Xgboost)
- **n_jobs**: -1
- **objective**: multi:softprob
- **eta**: 0.1
- **max_depth**: 7
- **min_child_weight**: 25
- **subsample**: 0.9
- **colsample_bytree**: 0.6
- **eval_metric**: mlogloss
- **num_class**: 3
- **explain_level**: 2

## Validation
 - **validation_type**: kfold
 - **k_folds**: 5
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

165.3 seconds

### Metric details
|           |         -1 |          0 |          1 |   accuracy |   macro avg |   weighted avg |   logloss |
|:----------|-----------:|-----------:|-----------:|-----------:|------------:|---------------:|----------:|
| precision |   0.831418 |   0.318182 |   0.651515 |   0.746988 |    0.600372 |       0.699853 |  0.647285 |
| recall    |   0.913684 |   0.102941 |   0.785388 |   0.746988 |    0.600671 |       0.746988 |  0.647285 |
| f1-score  |   0.870612 |   0.155556 |   0.712215 |   0.746988 |    0.579461 |       0.711652 |  0.647285 |
| support   | 475        | 136        | 219        |   0.746988 |  830        |     830        |  0.647285 |


## Confusion matrix
|               |   Predicted as -1 |   Predicted as 0 |   Predicted as 1 |
|:--------------|------------------:|-----------------:|-----------------:|
| Labeled as -1 |               434 |                9 |               32 |
| Labeled as 0  |                62 |               14 |               60 |
| Labeled as 1  |                26 |               21 |              172 |

## Learning curves
![Learning curves](learning_curves.png)

## Permutation-based Importance
![Permutation-based Importance](permutation_importance.png)
## Confusion Matrix

![Confusion Matrix](confusion_matrix.png)


## Normalized Confusion Matrix

![Normalized Confusion Matrix](confusion_matrix_normalized.png)


## ROC Curve

![ROC Curve](roc_curve.png)


## Precision Recall Curve

![Precision Recall Curve](precision_recall_curve.png)



## SHAP Importance
![SHAP Importance](shap_importance.png)

## SHAP Dependence plots

### Dependence -1 (Fold 1)
![SHAP Dependence from fold 1](learner_fold_0_shap_dependence_class_-1.png)
### Dependence 0 (Fold 1)
![SHAP Dependence from fold 1](learner_fold_0_shap_dependence_class_0.png)
### Dependence 1 (Fold 1)
![SHAP Dependence from fold 1](learner_fold_0_shap_dependence_class_1.png)
### Dependence -1 (Fold 2)
![SHAP Dependence from fold 2](learner_fold_1_shap_dependence_class_-1.png)
### Dependence 0 (Fold 2)
![SHAP Dependence from fold 2](learner_fold_1_shap_dependence_class_0.png)
### Dependence 1 (Fold 2)
![SHAP Dependence from fold 2](learner_fold_1_shap_dependence_class_1.png)
### Dependence -1 (Fold 3)
![SHAP Dependence from fold 3](learner_fold_2_shap_dependence_class_-1.png)
### Dependence 0 (Fold 3)
![SHAP Dependence from fold 3](learner_fold_2_shap_dependence_class_0.png)
### Dependence 1 (Fold 3)
![SHAP Dependence from fold 3](learner_fold_2_shap_dependence_class_1.png)
### Dependence -1 (Fold 4)
![SHAP Dependence from fold 4](learner_fold_3_shap_dependence_class_-1.png)
### Dependence 0 (Fold 4)
![SHAP Dependence from fold 4](learner_fold_3_shap_dependence_class_0.png)
### Dependence 1 (Fold 4)
![SHAP Dependence from fold 4](learner_fold_3_shap_dependence_class_1.png)
### Dependence -1 (Fold 5)
![SHAP Dependence from fold 5](learner_fold_4_shap_dependence_class_-1.png)
### Dependence 0 (Fold 5)
![SHAP Dependence from fold 5](learner_fold_4_shap_dependence_class_0.png)
### Dependence 1 (Fold 5)
![SHAP Dependence from fold 5](learner_fold_4_shap_dependence_class_1.png)

## SHAP Decision plots

### Worst decisions for selected sample 1 (Fold 1)
![SHAP worst decisions from Fold 1](learner_fold_0_sample_0_worst_decisions.png)
### Worst decisions for selected sample 1 (Fold 2)
![SHAP worst decisions from Fold 2](learner_fold_1_sample_0_worst_decisions.png)
### Worst decisions for selected sample 1 (Fold 3)
![SHAP worst decisions from Fold 3](learner_fold_2_sample_0_worst_decisions.png)
### Worst decisions for selected sample 1 (Fold 4)
![SHAP worst decisions from Fold 4](learner_fold_3_sample_0_worst_decisions.png)
### Worst decisions for selected sample 1 (Fold 5)
![SHAP worst decisions from Fold 5](learner_fold_4_sample_0_worst_decisions.png)
### Worst decisions for selected sample 2 (Fold 1)
![SHAP worst decisions from Fold 1](learner_fold_0_sample_1_worst_decisions.png)
### Worst decisions for selected sample 2 (Fold 2)
![SHAP worst decisions from Fold 2](learner_fold_1_sample_1_worst_decisions.png)
### Worst decisions for selected sample 2 (Fold 3)
![SHAP worst decisions from Fold 3](learner_fold_2_sample_1_worst_decisions.png)
### Worst decisions for selected sample 2 (Fold 4)
![SHAP worst decisions from Fold 4](learner_fold_3_sample_1_worst_decisions.png)
### Worst decisions for selected sample 2 (Fold 5)
![SHAP worst decisions from Fold 5](learner_fold_4_sample_1_worst_decisions.png)
### Worst decisions for selected sample 3 (Fold 1)
![SHAP worst decisions from Fold 1](learner_fold_0_sample_2_worst_decisions.png)
### Worst decisions for selected sample 3 (Fold 2)
![SHAP worst decisions from Fold 2](learner_fold_1_sample_2_worst_decisions.png)
### Worst decisions for selected sample 3 (Fold 3)
![SHAP worst decisions from Fold 3](learner_fold_2_sample_2_worst_decisions.png)
### Worst decisions for selected sample 3 (Fold 4)
![SHAP worst decisions from Fold 4](learner_fold_3_sample_2_worst_decisions.png)
### Worst decisions for selected sample 3 (Fold 5)
![SHAP worst decisions from Fold 5](learner_fold_4_sample_2_worst_decisions.png)
### Worst decisions for selected sample 4 (Fold 1)
![SHAP worst decisions from Fold 1](learner_fold_0_sample_3_worst_decisions.png)
### Worst decisions for selected sample 4 (Fold 2)
![SHAP worst decisions from Fold 2](learner_fold_1_sample_3_worst_decisions.png)
### Worst decisions for selected sample 4 (Fold 3)
![SHAP worst decisions from Fold 3](learner_fold_2_sample_3_worst_decisions.png)
### Worst decisions for selected sample 4 (Fold 4)
![SHAP worst decisions from Fold 4](learner_fold_3_sample_3_worst_decisions.png)
### Worst decisions for selected sample 4 (Fold 5)
![SHAP worst decisions from Fold 5](learner_fold_4_sample_3_worst_decisions.png)
### Best decisions for selected sample 1 (Fold 1)
![SHAP best decisions from Fold 1](learner_fold_0_sample_0_best_decisions.png)
### Best decisions for selected sample 1 (Fold 2)
![SHAP best decisions from Fold 2](learner_fold_1_sample_0_best_decisions.png)
### Best decisions for selected sample 1 (Fold 3)
![SHAP best decisions from Fold 3](learner_fold_2_sample_0_best_decisions.png)
### Best decisions for selected sample 1 (Fold 4)
![SHAP best decisions from Fold 4](learner_fold_3_sample_0_best_decisions.png)
### Best decisions for selected sample 1 (Fold 5)
![SHAP best decisions from Fold 5](learner_fold_4_sample_0_best_decisions.png)
### Best decisions for selected sample 2 (Fold 1)
![SHAP best decisions from Fold 1](learner_fold_0_sample_1_best_decisions.png)
### Best decisions for selected sample 2 (Fold 2)
![SHAP best decisions from Fold 2](learner_fold_1_sample_1_best_decisions.png)
### Best decisions for selected sample 2 (Fold 3)
![SHAP best decisions from Fold 3](learner_fold_2_sample_1_best_decisions.png)
### Best decisions for selected sample 2 (Fold 4)
![SHAP best decisions from Fold 4](learner_fold_3_sample_1_best_decisions.png)
### Best decisions for selected sample 2 (Fold 5)
![SHAP best decisions from Fold 5](learner_fold_4_sample_1_best_decisions.png)
### Best decisions for selected sample 3 (Fold 1)
![SHAP best decisions from Fold 1](learner_fold_0_sample_2_best_decisions.png)
### Best decisions for selected sample 3 (Fold 2)
![SHAP best decisions from Fold 2](learner_fold_1_sample_2_best_decisions.png)
### Best decisions for selected sample 3 (Fold 3)
![SHAP best decisions from Fold 3](learner_fold_2_sample_2_best_decisions.png)
### Best decisions for selected sample 3 (Fold 4)
![SHAP best decisions from Fold 4](learner_fold_3_sample_2_best_decisions.png)
### Best decisions for selected sample 3 (Fold 5)
![SHAP best decisions from Fold 5](learner_fold_4_sample_2_best_decisions.png)
### Best decisions for selected sample 4 (Fold 1)
![SHAP best decisions from Fold 1](learner_fold_0_sample_3_best_decisions.png)
### Best decisions for selected sample 4 (Fold 2)
![SHAP best decisions from Fold 2](learner_fold_1_sample_3_best_decisions.png)
### Best decisions for selected sample 4 (Fold 3)
![SHAP best decisions from Fold 3](learner_fold_2_sample_3_best_decisions.png)
### Best decisions for selected sample 4 (Fold 4)
![SHAP best decisions from Fold 4](learner_fold_3_sample_3_best_decisions.png)
### Best decisions for selected sample 4 (Fold 5)
![SHAP best decisions from Fold 5](learner_fold_4_sample_3_best_decisions.png)

[<< Go back](../README.md)
