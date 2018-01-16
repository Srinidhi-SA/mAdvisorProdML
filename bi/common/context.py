from bi.common.decorators import accepts
from bi.settings import setting as GLOBALSETTINGS
import ast
class ContextSetter:

    MEASUREC_COLUMNS = "measure_columns"
    DIMENSION_COLUMNS = "dimension_columns"
    TIME_DIMENSION_COLUMNS = "time_dimension_columns"
    NULL_VALUES = 'num_nulls'
    NON_NULL_VALUES = 'num_non_nulls'

    def __init__(self, config_obj):
        self._BASE_DIR = None
        self._config_obj = config_obj
        self._column_separator = "|~|"
        self.CSV_FILE = ""
        self.RESULT_FILE = ""
        self.NARRATIVES_FILE = ""
        self.OUTPUT_FILEPATH = ""
        self.resultcolumn = ""
        self.MONITOR_API = ""
        self.analysistype = ""
        self.ignorecolumns = []
        self.utf8columns = []
        self.considercolumns = []
        self.considercolumnstype = ["including"]
        self.measure_suggestions = []

        self.MODELFEATURES = []
        self.appid = None
        self.algorithmslug = []
        self.levelcount_dict = {}
        self.dimension_filter = {}
        self.measure_filter = {}
        self.time_dimension_filter = {}
        self.message_url = ""
        self.analysisList = []
        self.existingColumnTransformsSettings = []
        self.newColumnTransformsSettings = []
        self.runEnvironment = None
        self.METADATA_URL = None
        self.METADATA_SLUGS = None
        self.dbConnectionParams = {}
        self.dataSourceType = None
        self.measureAnalysisWeight = {}
        self.dimensionAnalysisWeight = {}
        self.globalCompletionStatus = 0
        self.currentAnalysis = None
        self.analysisDict = {}
        self.stockSymbolList = []
        self.dataAPI = ""
        self.trendSettings = None
        self.metaIgnoreMsgFlag = False
        self.customAnalysisDetails = []
        self.jobType = None
        self.storyOnScoredData = False
        self.uidCol = None
        self.ignoremessages = False
        self.labelMappingDict = []
        self.percentageColumns = []
        self.dollarColumns = []
        self.colPolarity = []

        self.requestedDateFormat = None
        self.dateFormatDict = {}
        self.allDateColumns = []
        self.string_to_date_columns = {}
        self.dateFormatDetails = {}
        self.dateTimeSuggestions = []
        self.selected_date_columns = []



    def set_params(self):
        self.FILE_SETTINGS = self._config_obj.get_file_settings()
        self.COLUMN_SETTINGS = self._config_obj.get_column_settings()
        self.FILTER_SETTINGS = self._config_obj.get_filter_settings()
        self.ADVANCE_SETTINGS = self._config_obj.get_advance_settings()
        self.TRANSFORMATION_SETTINGS = self._config_obj.get_transformation_settings()
        self.STOCK_SETTINGS = self._config_obj.get_stock_settings()
        self.DATABASE_SETTINGS = self._config_obj.get_database_settings()

        fileSettingKeys = self.FILE_SETTINGS.keys()
        columnSettingKeys = self.COLUMN_SETTINGS.keys()
        filterSettingKeys = self.FILTER_SETTINGS.keys()
        advanceSettingKeys = self.ADVANCE_SETTINGS.keys()
        transformSettingsKeys = self.TRANSFORMATION_SETTINGS.keys()
        stockSettingKeys = self.STOCK_SETTINGS.keys()
        dbSettingKeys = self.DATABASE_SETTINGS.keys()

        if len(dbSettingKeys) > 0:
            if "datasource_details" in dbSettingKeys:
                self.dbConnectionParams = self.DATABASE_SETTINGS["datasource_details"]
            if "datasource_type" in dbSettingKeys:
                self.dataSourceType = self.DATABASE_SETTINGS["datasource_type"]

        if len(fileSettingKeys) > 0:
            if "metadata" in fileSettingKeys:
                self.METADATA_URL = self.FILE_SETTINGS['metadata']["url"]
                self.METADATA_SLUGS = self.FILE_SETTINGS['metadata']["slug_list"]
            if "inputfile" in fileSettingKeys:
                if len(self.FILE_SETTINGS['inputfile']) > 0:
                    self.CSV_FILE =self.FILE_SETTINGS['inputfile'][0]
            if "outputfile" in fileSettingKeys:
                self.OUTPUT_FILEPATH =self.FILE_SETTINGS['outputfile'][0]
            if "narratives_file" in fileSettingKeys:
                self.NARRATIVES_FILE =self.FILE_SETTINGS['narratives_file'][0]
            if "result_file" in fileSettingKeys:
                self.RESULT_FILE =self.FILE_SETTINGS['result_file'][0]
            if "monitor_api" in fileSettingKeys:
                self.MONITOR_API =self.FILE_SETTINGS['monitor_api'][0]
            if "train_test_split" in fileSettingKeys:
                self.train_test_split =self.FILE_SETTINGS['train_test_split'][0]
            if "modelpath" in fileSettingKeys:
                self.MODEL_PATH =self.FILE_SETTINGS['modelpath'][0]
            if "scorepath" in fileSettingKeys:
                self.SCORE_PATH =self.FILE_SETTINGS['scorepath'][0]
            if "foldername" in fileSettingKeys:
                self.FOLDERS =self.FILE_SETTINGS['foldername'][0]
            if "modelname" in fileSettingKeys:
                self.MODELS =self.FILE_SETTINGS['modelname'][0]
            if "modelfeatures" in fileSettingKeys:
                self.MODELFEATURES = self.FILE_SETTINGS['modelfeatures']
                # if modelfeaturedata != None and len(modelfeaturedata) > 0:
                #     modelfeaturedata = modelfeaturedata[0]
                #     if self._column_separator in modelfeaturedata:
                #         self.MODELFEATURES =modelfeaturedata.split(self._column_separator)
            if "levelcounts" in fileSettingKeys:
                levelcountdata = self.FILE_SETTINGS['levelcounts']
                if levelcountdata != None and len(levelcountdata) > 0:
                    levelcountdata = levelcountdata[0]
                    # if self._column_separator in levelcountdata:
                    #     self.levelcounts =self.FILE_SETTINGS['levelcounts'][0].split(self._column_separator)
                    #     self.levelcount_dict = dict([(self.levelcounts[i*2],self.levelcounts[i*2+1]) for i in range(len(self.levelcounts)/2)])
                    # else:
                    #     self.levelcount_dict = {}
                    self.levelcount_dict = levelcountdata
            if "script_to_run" in fileSettingKeys:
                self.scripts_to_run =self.FILE_SETTINGS.get('script_to_run')
            else:
                self.scripts_to_run = []
            if "algorithmslug" in fileSettingKeys:
                self.algorithmslug = self.FILE_SETTINGS['algorithmslug']
            if 'labelMappingDict' in fileSettingKeys:
                self.labelMappingDict = self.FILE_SETTINGS['labelMappingDict']

        if len(columnSettingKeys) > 0:
            if "variableSelection" in columnSettingKeys:
                varSelectionArr = self.COLUMN_SETTINGS["variableSelection"]
                self.considercolumns = []
                for colSetting in varSelectionArr:
                    self.considercolumns.append(colSetting["name"])
                    if colSetting["targetColumn"] == True:
                        self.resultcolumn = colSetting["name"]
                        if colSetting["columnType"] == "measure":
                            if colSetting["setVarAs"] != None:
                                self.analysistype = "dimension"
                            else:
                                self.analysistype = "measure"
                        elif colSetting["columnType"] == "dimension":
                            self.analysistype = "dimension"
                    if colSetting["uidCol"] == True:
                        self.uidCol = colSetting["name"]
                    if colSetting["columnType"] == "datetime" or colSetting["dateSuggestionFlag"] == True:
                        self.allDateColumns.append(colSetting["name"])
                        if colSetting["selected"] == True:
                            self.selected_date_columns.append(colSetting["name"])
                    if colSetting["dateSuggestionFlag"] == True:
                        self.dateTimeSuggestions.append(colSetting["name"])
                    if colSetting["setVarAs"] != None:
                        self.customAnalysisDetails.append({"colName":colSetting["name"],"treatAs":colSetting["setVarAs"]})
                    if colSetting["polarity"] != None:
                        self.colPolarity.append({"colName":colSetting["name"],"polarity":colSetting["polarity"]})

        if len(filterSettingKeys) > 0:
            if "dimensionColumnFilters" in filterSettingKeys:
                self.dimension_filter = self.FILTER_SETTINGS.get("dimensionColumnFilters")
            if "measureColumnFilters" in filterSettingKeys:
                self.measure_filter = self.FILTER_SETTINGS.get("measureColumnFilters")
            if "timeDimensionColumnFilters" in filterSettingKeys:
                self.time_dimension_filter = self.FILTER_SETTINGS.get("timeDimensionColumnFilters")

        if len(advanceSettingKeys) > 0:
            if "analysis" in advanceSettingKeys:
                analysis_array = self.ADVANCE_SETTINGS["analysis"]
                analysisList = [obj["name"] for obj in analysis_array if obj["status"] == True]
                analysisDictList = []
                for obj in analysis_array:
                    tempDict = {}
                    if obj["status"] == True:
                        tempDict["analysisSubTypes"] = [val["name"] for val in obj["analysisSubTypes"] if val["status"]==True]
                        tempDict["name"] = obj["name"]
                        tempDict["displayName"] = obj["displayName"]
                        if "binSetting" in obj:
                            tempDict["binSetting"] = {}
                            binSettingArray = obj["binSetting"]
                            for val in binSettingArray:
                                if val["name"] == "binLevels":
                                    tempDict["binSetting"].update({"bins":val["value"]})
                                elif val["name"] == "binCardinality":
                                    tempDict["binSetting"].update({"binCardinality":val["value"]})
                        if obj["noOfColumnsToUse"] == None:
                            tempDict["noOfColumnsToUse"] = None
                        else:
                            nCols = [val["value"] if val["name"]=="custom" else val["defaultValue"] for val in [k for k in obj["noOfColumnsToUse"] if k["status"]==True]]
                            try:
                                tempDict["noOfColumnsToUse"] = int(nCols[0])
                            except:
                                tempDict["noOfColumnsToUse"] = int([val["defaultValue"] for val in [k for k in obj["noOfColumnsToUse"] if k["status"]==True]][0])

                        analysisDictList.append(tempDict)
                # adding overview to analysisList
                # required to create the summary node
                if "overview" not in analysisList:
                    analysisList.append("overview")
                    analysisDictList.append(
                        {
                            "analysisSubTypes" : [],
                            "displayName" : "Overview",
                            "name" : "overview",
                            "noOfColumnsToUse" : None,
                            "status" : True
                        }
                    )
                self.analysisList = [GLOBALSETTINGS.scriptsMapping[x] for x in analysisList]
                self.analysisDict = dict(zip(self.analysisList,analysisDictList))
            if "trendSettings" in advanceSettingKeys:
                trendSettingObj = self.ADVANCE_SETTINGS["trendSettings"]
                trendSettings = [obj for obj in trendSettingObj if obj["status"]==True]
                if len(trendSettings) > 0:
                    self.trendSettings = trendSettings[0]

            if "targetLevels" in advanceSettingKeys:
                self.targetLevels = self.ADVANCE_SETTINGS["targetLevels"]

        if len(transformSettingsKeys) > 0:
            if "newColumns" in transformSettingsKeys:
                newColumnActions = self.TRANSFORMATION_SETTINGS["newColumns"]

            if "existingColumns" in transformSettingsKeys:
                existingColumnActions = self.TRANSFORMATION_SETTINGS["existingColumns"]
                validColumnActions = []
                for transformObj in existingColumnActions:
                    valid = False
                    validColumnSetting = []
                    for action in transformObj["columnSetting"]:
                        if action["status"] == True:
                            valid = True
                            validColumnSetting.append(action)
                    actionOrder = {"delete":0,"rename":2,"replace":1,"data_type":3}
                    validColumnSetting = [x for x in validColumnSetting if x in actionOrder.keys()]
                    validColumnSetting = sorted(validColumnSetting,key=lambda x:actionOrder[x["actionName"]])
                    if valid:
                        validObj = transformObj
                        validObj["columnSetting"] = validColumnSetting
                        validColumnActions.append(validObj)
                self.existingColumnTransformsSettings = validColumnActions

        if len(stockSettingKeys) > 0:
            if "stockSymbolList" in stockSettingKeys:
                self.stockSymbolList = self.STOCK_SETTINGS.get("stockSymbolList")
            if "dataAPI" in stockSettingKeys:
                self.dataAPI = self.STOCK_SETTINGS.get("dataAPI")

        if self.analysistype in ["measure","dimension"]:
            self.set_analysis_weights(self.analysisList,self.analysistype)

    def set_ignore_column_suggestions(self,ignoreSuggestions):
        self.ignorecolumns = ignoreSuggestions

    def set_utf8_columns(self,utf8Cols):
        self.utf8columns = utf8Cols

    def set_date_format(self,dateFormat):
        self.dateFormatDict = dateFormat

    def get_date_format_dict(self):
        return self.dateFormatDict

    def get_selected_date_columns(self):
        return self.selected_date_columns

    def set_measure_suggestions(self,measureSugCols):
        self.measure_suggestions = measureSugCols

    # need to check its usage
    def set_date_format_details(self,data):
        self.dateFormatDetails = data

    def get_date_format_details(self):
        return self.dateFormatDetails

    @accepts(object,(list,tuple))
    def set_percentage_columns(self,data):
        self.percentageColumns = data

    def get_percentage_columns(self):
        return self.percentageColumns

    def set_dollar_columns(self,data):
        self.dollarColumns = data

    def get_dollar_columns(self):
        return self.dollarColumns

    def get_label_map(self):
        if len(self.labelMappingDict) > 0:
            original = self.labelMappingDict[0]
            modified = {}
            for val in original:
                modified[int(val)] = original[val]
            return modified
        else:
            return []
    def get_uid_column(self):
        return self.uidCol
    def get_datasource_type(self):
        return self.dataSourceType
    def get_dbconnection_params(self):
        return self.dbConnectionParams
    def get_metadata_ignore_msg_flag(self):
        return self.metaIgnoreMsgFlag
    def set_metadata_ignore_msg_flag(self,data):
        self.metaIgnoreMsgFlag = data
    def get_metadata_script_weight(self):
        return GLOBALSETTINGS.metadataScriptWeight
    def get_subsetting_script_weight(self):
        return GLOBALSETTINGS.subsettingScriptWeight
    def set_model_path(self,data):
        self.MODEL_PATH = data
    def set_environment(self,data):
        self.runEnvironment = data
    def get_environement(self):
        return self.runEnvironment
    def set_score_path(self,data):
        self.SCORE_PATH = data
    def set_analysis_name(self,name):
        self.currentAnalysis = name
    def get_analysis_name(self):
        return self.currentAnalysis
    def set_analysis_weights(self,scriptsToRun,analysis_type):
        scriptsToRun += ["initialization"]
        if analysis_type == "measure":
            relativeWeightArray = [GLOBALSETTINGS.measureAnalysisRelativeWeight[x] for x in scriptsToRun]
        elif analysis_type == "dimension":
            relativeWeightArray = [GLOBALSETTINGS.dimensionAnalysisRelativeWeight[x] for x in scriptsToRun]
        totalWeight = sum(relativeWeightArray)
        percentWeight = [int(round(x*100/float(totalWeight))) for x in relativeWeightArray]
        diff = sum(percentWeight) - 100
        percentWeight = percentWeight[:-1] + [percentWeight[-1]+-(diff)]
        weightDict = dict(zip(scriptsToRun,percentWeight))
        outputdict = {}
        for k,v in weightDict.items():
            outputdict[k] = {"total":v,"script":v/2,"narratives":v-v/2}
        if analysis_type == "measure":
            self.measureAnalysisWeight = outputdict
        elif analysis_type == "dimension":
            self.dimensionAnalysisWeight = outputdict



    def get_custom_analysis_details(self):
        if self.customAnalysisDetails:
            return self.customAnalysisDetails
        else:
            return None

    def get_metadata_url(self):
        return self.METADATA_URL

    def get_metadata_slugs(self):
        return self.METADATA_SLUGS

    def get_stock_symbol_list(self):
        return self.stockSymbolList

    def get_stock_data_api(self):
        return self.dataAPI

    def get_trend_settings(self):
        return self.trendSettings

    def get_target_levels(self):
        return self.targetLevels

    def get_measure_analysis_weight(self):
        return self.measureAnalysisWeight

    def get_dimension_analysis_weight(self):
        return self.dimensionAnalysisWeight

    def get_ml_model_training_weight(self):
        return GLOBALSETTINGS.mlModelTrainingWeight

    def get_ml_model_prediction_weight(self):
        return GLOBALSETTINGS.mlModelPredictionWeight

    def update_completion_status(self,data):
        self.globalCompletionStatus = data

    def get_completion_status(self):
        return self.globalCompletionStatus

    def get_existing_column_transform_settings(self):
        return self.existingColumnTransformsSettings

    def get_new_column_transform_settings(self):
        return self.newColumnTransformsSettings

    def get_analysis_dict(self):
        return self.analysisDict

    def get_analysis_name_list(self):
        return self.analysisList

    def get_algorithm_slug(self):
        return self.algorithmslug

    def get_column_separator(self):
        return self._column_separator

    def get_level_count_dict(self):
        return self.levelcount_dict

    def get_measure_suggestions(self):
        return self.measure_suggestions

    def get_scripts_to_run(self):
        return self.scripts_to_run

    def get_consider_columns_type(self):
        return self.considercolumnstype

    def get_score_consider_columns_type(self):
        return self.scoreconsidercolumnstype

    def get_input_file(self):
        return self.CSV_FILE

    def get_narratives_file(self):
        return self.NARRATIVES_FILE

    def get_result_file(self):
        return self.RESULT_FILE

    def get_result_column(self):
        return self.resultcolumn

    def get_monitor_api(self):
        return self.MONITOR_API

    def get_analysis_type(self):
        return self.analysistype

    def get_consider_columns(self):
        return self.considercolumns

    def get_score_consider_columns(self):
        return self.scoreconsidercolumns

    def get_ignore_column_suggestions(self):
        return self.ignorecolumns

    def get_utf8_columns(self):
        return self.utf8columns

    def get_dimension_filters(self):
        return self.dimension_filter

    def get_measure_filters(self):
        return self.measure_filter

    def get_time_dimension_filters(self):
        return self.time_dimension_filter

    def get_date_settings(self):
        return self.string_to_date_columns

    def get_column_subset(self):
        return self.considercolumns

    def get_date_filters(self):
        return self.date_filter

    def get_date_columns(self):
        return self.allDateColumns

    def get_requested_date_format(self):
        return self.requestedDateFormat

    def get_train_test_split(self):
        return self.train_test_split

    def get_model_path(self):
        return self.MODEL_PATH

    def get_score_path(self):
        return self.SCORE_PATH

    def get_model_features(self):
        return self.MODELFEATURES

    def get_app_id(self):
        return self.appid

    def get_datetime_suggestions(self):
        return self.dateTimeSuggestions

    def get_output_filepath(self):
        return self.OUTPUT_FILEPATH

    def set_message_url(self,data):
        self.message_url = data

    def get_message_url(self):
        return self.message_url

    def set_job_type(self,data):
        self.jobType = data

    def get_job_type(self):
        return self.jobType

    def set_story_on_scored_data(self,data):
        self.storyOnScoredData = data

    def get_story_on_scored_data(self):
        return self.storyOnScoredData

    def set_message_ignore(self,data):
        self.ignoremessages = data

    def get_message_ignore(self):
        return self.ignoremessages

    def get_script_weights(self):
        jobType = self.get_job_type()
        analysistype = self.get_analysis_type()
        if jobType == "story":
            if analysistype == "dimension":
                scriptWeightDict = self.get_dimension_analysis_weight()
            elif analysistype == "measure":
                scriptWeightDict = self.get_measure_analysis_weight()
        elif jobType == "training":
            scriptWeightDict = self.get_ml_model_training_weight()
        elif jobType == "prediction":
            scriptWeightDict = self.get_ml_model_prediction_weight()
        elif jobType == "metaData":
            scriptWeightDict = self.get_metadata_script_weight()
        elif jobType == "subSetting":
            scriptWeightDict = self.get_subsetting_script_weight()
        return scriptWeightDict
