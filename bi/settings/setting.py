DECISIONTREERKMEANSTARGETNAME = ['Low','Medium','High']
HDFS_SECRET_KEY = "xfBmEcr_hFHGqVrTo2gMFpER3ks9x841UcvJbEQJesI="
ANOVAMAXLEVEL = 200
BLOCKSPLITTER = "|~NEWBLOCK~|"
scriptsMapping = {
    "overview" : "Descriptive analysis",
    "performance" : "Measure vs. Dimension",
    "influencer" : "Measure vs. Measure",
    "prediction" : "Predictive modeling",
    "trend" : "Trend",
    "association" : "Dimension vs. Dimension"
}
measureAnalysisRelativeWeight = {
    "initialization":0.25,
    "Descriptive analysis":1,
    "Measure vs. Dimension":3,
    "Measure vs. Measure":3,
    "Trend":1.5,
    "Predictive modeling":1.5
}
dimensionAnalysisRelativeWeight = {
    "initialization":0.25,
    "Descriptive analysis":1,
    "Dimension vs. Dimension":4,
    "Trend":2.5,
    "Predictive modeling":2.5
}
mlModelTrainingWeight = {
    "initialization":{"total":10,"script":10,"narratives":10},
    "randomForest":{"total":30,"script":30,"narratives":30},
    "logisticRegression":{"total":30,"script":30,"narratives":30},
    "xgboost":{"total":30,"script":30,"narratives":30}
}
mlModelPredictionWeight = {
    "initialization":{"total":10,"script":10,"narratives":10},
    "randomForest":{"total":20,"script":20,"narratives":20},
    "logisticRegression":{"total":20,"script":20,"narratives":20},
    "xgboost":{"total":20,"script":20,"narratives":20},
    "Descriptive analysis":{"total":10,"script":10,"narratives":10},
    "Dimension vs. Dimension":{"total":10,"script":5,"narratives":5},
    "Predictive modeling":{"total":10,"script":5,"narratives":5}
}
metadataScriptWeight = {
    "initialization":{"total":3,"script":2,"narratives":1},
}
subsettingScriptWeight = {
    "initialization":{"total":3,"script":2,"narratives":1},
}
