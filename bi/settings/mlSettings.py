from pySparkMLClassificationParams import *
from pySparkMLRegressionParams import *
from sklearnMLClassificationParams import *
from sklearnMLRegressionParams import *

ALGORITHMRANDOMSLUG = "f77631ce2ab24cf78c55bb6a5fce4db8"
MLENVIRONMENT = "python" #can be python or spark

SKLEARN_GRIDSEARCH_PARAMS = [
            {
                "name":"evaluationMetric",
                "displayName":"Metric Used for Optimization",
                "defaultValue":[
                        {
                            "name":"accuracy",
                            "selected":True,
                            "displayName":"Accuracy"
                        },
                        {
                            "name":"precision",
                            "selected":False,
                            "displayName":"Precision"
                        },
                        {
                            "name":"recall",
                            "selected":False,
                            "displayName":"Recall"
                        }
                       ],
                "paramType":"list",
                "uiElemType":"dropDown",
                "display":True
            },
            {
                "name":"iidAssumption",
                "displayName":"Independent and Identical Distributed",
                 "defaultValue":[
                        {
                            "name":"true",
                            "selected":True,
                            "displayName":"True"
                        },
                        {
                            "name":"false",
                            "selected":False,
                            "displayName":"False"
                        }
                       ],
                "paramType":"list",
                "uiElemType":"dropDown",
                "display":True
            },
            {
                    "name":"kFold",
                    "displayName":"No Of Folds to Use",
                    "defaultValue":3,
                    "acceptedValue":None,
                    "valueRange":[2,10],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True

            }
]
SKLEARN_RANDOMSEARCH_PARAMS = [
            {
                "name":"evaluationMetric",
                "displayName":"Metric Used for Optimization",
                "defaultValue":[
                        {
                            "name":"accuracy",
                            "selected":True,
                            "displayName":"Accuracy"
                        },
                        {
                            "name":"precision",
                            "selected":False,
                            "displayName":"Precision"
                        },
                        {
                            "name":"recall",
                            "selected":False,
                            "displayName":"Recall"
                        }
                       ],
                "paramType":"list",
                "uiElemType":"dropDown",
                "display":True
            },
            {
                "name":"iidAssumption",
                "displayName":"Independent and Identical Distributed",
                 "defaultValue":[
                        {
                            "name":"true",
                            "selected":True,
                            "displayName":"True"
                        },
                        {
                            "name":"false",
                            "selected":False,
                            "displayName":"False"
                        }
                       ],
                "paramType":"list",
                "uiElemType":"dropDown",
                "display":True
            },
            {
                    "name":"kFold",
                    "displayName":"No Of Folds to Use",
                    "defaultValue":3,
                    "acceptedValue":None,
                    "valueRange":[2,10],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True

            }
]
SKLEARN_NONE_PARAMS = [
            {
                "name":"evaluationMetric",
                "displayName":"Metric Used for Optimization",
                "defaultValue":[
                       ],
                "paramType":"list",
                "uiElemType":"dropDown",
                "display":True
            },
            {
                "name":"iidAssumption",
                "displayName":"Independent and Identical Distributed",
                 "defaultValue":[
                       ],
                "paramType":"list",
                "uiElemType":"dropDown",
                "display":True
            },
            {
                    "name":"kFold",
                    "displayName":"No Of Folds to Use",
                    "defaultValue":3,
                    "acceptedValue":None,
                    "valueRange":[2,10],
                    "paramType":"number",
                    "uiElemType":"slider",
                    "display":True

            }
]

SKLEARN_HYPERPARAMETER_OBJECT = [
    {
        "name":"gridsearchcv",
        "params":SKLEARN_GRIDSEARCH_PARAMS,
        "displayName":"Grid Search",
        "selected":False
    },
    {
        "name":"randomsearchcv",
        "params":SKLEARN_RANDOMSEARCH_PARAMS,
        "displayName":"Random Search",
        "selected": False

    },
    {
        "name":"none",
        "params":None,
        "displayName":"None",
        "selected": True
    }
]

