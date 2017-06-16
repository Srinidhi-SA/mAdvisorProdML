
import json

from bi.algorithms import LinearRegression
from bi.algorithms import KmeansClustering
from bi.narratives.regression import RegressionNarrative
from bi.common import DataWriter
from bi.common import utils
from bi.narratives.regression import LinearRegressionNarrative


# from bi.stats import Correlation

class RegressionScript:
    def __init__(self, data_frame, df_helper, df_context, spark, correlations):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark
        self._correlations = correlations

    def Run(self):
        regression_result_obj = LinearRegression(self._data_frame, self._dataframe_helper, self._dataframe_context).fit(self._dataframe_context.get_result_column())
        regression_result = utils.as_dict(regression_result_obj)

        #print 'Regression result: %s' % (json.dumps(regression_result, indent=2))
        DataWriter.write_dict_as_json(self._spark, regression_result, self._dataframe_context.get_result_file()+'Regression/')



        # regression_narratives_obj = LinearRegressionNarrative(len(self._dataframe_helper.get_numeric_columns()),regression_result_obj, self._correlations,self._dataframe_helper)
        # regression_narratives = utils.as_dict(regression_narratives_obj)

        regression_narratives_obj = RegressionNarrative(self._dataframe_helper,self._dataframe_context,self._spark,regression_result_obj,self._correlations)
        regression_narratives = utils.as_dict(regression_narratives_obj.narratives)


        print 'Regression narratives:  %s' %(json.dumps(regression_narratives, indent=2))
        DataWriter.write_dict_as_json(self._spark, regression_narratives, self._dataframe_context.get_narratives_file()+'Regression/')
