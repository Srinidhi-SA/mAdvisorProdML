import os
import jinja2
import re
import pattern.en
from bi.common.utils import accepts
from bi.common.results import ChiSquareResult
from bi.common.results import DFChiSquareResult
import operator
import numpy
import json
from chisquare import ChiSquareAnalysis


###
### TODO: complete rewrite recommended
###         Ram, 28/Jan/2017
###


class ChiSquareNarratives:
    @accepts(object, int, DFChiSquareResult)
    def __init__(self, num_dimension_columns, df_chisquare_result):
        self._num_dimension_columns = num_dimension_columns
        self._df_chisquare = df_chisquare_result
        self._df_chisquare_result = df_chisquare_result.get_result()
        self.narratives = {}
        # self._base_dir = os.path.dirname(os.path.realpath(__file__))+"/../../templates/chisquare/"
        self._base_dir = os.environ.get('MADVISOR_BI_HOME')+"/templates/chisquare/"
        self._generate_narratives()

    def _generate_narratives(self):
        for target_dimension in self._df_chisquare_result.keys():

            target_chisquare_result = self._df_chisquare_result[target_dimension]
            significant_variables = [dim for dim in target_chisquare_result.keys() if target_chisquare_result[dim].get_pvalue()<=0.05]
            #insignificant_variables = [i for i in self._df_chisquare_result[target_dimension] if i['pv']>0.05]
            num_analysed_variables = len(target_chisquare_result)
            num_significant_variables = len(significant_variables)
            self.narratives[target_dimension] = {}
            self.narratives[target_dimension]['heading'] = target_dimension + ' Performance Analysis'
            self.narratives[target_dimension]['sub_heading'] = "Relationship with other variables"
            data_dict = {
                          'num_variables' : num_analysed_variables,
                          'num_significant_variables' : num_significant_variables,
                          'significant_variables' : significant_variables,
                          'target_dimension' : target_dimension
            } # for both para 1 and para 2
            templateLoader = jinja2.FileSystemLoader( searchpath=self._base_dir)
            templateEnv = jinja2.Environment( loader=templateLoader )
            template = templateEnv.get_template('chisquare_template1.temp')
            summary1 = template.render(data_dict).replace("\n", "")
            summary1 = re.sub(' +',' ',summary1)
            templateLoader = jinja2.FileSystemLoader( searchpath=self._base_dir)
            templateEnv = jinja2.Environment( loader=templateLoader )
            template = templateEnv.get_template('chisquare_template2.temp')
            summary2 = template.render(data_dict).replace("\n", "")
            summary2 = re.sub(' +',' ',summary2)
            self.narratives[target_dimension]['summary'] = [summary1,summary2]

            for analysed_dimension in significant_variables:
                chisquare_result = self._df_chisquare.get_chisquare_result(target_dimension,analysed_dimension)
                self.narratives[target_dimension][analysed_dimension] = ChiSquareAnalysis(chisquare_result, target_dimension, analysed_dimension, significant_variables, num_analysed_variables)
