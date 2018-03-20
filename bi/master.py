import sys
import sys
import time
import json
import pyhocon

reload(sys)
sys.setdefaultencoding('utf-8')

from bi.settings import *
from bi.common import utils as CommonUtils
from bi.common import DataLoader,MetaParser, DataFrameHelper,ContextSetter,ResultSetter
from bi.common import NarrativesTree,ConfigValidator
from parser import configparser
from bi.scripts.stock_advisor import StockAdvisor
from bi.settings import setting as GLOBALSETTINGS
import master_helper as MasterHelper
def main(configJson):
    LOGGER = {}
    deployEnv = False  # running the scripts from job-server env
    debugMode = True   # runnning the scripts for local testing and development
    cfgMode = False    # runnning the scripts by passing config.cfg path
    scriptStartTime = time.time()
    if isinstance(configJson,pyhocon.config_tree.ConfigTree) or isinstance(configJson,dict):
        deployEnv = True
        debugMode = False
        ignoreMsg = False
    elif isinstance(configJson,basestring):
        if configJson.endswith(".cfg"):
            print "######################## Running in cfgMode ########################"
            cfgMode = True
            debugMode = False
            ignoreMsg = False
        else:
            print "######################## Running in debugMode ######################"
            cfgMode = False
            debugMode = True
            ignoreMsg = True
            # Test Configs are defined in bi/settings/configs/localConfigs
            jobType = "subSetting"
            configJson = get_test_configs(jobType)

    print "######################## Creating Spark Session ###########################"
    if debugMode:
        APP_NAME = "mAdvisor_running_in_debug_mode"
    else:
        if "job_config" in configJson.keys() and "job_name" in configJson["job_config"].keys():
            APP_NAME = configJson["job_config"]["job_name"]
        else:
            APP_NAME = "--missing--"

    spark = CommonUtils.get_spark_session(app_name=APP_NAME)
    spark.sparkContext.setLogLevel("ERROR")
    print "######################### Parsing the configs #############################"

    config = configJson["config"]
    job_config = configJson["job_config"]
    jobType = job_config["job_type"]
    messageUrl = configJson["job_config"]["message_url"]
    jobName = job_config["job_name"]
    try:
        errorURL = job_config["error_reporting_url"]
    except:
        errorURL = None
    if "app_id" in job_config:
        appid = job_config["app_id"]
    else:
        appid = None
    configJsonObj = configparser.ParserConfig(config)
    configJsonObj.set_json_params()
    dataframe_context = ContextSetter(configJsonObj)
    dataframe_context.set_job_type(jobType)
    dataframe_context.set_message_url(messageUrl)
    dataframe_context.set_params()
    dataframe_context.set_app_id(appid)
    dataframe_context.set_debug_mode(debugMode)
    dataframe_context.set_job_url(job_config["job_url"])
    dataframe_context.set_app_name(APP_NAME)
    dataframe_context.set_error_url(errorURL)
    dataframe_context.set_logger(LOGGER)
    dataframe_context.set_xml_url(job_config["xml_url"])
    dataframe_context.set_job_name(jobName)
    if debugMode == True:
        dataframe_context.set_environment("debugMode")
        dataframe_context.set_message_ignore(True)

    messageURL = dataframe_context.get_message_url()
    analysistype = dataframe_context.get_analysis_type()
    result_setter = ResultSetter(dataframe_context)
    # scripts_to_run = dataframe_context.get_scripts_to_run()
    appid = dataframe_context.get_app_id()
    completionStatus = 0
    print "########################## Validate the Config ###############################"
    configValidator = ConfigValidator(dataframe_context)
    configValid = configValidator.get_sanity_check()
    print "#"*100
    print "analysistype",analysistype
    print "jobType",jobType
    print "configValid",configValid
    print "#"*100
    if not configValid:
        progressMessage = CommonUtils.create_progress_message_object("mAdvisor Job","custom","info","Please Provide a Valid Configuration",completionStatus,completionStatus,display=True)
        CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        response = CommonUtils.save_result_json(dataframe_context.get_job_url(),json.dumps({}))
        CommonUtils.save_error_messages(errorURL,APP_NAME,"Invalid Config Provided",ignore=ignoreMsg)
    else:
        ########################## Initializing messages ##############################
        if jobType == "story":
            if analysistype == "measure":
                progressMessage = CommonUtils.create_progress_message_object("Measure analysis","custom","info","Analyzing Target Variable",completionStatus,completionStatus,display=True)
            else:
                progressMessage = CommonUtils.create_progress_message_object("Dimension analysis","custom","info","Analyzing Target Variable",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg,emptyBin=True)
            dataframe_context.update_completion_status(completionStatus)
        elif jobType == "metaData":
            progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Preparing data for loading",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg,emptyBin=True)
            progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Initializing the loading process",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            progressMessage = CommonUtils.create_progress_message_object("metaData","custom","info","Data Upload in progress",completionStatus,completionStatus,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
            dataframe_context.update_completion_status(completionStatus)

        df = None
        data_loading_st = time.time()
        progressMessage = CommonUtils.create_progress_message_object("scriptInitialization","scriptInitialization","info","Loading the Dataset",completionStatus,completionStatus)
        if jobType != "story" and jobType != "metaData":
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg,emptyBin=True)
            dataframe_context.update_completion_status(completionStatus)
        ########################## Load the dataframe ##############################
        df = MasterHelper.load_dataset(spark,dataframe_context)
        if jobType != "metaData":
            metaParserInstance = MasterHelper.get_metadata(df,spark,dataframe_context)
            df,df_helper = MasterHelper.set_dataframe_helper(df,dataframe_context,metaParserInstance)
            # updating metaData for binned Cols
            colsToBin = df_helper.get_cols_to_bin()
            levelCountDict = df_helper.get_level_counts(colsToBin)
            metaParserInstance.update_level_counts(colsToBin,levelCountDict)

        ############################ MetaData Calculation ##########################

        if jobType == "metaData":
            MasterHelper.run_metadata(spark,df,dataframe_context)
        ############################################################################

        ################################ Data Sub Setting ##########################
        if jobType == "subSetting":
            MasterHelper.run_subsetting(spark,df,dataframe_context,df_helper)
        ############################################################################

        ################################ Story Creation ############################
        if jobType == "story":
            if analysistype == "dimension":
                MasterHelper.run_dimension_analysis(spark,df,dataframe_context,df_helper,metaParserInstance)
            elif analysistype == "measure":
                MasterHelper.run_measure_analysis(spark,df,dataframe_context,df_helper,metaParserInstance)

            progressMessage = CommonUtils.create_progress_message_object("final","final","info","Job Finished",100,100,display=True)
            CommonUtils.save_progress_message(messageURL,progressMessage,ignore=ignoreMsg)
        ############################################################################

        ################################ Model Training ############################
        elif jobType == 'training':
            MasterHelper.train_models(spark,df,dataframe_context,df_helper,metaParserInstance)
        ############################################################################

        ############################## Model Prediction ############################
        elif jobType == 'prediction':
            MasterHelper.score_model(spark,df,dataframe_context,df_helper,metaParserInstance)

        ############################################################################

        ################################### Stock ADVISOR ##########################
        if jobType == 'stockAdvisor':
            file_names = dataframe_context.get_stock_symbol_list()
            stockObj = StockAdvisor(spark, file_names,dataframe_context,result_setter)
            stockAdvisorData = stockObj.Run()
            stockAdvisorDataJson = CommonUtils.convert_python_object_to_json(stockAdvisorData)
            response = CommonUtils.save_result_json(configJson["job_config"]["job_url"],stockAdvisorDataJson)

        ############################################################################
        scriptEndTime = time.time()
        runtimeDict = {"startTime":scriptStartTime,"endTime":scriptEndTime}
        print runtimeDict
        CommonUtils.save_error_messages(errorURL,"jobRuntime",runtimeDict,ignore=ignoreMsg)
        print "Scripts Time : ", scriptEndTime - scriptStartTime, " seconds."
        #spark.stop()

def submit_job_through_yarn():
    print sys.argv
    print json.loads(sys.argv[1])
    json_config = json.loads(sys.argv[1])
    # json_config["config"] = ""

    main(json_config["job_config"])

if __name__ == '__main__':
    main(sys.argv[1])
    print 'Main Method End .....'
