## importing required packages
import os
import pandas as pd
import re

from flask import Flask, render_template, request, json

## pattern for escape characters
pattern = re.compile(r"\\n|\\r|\\t|\\r|\\f|\\b")
#pattern = re.compile(r"\s")


##  Global variable declariation
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = 'data'
XL_FILE = 'sample_data.xlsx'
CARRIER_COLUMN_NAME = 'Carrier_Name'
TG_COLUMN_NAME = 'TG_Name'
STATUS_COLUMN_NAME = 'Status'

## Initialize flask app 
app = Flask(__name__)


## main or index page routing function
@app.route("/")
def main():
    keyword = request.args.get('inputKeyword')
    if keyword:
        print("query param keyword: -->", keyword)
    return render_template('index.html')


## Serach call rounting function
@app.route('/search', methods=['POST'])
def search():
    # read the posted values from the UI
    keyword = request.form['inputKeyword']
    test_file_path = os.path.join(BASE_DIR, DATA_DIR, XL_FILE)

    sheet_to_df_dict = read_xls(test_file_path)
    InfoDF = pd.DataFrame()

    for sht, df in sheet_to_df_dict.items():
        car_df = df[(df[CARRIER_COLUMN_NAME].str.contains(str(keyword), case=False)) & (df[STATUS_COLUMN_NAME] == 'LIVE')]
        tg_df = df[(df[TG_COLUMN_NAME].str.contains(str(keyword), case=False)) & (df[STATUS_COLUMN_NAME] == 'LIVE')]
        tempDF = pd.concat([car_df, tg_df])

        InfoDF = pd.concat([InfoDF,tempDF])

    req_df = InfoDF #.iloc[:,0:7]
    #req_df.reset_index(drop=True, inplace=True)
    tables_html=[req_df.to_html(classes="table table-striped table-bordered search-data ", index=False, header="true")]

    #return json.dumps(req_df.to_dict('records'))

    if len(tables_html[0]) > 450 :
        search_result = remove_escape_characters(tables_html[0])

    else:
        search_result = '<h4> No result found.. </h4>'

    return (search_result)


## helping functions to remove escape characters
def remove_escape_characters(string):
    #processed_string = string.encode('ascii', 'ignore').decode('unicode_escape') if isinstance(string, str) else string
    processed_string = string

    cleaned_string = pattern.sub(", ", str(processed_string))
    return cleaned_string

## helping functions to remove excel file read
def read_xls(test_file):
    # df_one = pd.read_excel(test_file, sheet_name=None)
    # print(df_one.head())
    xls = pd.ExcelFile(test_file)
    all_sheet_names = xls.sheet_names

    ## to read all sheets to a map
    sheet_to_df_dict = {}
    for sheet_name in all_sheet_names:
        sheet_to_df_dict[sheet_name] = xls.parse(sheet_name)

    return sheet_to_df_dict


## main function
if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0', port=5555)

