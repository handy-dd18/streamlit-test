import streamlit as st
import pandas as pd
from sklearn import datasets

from bokeh.plotting import figure

from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models import DataTable, TableColumn, HTMLTemplateFormatter, NumberFormatter

from boxsdk import OAuth2, Client
from boxsdk.auth.jwt_auth import JWTAuth
import urllib.request
import requests

from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

config = JWTAuth.from_settings_file('<config.json>')

auth = OAuth2(
    client_id='<client_id>',
    client_secret='<client_secret>',
    access_token='<access_token>',
)
client = Client(auth)

# def load_data():
#     iris = datasets.load_iris()
#     df = pd.DataFrame(iris.data, columns=iris.feature_names)
#     df['target'] = iris.target_names[iris.target]
#     return df

# df = load_data()
df = pd.read_csv('./iris.csv')
# targets = list(df.target.unique())
# selected_targets = st.multiselect('select targets', targets, default=targets)
# df = df[df.target.isin(selected_targets)]

for index, data in df.iterrows():
    box_fileid=data['links'].split('/')[-1]
    download_url = client.file(box_fileid).get_download_url()
    df.loc[index, 'links'] = download_url

cds = ColumnDataSource(df)

columns = [
TableColumn(field="sepal.length", title="sepal.length", formatter=NumberFormatter(format="0.00")),
TableColumn(field="sepal.width", title="sepal.width", formatter=NumberFormatter(format="0.00")),
TableColumn(field="petal.length", title="petal.length", formatter=NumberFormatter(format="0.00")),
TableColumn(field="petal.width", title="petal.width", formatter=NumberFormatter(format="0.00")),
TableColumn(field="variety", title="variety"),
TableColumn(field="links", title="links", formatter=HTMLTemplateFormatter(template='<a href="<%= links %>"target="_blank">Box Link</a>')),
]
p = DataTable(source=cds, columns=columns, css_classes=["my_table"])

st.set_page_config(page_title="出力結果", layout="wide")
st.subheader('出力結果')
st.bokeh_chart(p)

# gd = GridOptionsBuilder.from_dataframe(df)
# gd.configure_selection(selection_mode='multiple', use_checkbox=True)
# gridoptions = gd.build()
# grid_table = AgGrid(df, height=250, gridOptions=gridoptions,
#                     update_mode=GridUpdateMode.SELECTION_CHANGED)
# st.write('## Selected')
# selected_row = grid_table["selected_rows"]
# st.dataframe(selected_row)

# st.dataframe(df.style.highlight_max(axis=0))

# df.hist()
# st.pyplot()