PYSPARK_HYPERPARAMETER_OBJECT = [
    {
        "name":"gridsearchcv",
        "params":SKLEARN_GRIDSEARCH_PARAMS,
        "displayName":"Grid Search",
        "selected":False
    },
    {
        "name":"randomsearchcv",
        "params":SKLEARN_RANDOMSEARCH_PARAMS,
        "displayName":"Random Search",
        "selected": False

    },
    {
        "name":"none",
        "params":None,
        "displayName":"None",
        "selected": True
    }
]

if MLENVIRONMENT == "spark":
    ALGORITHM_LIST_REGRESSION={
        "ALGORITHM_SETTING":[
          {
            "algorithmName": "Linear Regression",
            "selected": True,
            "parameters": PYSPARK_ML_LINEAR_REGRESSION_PARAMS,
            "algorithmSlug": ALGORITHMRANDOMSLUG+"linr",
            "hyperParameterSetting": PYSPARK_HYPERPARAMETER_OBJECT,
            "description":"fill in the blanks"
          },
          {
            "algorithmName": "Gradient Boosted Tree Regression",
            "selected": True,
            "parameters": PYSPARK_ML_GBT_REGRESSION_PARAMS,
            "algorithmSlug": ALGORITHMRANDOMSLUG+"gbtr",
            "hyperParameterSetting": PYSPARK_HYPERPARAMETER_OBJECT,
            "description":"fill in the blanks"
          },
          {
            "algorithmName": "Decision Tree Regression",
            "selected": True,
            "parameters": PYSPARK_ML_DTREE_REGRESSION_PARAMS,
            "algorithmSlug": ALGORITHMRANDOMSLUG+"dtreer",
            "hyperParameterSetting": PYSPARK_HYPERPARAMETER_OBJECT,
            "description":"fill in the blanks"
          },
          {
            "algorithmName": "Random Forest Regression",
            "selected": True,
            "parameters": PYSPARK_ML_RF_REGRESSION_PARAMS,
            "algorithmSlug": ALGORITHMRANDOMSLUG+"rfr",
            "hyperParameterSetting": PYSPARK_HYPERPARAMETER_OBJECT,
            "description":"fill in the blanks"
          }
        ]
    }
    ALGORITHM_LIST_CLASSIFICATION = {
        "ALGORITHM_SETTING": [
            # {
            #     "algorithmName": "Logistic Regression",
            #     "selected": True,
            #     "parameters": PYSPARK_ML_LINEAR_REGRESSION_PARAMS,
            #     "algorithmSlug": ALGORITHMRANDOMSLUG + "linr",
            # "hyperParameterSetting": PYSPARK_HYPERPARAMETER_OBJECT,
            # "description":"fill in the blanks"
            # },
            # {
            #     "algorithmName": "Random Forest",
            #     "selected": True,
            #     "parameters": PYSPARK_ML_GBT_REGRESSION_PARAMS,
            #     "algorithmSlug": ALGORITHMRANDOMSLUG + "gbtr",
            # "hyperParameterSetting": PYSPARK_HYPERPARAMETER_OBJECT,
            # "description":"fill in the blanks"
            # },
            # {
            #     "algorithmName": "XGBoost",
            #     "selected": True,
            #     "parameters": PYSPARK_ML_DTREE_REGRESSION_PARAMS,
            #     "algorithmSlug": ALGORITHMRANDOMSLUG + "dtreer",
            #     "hyperParameterSetting": PYSPARK_HYPERPARAMETER_OBJECT,
            # "description":"fill in the blanks"
            # },
            # {
            #     "algorithmName": "SVM",
            #     "selected": True,
            #     "parameters": PYSPARK_ML_RF_REGRESSION_PARAMS,
            #     "algorithmSlug": ALGORITHMRANDOMSLUG + "rfr",
            # "hyperParameterSetting": PYSPARK_HYPERPARAMETER_OBJECT,
            # "description":"fill in the blanks"
            # }
        ]
    }
