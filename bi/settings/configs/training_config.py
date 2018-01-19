def get_training_config():
    trainingConfig = {
      "config": {
        "COLUMN_SETTINGS": {
          "variableSelection": [
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "uid",
              "selected": True,
              "slug": "46ec8e7d3b3f43a4907cb7ba10e87215",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": True
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Month",
              "selected": False,
              "slug": "b501227d44a04f8ba03b56770b4acd5d",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": True,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Deal_Type",
              "selected": True,
              "slug": "81bf54cc137942cabf56c2aa0dbba528",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Price_Range",
              "selected": True,
              "slug": "74c836af52014f9d83e3d4326657add1",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Discount_Range",
              "selected": True,
              "slug": "984322638b154e7abdcbabf2c8871186",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Source",
              "selected": True,
              "slug": "2cc19c3b13e44206841d75deab962178",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Platform",
              "selected": True,
              "slug": "66f4f08701864877a1041393c78964e2",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": True,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Buyer_Age",
              "selected": True,
              "slug": "4cfea1a4dbc74f9daaf3ca34eac9043e",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Buyer_Gender",
              "selected": True,
              "slug": "59e9473ae53d4f0bb9daf25bcf27c2cc",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Tenure_in_Days",
              "selected": True,
              "slug": "4e1f9abaebb94022bf95ff49a26bf06a",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Sales",
              "selected": True,
              "slug": "be262c1a685c4e64b123f0c2fb04fe4a",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Marketing_Cost",
              "selected": True,
              "slug": "6b594d8804634495ac9799696a46c107",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Shipping_Cost",
              "selected": True,
              "slug": "b2b5e4231f164078be5a3170bae80bf3",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "measure",
              "name": "Last_Transaction",
              "selected": True,
              "slug": "74d5c13420464b03a67c5638f28d015b",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "datetime",
              "name": "new_date",
              "selected": True,
              "slug": "c2556ed2222341deb12012ed6e24b551",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": False,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "Order Date",
              "selected": False,
              "slug": "3ef2616ac7df4730b3a9001f4583a944",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": True,
              "targetColumn": False,
              "uidCol": False
            },
            {
              "polarity": None,
              "setVarAs": None,
              "columnType": "dimension",
              "name": "newCol",
              "selected": False,
              "slug": "584d980dd1b94ffa9dd7590bef9a44a6",
              "targetColSetVarAs": None,
              "dateSuggestionFlag": True,
              "targetColumn": False,
              "uidCol": False
            }
          ]
        },
        "DATA_SOURCE": {
          "datasource_type": "fileUpload",
          "datasource_details": ""
        },
        "FILE_SETTINGS": {
          "analysis_type": [
            "training"
          ],
          "modelpath": [
            "llllll-ui5h22aaz6"
          ],
          "train_test_split": [
            0.68
          ],
          "metadata": {
            "url": "34.196.204.54:9012/api/get_metadata_for_mlscripts/",
            "slug_list": [
              "ecommerce_uidcsv-afzlqzqiym"
            ]
          },
          "inputfile": [
            "file:///home/gulshan/marlabs/datasets/sampleDatasets/ecommerce_UID.csv"
          ]
        }
      },
     "job_config": {
        "message_url": "http://34.196.204.54:9012/api/messages/Job_model-llllll-ui5h22aaz6-med3jt1vtl_123/",
        "get_config": {
          "action": "get_config",
          "method": "GET"
        },
        "error_reporting_url": "http://34.196.204.54:9012/api/set_job_report/model-llllll-ui5h22aaz6-med3jt1vtl/",
        "set_result": {
          "action": "result",
          "method": "PUT"
        },
        "job_url": "http://34.196.204.54:9012/api/job/model-llllll-ui5h22aaz6-med3jt1vtl/",
        "job_type": "training",
        "job_name": "llllll",
        "xml_url": "http://34.196.204.54:9012/api/xml/model-llllll-ui5h22aaz6-med3jt1vtl/",
        "app_id": 2
      }
    }



    return trainingConfig