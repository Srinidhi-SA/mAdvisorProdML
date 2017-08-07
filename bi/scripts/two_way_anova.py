import json

from bi.common import DataWriter
from bi.common import utils as CommonUtils
from bi.narratives.anova import AnovaNarratives
from bi.stats import TwoWayAnova


class TwoWayAnovaScript:
    def __init__(self, data_frame, df_helper, df_context, result_setter, spark):
        self._result_setter = result_setter
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context
        self._spark = spark

    def Run(self):
        df_anova_obj = TwoWayAnova(self._data_frame, self._dataframe_helper, self._dataframe_context).test_all(measure_columns=(self._dataframe_context.get_result_column(),))
        df_anova_result = CommonUtils.as_dict(df_anova_obj)
        # print 'RESULT: %s' % (json.dumps(df_anova_result, indent=2))

        anova_narratives_obj = AnovaNarratives(df_anova_obj,self._dataframe_helper,self._result_setter)
        anova_narratives = CommonUtils.as_dict(anova_narratives_obj)
        # print anova_narratives
        DataWriter.write_dict_as_json(self._spark, {'RESULT':json.dumps(df_anova_result['result'])}, self._dataframe_context.get_result_file()+'OneWayAnova/')
        DataWriter.write_dict_as_json(self._spark, {'narratives':json.dumps(anova_narratives['narratives'])}, self._dataframe_context.get_narratives_file()+'OneWayAnova/')
        #print "Narratives: %s" % (json.dumps(anova_narratives, indent=2))
