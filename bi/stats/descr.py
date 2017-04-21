from pyspark.sql import functions as FN

from bi.common.decorators import accepts
from bi.common import BIException
from bi.common import DataFrameHelper
from bi.common.results import MeasureDescriptiveStats
from bi.common.results import DimensionDescriptiveStats
from bi.common.results import DataFrameDescriptiveStats

from bi.transformations import Quantizer
from bi.transformations import Binner

from util import Stats


class DescriptiveStats:
    # collect freq stats for dimension column only if number of levels is less than MAX_NUM_LEVELS
    MAX_NUM_LEVELS = 100

    def __init__(self, data_frame, df_helper, df_context):
        self._data_frame = data_frame
        self._dataframe_helper = df_helper
        self._dataframe_context = df_context

    def stats(self):
        data_frame_descr_stats = DataFrameDescriptiveStats(num_columns=self._dataframe_helper.get_num_columns(),
                                                           num_rows=self._dataframe_helper.get_num_rows())
        for measure_column in self._dataframe_helper.get_numeric_columns():
            descr_stats = self.stats_for_measure_column(measure_column)
            data_frame_descr_stats.add_measure_stats(measure_column, descr_stats)

        for dimension_column in self._dataframe_helper.get_string_columns():
            descr_stats = self.stats_for_dimension_column(dimension_column)
            data_frame_descr_stats.add_dimension_stats(dimension_column, descr_stats)

        for time_dimension_column in self._dataframe_helper.get_timestamp_columns():
            data_frame_descr_stats.add_time_dimension_stats(time_dimension_column, {})

        return data_frame_descr_stats

    @accepts(object, basestring)
    def five_point_summary(self, measure_column):
        return Quantizer.quantize(self._data_frame, measure_column, self._dataframe_helper)

    @accepts(object, basestring)
    def stats_for_measure_column(self, measure_column):
        if not self._dataframe_helper.is_numeric_column(measure_column):
            raise BIException.non_numeric_column(measure_column)

        descr_stats = MeasureDescriptiveStats()

        num_values = self._data_frame.select(measure_column).count()
        min_value = Stats.min(self._data_frame, measure_column)
        max_value = Stats.max(self._data_frame, measure_column)
        total_value = Stats.total(self._data_frame, measure_column)
        mean = Stats.mean(self._data_frame, measure_column)
        variance = Stats.variance(self._data_frame, measure_column)
        std_dev = Stats.std_dev(self._data_frame, measure_column)
        if min_value==max_value:
            skewness = 0
            kurtosis = 0
        else:
            skewness = Stats.skew(self._data_frame, measure_column)
            kurtosis = Stats.kurtosis(self._data_frame, measure_column)
        descr_stats.set_summary_stats(num_values=num_values, min_value=min_value, max_value=max_value,
                                      total=total_value,
                                      mean=mean, variance=variance, std_dev=std_dev,
                                      skew=skewness, kurtosis=kurtosis)

        descr_stats.set_five_point_summary_stats(self.five_point_summary(measure_column))
        descr_stats.set_histogram(Binner(self._data_frame, self._dataframe_helper).get_bins(measure_column))

        #descr_stats.set_raw_data([float(row[0]) for row in self._data_frame.select(measure_column).collect()])
        return descr_stats

    @accepts(object, basestring)
    def stats_for_dimension_column(self, dimension_column):
        if not self._data_frame_helper.is_string_column(dimension_column):
            raise BIException.non_string_column(dimension_column)

        col_non_nulls = FN.count(dimension_column).alias('non_nulls')
        col_nulls = FN.sum(FN.col(dimension_column).isNull().cast('integer')).alias('nulls')
        aggregate_columns = (col_non_nulls, col_nulls)
        result = self._data_frame.select(*aggregate_columns).collect()[0].asDict()
        cardinality = self._data_frame.select(FN.col(dimension_column)).distinct().count()

        # TODO column value frequencies
        descr_stats = DimensionDescriptiveStats(num_null_values=result.get('nulls'),
                                                num_non_null_values=result.get('non_nulls'), cardinality=cardinality)

        if cardinality > DescriptiveStats.MAX_NUM_LEVELS:
            return descr_stats

        freq = {}
        level_and_counts = self._data_frame.groupBy(dimension_column).count().sort(FN.desc('count')).collect()
        for row in level_and_counts:
            freq[row[0]] = row[1]

        descr_stats.set_value_frequencies(freq)
        return descr_stats

    @accepts(object, basestring)
    def stats_for_time_dimension_column(self, time_dimension_column):
        pass