else:
    ALGORITHM_LIST_REGRESSION={
        "ALGORITHM_SETTING":[
          {
            "algorithmName": "Linear Regression",
            "selected": True,
            "parameters": SKLEARN_ML_LINEAR_REGRESSION_PARAMS,
            "algorithmSlug": ALGORITHMRANDOMSLUG+"linr",
            "hyperParameterSetting":SKLEARN_HYPERPARAMETER_OBJECT,
            "description":"fill in the blanks"
          },
          {
            "algorithmName": "Gradient Boosted Tree Regression",
            "selected": True,
            "parameters": SKLEARN_ML_GBT_REGRESSION_PARAMS,
            "algorithmSlug": ALGORITHMRANDOMSLUG+"gbtr",
            "hyperParameterSetting": SKLEARN_HYPERPARAMETER_OBJECT,
            "description":"fill in the blanks"

          },
          {
            "algorithmName": "Decision Tree Regression",
            "selected": True,
            "parameters": SKLEARN_ML_DTREE_REGRESSION_PARAMS,
            "algorithmSlug": ALGORITHMRANDOMSLUG+"dtreer",
            "hyperParameterSetting": SKLEARN_HYPERPARAMETER_OBJECT,
            "description":"fill in the blanks"
          },
          {
            "algorithmName": "Random Forest Regression",
            "selected": True,
            "parameters": SKLEARN_ML_RF_REGRESSION_PARAMS,
            "algorithmSlug": ALGORITHMRANDOMSLUG+"rfr",
            "hyperParameterSetting": SKLEARN_HYPERPARAMETER_OBJECT,
            "description":"fill in the blanks"
          }
        ]
    }
    ALGORITHM_LIST_CLASSIFICATION = {
        "ALGORITHM_SETTING": [
            {
                "algorithmName": "Logistic Regression",
                "selected": True,
                "parameters": SKLEARN_ML_LOGISTIC_REGRESSION_PARAMS,
                "algorithmSlug": ALGORITHMRANDOMSLUG + "lr",
                "hyperParameterSetting": SKLEARN_HYPERPARAMETER_OBJECT,
                "description":"A statistical method to predict the likely outcome of any qualitative attribute. It is invariably used for predicting binary outcomes (such as Yes or No)."
            },
            {
                "algorithmName": "Random Forest",
                "selected": True,
                "parameters": SKLEANR_ML_RF_CLASSIFICATION_PARAMS,
                "algorithmSlug": ALGORITHMRANDOMSLUG + "rf",
                "hyperParameterSetting": SKLEARN_HYPERPARAMETER_OBJECT,
                "description":"""A meta estimator that uses averaging predictive power of a number of decision tree
                classification models. This is very effective in predicting the likelihood in multi-class
                classifications and also to control overfitting."""
            },
            {
                "algorithmName": "XGBoost",
                "selected": True,
                "parameters": SKLEARN_ML_XGBOOST_CLASSIFICATION_PARAMS,
                "algorithmSlug": ALGORITHMRANDOMSLUG + "xgb",
                "hyperParameterSetting": SKLEARN_HYPERPARAMETER_OBJECT,
                "description":"""A machine learning technique that produces an ensemble of multiple decision tree
                models to predict categorical variables. It is highly preferred to leverage
                computational power to build scalable and accurate models."""
            },
            # {
            #     "algorithmName": "SVM",
            #     "selected": False,
            #     "parameters": SKLEARN_ML_RF_REGRESSION_PARAMS,
            #     "algorithmSlug": ALGORITHMRANDOMSLUG + "rfr",
            #     "hyperParameterSetting": SKLEARN_HYPERPARAMETER_OBJECT,
            # "description":"fill in the blanks"
            # }
        ]
    }
