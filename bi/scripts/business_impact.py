import time, json, re, sys
from bi.common import utils as CommonUtils
from bi.common import NormalCard, NarrativesTree, HtmlData, C3ChartData, TableData, ModelSummary,PopupData,NormalCard,ParallelCoordinateData,DataBox,WordCloud

class BusinessCard:
    """
    Functionalities
    """
    def __init__(self, business_impact_nodes, story_result, meta_parser, result_setter, dataframe_context, dataframe_helper, start_time):
        self._business_impact_nodes = business_impact_nodes
        self._story_result = story_result
        self._meta_parser = meta_parser
        self._result_setter = result_setter
        self._dataframe_context = dataframe_context
        self._dataframe_helper = dataframe_helper
        self.subheader = "Business Impact"
        self.business_card1 = NormalCard()
        self.business_card1.set_card_name("Overview")
        self.businessCardData = []
        self.start_time = start_time

    def set_params(self):
        self.target_levels = self._dataframe_helper.get_num_unique_values(self._dataframe_context.get_result_column())
        self.number_variables = self.get_number_variables()
        self.number_measures = self.get_number_measures()
        self.number_dimensions = self.get_number_dimensions()
        self.analysis_list = ["overview_rules","association_summary","association_rules","prediction_rules"]
        self.data_points = self.get_number_data_points()
        self.number_charts = self.get_number_charts()
        self.number_prediction_rules = self.get_number_prediction_rules()
        self.number_pages = self.get_number_pages()
        self.number_analysis = self.get_number_analysis()
        self.number_queries = self.get_number_queries()
        self.time_mAdvisor = time.time() - self.start_time
        self.time_analyst = self.get_time_analyst()
        self.time_saved = self.get_time_saved()
        self.impact_on_productivity = self.get_impact_on_productivity()

    def get_number_charts(self):
        return json.dumps(self._story_result,indent=2).count("c3Chart")

    def get_number_analysis(self):
        significant_variables_levels = {"None" : 0}
        for each in self._story_result['listOfNodes']:
            if each['name'] == 'Key Drivers':
                for node in each['listOfNodes']:
                    significant_variables_levels[node['name']] = [self._meta_parser.get_num_unique_values(node['name']) if node['name'] in self._dataframe_helper.get_string_columns() else 5][0]

        self.number_analysis_dict = {}
        self.number_analysis_dict["overview_rules"] = self.target_levels*2
        self.number_analysis_dict['association_summary'] = (self.number_dimensions+self.number_measures)*2
        self.number_analysis_dict["association_rules"] = sum(significant_variables_levels.values())*6
        self.number_analysis_dict["prediction_rules"] = self.number_prediction_rules*5
        return sum(self.number_analysis_dict.values())

    def get_number_queries(self):
        queries_per_analysis_dict = {"overview_rules" : 15, "association_summary" : 120, "association_rules" : 600, "prediction_rules" : 200}
        sum = 0
        for analysis in self.analysis_list:
            sum += self.number_analysis_dict[analysis]*queries_per_analysis_dict[analysis]
        return sum

    def get_number_prediction_rules(self):
        num_prediction_rules = 0
        for each_node in self._story_result['listOfNodes']:
            if each_node['name'] == 'Prediction':
                for card in each_node['listOfCards'][0]['cardData']:
                    if card['dataType'] == 'table':
                        num_prediction_rules = len(card['data']['tableData'])
        return num_prediction_rules

    def get_number_pages(self):
        sum = 0
        for each in self._story_result['listOfNodes']:
            if each['listOfNodes']:
                for items in each['listOfNodes']:
                    sum += len(items['listOfCards'])
                sum += len(each['listOfCards'])
            else:
                sum += len(each['listOfCards'])
        return sum

    def get_number_data_points(self):
        return self._meta_parser.get_num_rows()*self._meta_parser.get_num_columns()

    def get_number_variables(self):
        return self._meta_parser.get_num_columns()

    def get_number_dimensions(self):
        self.number_dimensions = len(self._dataframe_helper.get_string_columns())
        return self.number_dimensions

    def get_number_measures(self):
        self.number_measures = len(self._dataframe_helper.get_numeric_columns())
        return self.number_measures

    def get_time_analyst(self):
        time_per_analysis_dict = {"overview_rules" : 10, "association_summary" : 120, "association_rules" : 180, "prediction_rules" : 300}
        sum = 0
        for analysis in self.analysis_list:
            sum += self.number_analysis_dict[analysis]*time_per_analysis_dict[analysis]
        return sum

    def get_time_saved(self):
        '''
        Total Time Saved - 21 Hrs ( Productitvity Gain = Time taken by data scientist - time taken by mAdvisor)
        '''
        return self.time_analyst - self.time_mAdvisor

    def get_impact_on_productivity(self):
        '''
        Impact on Productivity - 3.5 X  ( Impact on Productivity = Time taken by data scientist / time taken by mAdvisor)
        '''
        productivity = str(round(self.time_analyst/self.time_mAdvisor,1)) + "X"
        return productivity

    def get_summary_data(self):
        summaryData = [
            {
              "name":"Total Data Points",
              "value":str(self.data_points)
            },
            {
              "name": "Number of Queries",
              "value": str(self.number_queries)
            },
            {
              "name": "Number of Analysis",
              "value": str(self.number_analysis)
            },
            {
              "name": "Total Pages",
              "value": str(self.number_pages)
            },
            {
              "name": "Total Time Saved",
              "value": CommonUtils.humanize_time(self.time_saved)
            },
            {
              "name": "Impact on Productivity",
              "value": str(self.impact_on_productivity)
            }
        ]
        # summaryData = HtmlData(data="<p> Hello World!!! </p>")
        summaryDataClass = DataBox(data=summaryData)
        self.businessCardData.append(summaryDataClass)
        # businessCardData.append(summaryData)
        # self.business_card1.set_card_data(self.businessCardData)
        # self._businessImpactNode.add_a_card(self.business_card1)

    def get_summary_para(self):
        para = """<blockquote><p>
        <b>Great Job !!!</b>mAdvisor has analysed the dataset that contains {} variables ({} dimensions and {} measures) and executed about <b>{}</b> queries for <b>{}</b> analysis. This would have taken an estimated average of <b>{}</b> for a data analyst to come up with a similar analysis.
        </p></blockquote>
        """.format(self.number_variables, self.number_dimensions, self.number_measures, self.number_queries, self.number_analysis, CommonUtils.humanize_time(self.time_analyst))
        paraDataClass = HtmlData(data=para)
        self.businessCardData.append(paraDataClass)

    def get_image_data(self):
        para = """<div class="col-md-6">

                              <img src="images/icon_dataAnalyst.png" class="pull-left" />

                              <h1 class="pull-left xs-mt-40 xs-ml-10"><small>Data Analyst <img src="images/icon_bAClock.png" class="xs-ml-10" /></small><br>

                                 <small>{}</small>

                              </h1>

                           </div>

                           <div class="col-md-6">

                              <img src="images/icon_bAmAdvisor.png" class="pull-left" />

                              <h1 class="pull-left xs-mt-40 xs-ml-10 text-primary"> <img src="images/icon_bAClock.png" /><br>

                                 <small>{}</small>

                              </h1>

                           </div>
           """.format(CommonUtils.humanize_time(self.time_analyst), CommonUtils.humanize_time(self.time_mAdvisor))
        paraDataClass = HtmlData(data=para)
        self.businessCardData.append(paraDataClass)

    def Run(self):
        print "In Run of BusinessCard"
        self._businessImpactNode = NarrativesTree()
        self._businessImpactNode.set_name("Business Impact")

        self.set_params()

        summary = self.get_summary_data()
        image_data = self.get_image_data()
        summary_para = self.get_summary_para()

        self.business_card1.set_card_data(self.businessCardData)
        self._businessImpactNode.add_a_card(self.business_card1)
        self._result_setter.set_business_impact_node(self._businessImpactNode)
