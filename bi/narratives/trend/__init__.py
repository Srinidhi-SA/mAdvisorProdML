import json
import os

from datetime import datetime
from dateutil.relativedelta import relativedelta

from bi.narratives import utils as NarrativesUtils
from trend_narratives import TrendNarrative

from pyspark.sql.functions import col, udf
from pyspark.sql.types import *



class TimeSeriesNarrative:
    def __init__(self, df_helper, df_context, result_setter, spark):
        self._result_setter = result_setter
        self._dataframe_helper = df_helper
        self._data_frame = df_helper.get_data_frame()
        self._spark = spark
        self._dataframe_context = df_context

        self._dateFormatDetected = False
        self._date_suggestion_columns = df_context.get_date_column_suggestions()
        self._dateFormatConversionDict = NarrativesUtils.date_formats_mapping_dict()
        self._td_columns = df_helper.get_timestamp_columns()

        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/trend/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/trend/"
        self.narratives = {"SectionHeading":"",
                           "card1":{},
                           "card2":{},
                           "card3":{}
                        }
        month_dict = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}


        measure_column = df_context.get_result_column()

        if self._date_suggestion_columns != None:
            time_dimension_column = self._date_suggestion_columns[0]
            existingDateFormat = None
            dateColumnFormatDict =  df_helper.get_datetime_format(time_dimension_column)
            if time_dimension_column in dateColumnFormatDict:
                existingDateFormat = dateColumnFormatDict[time_dimension_column]
                self._dateFormatDetected = True
            if df_context.get_requested_date_format() != None:
                requestedDateFormat = df_context.get_requested_date_format()[0]
            else:
                requestedDateFormat = None
            if requestedDateFormat != None:
                requestedDateFormat = self._dateFormatConversionDict[requestedDateFormat]
            else:
                requestedDateFormat = existingDateFormat

        if self._date_suggestion_columns != None:
            if self._dateFormatDetected:

                string_to_date = udf(lambda x: datetime.strptime(x,existingDateFormat), DateType())
                def get_year_month_from_date(x):
                    dt_obj = datetime.strptime(x,existingDateFormat)
                    out = dt_obj.strftime("%b-%y")
                    return out
                date_to_month_year = udf(get_year_month_from_date, StringType())
                self._data_frame = self._data_frame.withColumn("suggestedDate", string_to_date(time_dimension_column))
                self._data_frame = self._data_frame.withColumn("year_month", date_to_month_year(time_dimension_column))

                grouped_data = self._data_frame .groupBy("suggestedDate").agg({ measure_column : 'sum'})
                grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[-1],"value")
                grouped_data = grouped_data.withColumn("year_month",udf(lambda x:x.strftime("%b-%y"))("suggestedDate"))
                grouped_data = grouped_data.orderBy("suggestedDate",ascending=True)
                grouped_data = grouped_data.withColumnRenamed(grouped_data.columns[0],"key")
                grouped_data = grouped_data.toPandas()

                pandasDf = self._data_frame.toPandas()
                pandasDf.drop(time_dimension_column,axis=1,inplace=True)
                pandasDf.rename(columns={'year_month': time_dimension_column}, inplace=True)


                # pandasDf = df_helper.get_data_frame().toPandas()
                # pandasDf[time_dimension_column] = pandasDf[time_dimension_column].apply(lambda x:datetime.strptime(x,existingDateFormat))
                # pandasDf[time_dimension_column] = pandasDf[time_dimension_column].apply(lambda x: month_dict[x.month]+"-"+str(x.year))

                # grouped_data = df_helper.get_aggregate_data(time_dimension_column,measure_column,
                #                                                 existingDateFormat=existingDateFormat,
                #                                                 requestedDateFormat=requestedDateFormat)
                significant_dimensions = df_helper.get_significant_dimension()
                trend_narrative_obj = TrendNarrative(measure_column,time_dimension_column,grouped_data,existingDateFormat,requestedDateFormat)
                # grouped_data = trend_narrative_obj.formatDateColumn(grouped_data,requestedDateFormat)
                # grouped_data = grouped_data.sort_values(by='key', ascending=True)
                # grouped_data["value"] = grouped_data["value"].apply(lambda x: round(x,2))
                dataDict = trend_narrative_obj.generateDataDict(grouped_data)
                # # update reference time with max value
                reference_time = dataDict["reference_time"]
                if len(significant_dimensions.keys()) > 0:
                    xtraData = trend_narrative_obj.get_xtra_calculations(pandasDf,significant_dimensions.keys(),time_dimension_column,measure_column,existingDateFormat,reference_time)
                    if xtraData != None:
                        dataDict.update(xtraData)
                # print 'Trend dataDict:  %s' %(json.dumps(dataDict, indent=2))
                self._result_setter.update_executive_summary_data(dataDict)
                self.narratives["SectionHeading"] = measure_column+" Performance Report"
                summary1 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                'trend_narrative_card1.temp',dataDict)
                summary2 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                'trend_narrative_card2.temp',dataDict)

                self.narratives["card1"]["paragraphs"] = NarrativesUtils.paragraph_splitter(summary1)
                self.narratives["card1"]["bubbleData"] = dataDict["bubbleData"]
                self.narratives["card1"]["chart"] = ""
                self.narratives["card2"]["paragraphs"] = NarrativesUtils.paragraph_splitter(summary2)
                self.narratives["card2"]["table1"] = dataDict["table_data"]["increase"]
                self.narratives["card2"]["table2"] = dataDict["table_data"]["decrease"]

                # grouped_data["key"] = grouped_data["key"].apply(lambda x: month_dict[x.month]+"-"+str(x.year))
                # trend_chart_data = grouped_data[["key","value"]].groupby("key").agg(sum).reset_index()
                trend_chart_data = grouped_data[["key","value"]].T.to_dict().values()
                trend_chart_data = sorted(trend_chart_data,key=lambda x:x["key"])
                card1chartdata = trend_chart_data
                card1chartdata = [{"key":val["key"].strftime("%b-%y"),"value":val["value"]} for val in card1chartdata]
                self.narratives["card1"]["chart"] = {"data":card1chartdata,"format":"%b-%y"}

                if dataDict["dateRange"]<365:
                    prediction_window = 3
                else:
                    prediction_window = 6
                predicted_values = trend_narrative_obj.get_forecast_values(grouped_data["value"],prediction_window)[len(grouped_data["value"]):]
                predicted_values = [round(x,2) for x in predicted_values]

                prediction_data = [{"key":x["key"],"value":x["value"]} for x in trend_chart_data]
                prediction_data[-1]["predicted_value"] = prediction_data[-1]["value"]
                for val in range(prediction_window):
                    dataLevel = dataDict["dataLevel"]
                    if dataLevel == "month":
                        last_key = prediction_data[-1]["key"]
                        key = last_key+relativedelta(months=1)
                        prediction_data.append({"key":key,"predicted_value":predicted_values[val]})

                prediction_data = [val.update({"key":val["key"].strftime("%b-%y")}) for val in prediction_data ]
                forecastDataDict = {"startForecast":predicted_values[0],
                                    "endForecast":predicted_values[prediction_window-1],
                                    "measure":dataDict["measure"],
                                    "forecast":True,
                                    "forecast_percentage": round((predicted_values[prediction_window-1]-predicted_values[0])/predicted_values[0],2),
                                    "prediction_window_text": str(prediction_window) + " months"
                                    }

                self._result_setter.update_executive_summary_data(forecastDataDict)
                summary3 = NarrativesUtils.get_template_output(self._base_dir,\
                                                                'trend_narrative_card3.temp',forecastDataDict)
                self.narratives["card3"]["paragraphs"] = NarrativesUtils.paragraph_splitter(summary3)
                self.narratives["card3"]["chart"] = {"data":prediction_data,"format":"%b-%y"}
            else:
                self._result_setter.update_executive_summary_data({"trend_present":False})
                print "Trend Analysis Failed"
                print "#"*20+"Trend Analysis Error"+"#"*20
                print "No date format for the date column %s was detected." %(time_dimension_column)
                print "#"*60
        else:
            self._result_setter.update_executive_summary_data({"trend_present":False})
            print "Trend Analysis Failed"
            print "#"*20+"Trend Analysis Error"+"#"*20
            print "No date column present for Trend Analysis."
            print "#"*60





__all__ = [
    'TrendNarrative'
]
