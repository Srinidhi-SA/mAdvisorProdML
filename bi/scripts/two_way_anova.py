import json
from functools import reduce

from bi.common import utils
from bi.common import DataLoader
from bi.common import DataWriter
from bi.common import DataFrameHelper
from bi.common import BIException

from bi.stats.anova import TwoWayAnova
from bi.narratives.anova1 import AnovaNarratives

class TwoWayAnovaScript:
    def __init__(self, data_frame, df_helper, df_context, spark):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark

    def Run(self):
        df_anova_obj = TwoWayAnova(self._data_frame, self._dataframe_helper, self._dataframe_context).test_all(measure_columns=(self._dataframe_context.get_result_column(),))
        df_anova_result = utils.as_dict(df_anova_obj)
        print df_anova_result
        anova_narratives_obj = AnovaNarratives(df_anova_obj)
        anova_narratives = utils.as_dict(anova_narratives_obj)
        print anova_narratives
        DataWriter.write_dict_as_json(self._spark, {'ANOVA':json.dumps(df_anova_result)}, self._dataframe_context.get_result_file()+'TwoWayAnova/')
        DataWriter.write_dict_as_json(self._spark, anova_narratives, self._dataframe_context.get_narratives_file()+'TwoWayAnova/')
