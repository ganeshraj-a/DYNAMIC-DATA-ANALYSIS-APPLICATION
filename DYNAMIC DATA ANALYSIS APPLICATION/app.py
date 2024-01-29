#---------------------------------libarys-------#
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import base64
# import weasyprint
# from streamlit_weasyprint import st_weasyprint
import seaborn as sns
from io import BytesIO
import matplotlib.pyplot as plt
import xlsxwriter
#-----------------------#
def home():
#-----------------------read file ------------------------------#
    uploaded_file = st.file_uploader("Choose a excel file", type='xlsx')
    # df = "ganesh"
    if uploaded_file:
        st.markdown('---')
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        st.markdown("<h1 style='text-align: center;'>Data preview</h1>", unsafe_allow_html=True)
        st.dataframe(df)
#-----------------------------------dimension------------------

        st.title("Number of row: "+str(df.shape[0]))
        st.title("Number of column: " + str(df.shape[1]))
#-----------------------------null------------------------#
        null_counts = df.isnull().sum()


    # Create a new data frame with column names and null counts
        null_df = pd.DataFrame({'Column Name': null_counts.index,
                            'Null Count': null_counts.values})
# ------------------------- data type ---------------
        data_types = df.dtypes

        dtype_df = pd.DataFrame({'Column Name': data_types.index,
                         'Data Type': data_types.values})
# ----------------columns for null and datatype dataframe ---------------
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h1 style='text-align: center;'>Data No of null values</h1>", unsafe_allow_html=True)
            st.write(null_df)
        with col2:
            st.markdown("<h1 style='text-align: center;'>Datatype of each column</h1>", unsafe_allow_html=True)
            st.write(dtype_df)

        st.sidebar.markdown("<h1 style='text-align: center;'>pivote table</h1>", unsafe_allow_html=True)
# ----------------------------pivote table ---------------------------#
        aggfun = ['sum','mean','median','min','max','count','std','var','first''last']

        dfindex = st.sidebar.multiselect("index", options=df.columns,default=df.columns[0])
        dfcolumn = st.sidebar.multiselect("column", options=df.columns,default=df.columns[1])
        value = st.sidebar.multiselect("value", options=df.columns,default=df.columns[2])
        aggfuntion = st.sidebar.multiselect("agg funtion", options=aggfun,default=aggfun[1])
        pivot_table = pd.pivot_table(df,index=dfindex, columns=dfcolumn, values=value, aggfunc=aggfuntion)

    # Display the pivot table
        st.markdown("<h1 style='text-align: center;'>pivote table</h1>", unsafe_allow_html=True)


        st.write(pivot_table)

# ------------------------------- visualizations ------------------------#
        visu_list = ['Line charts','Bar charts','Scatter plots','Area charts','Histograms','Pie charts','Box plots','Violin plots',
         ]

        visu_sele = st.multiselect('Select the visualizations', options=visu_list)
        for i in range(len(visu_sele)):
            if visu_sele[i] == 'Line charts':
                st.title("Line chart")

                x = st.selectbox('select x axis',options=list(df.columns))
                y = st.selectbox('select y axis',options=list(df.columns))

            # visu_data = df[selected_column]
                cross_tab = pd.crosstab(df[x],df[y])
                print(cross_tab)
                fig = px.line(cross_tab)
                st.write(fig)


            elif visu_sele[i] == 'Bar charts':
                st.title("bar chart")

            # create the dropdown menus for x and y-axis labels
                x_label = st.selectbox('Select x-axis label:', options=df.columns)
                y_label = st.selectbox('Select y-axis label:', options=df.columns)

                # if y_label.dtype.value == "int64":
                #     filter = df[sum(df[y_label])]

            # update the bar chart based on the selected labels
                st.bar_chart(df[[x_label, y_label]])

            elif visu_sele[i] == 'Scatter plots':
                st.title("Scatterplot")
                try:
                    x_values = st.selectbox('x axis',options=df.columns)
                    y_values = st.selectbox('y axis',options=df.columns)
                    plot = px.scatter(data_frame=df,x = x_values,y=y_values)
                    st.plotly_chart(plot)
                except Exception as e:
                    print(e)
            elif visu_sele[i] == 'Histograms':
                st.title("Histograms")
                try:
                    select_box = st.selectbox(label = "Feature", options = df.columns)
                    sns.distplot(df[select_box])
                    st.pyplot()
                except Exception as e:
                    print(e)
            elif visu_sele[i] == "Pie charts":
                st.title("Pie charts")
                try:
                    Values = st.selectbox(label="Value",options=df.columns)
                    category = st.selectbox(label="category",options=df.columns)
                    fig = px.pie(df, values=Values, names=category)

                    st.plotly_chart(fig)
                except Exception as e:
                    print(e)
            elif visu_sele[i] == "Area charts":
                st.title("Area charts")
                try:
                    x = st.selectbox(label="X",options=df.columns)
                    y = st.selectbox(label="Y",options=df.columns)
                    area_chart = alt.Chart(df).mark_area(
                        opacity=0.5,
                        color='blue'
                    ).encode(
                        x=x,
                        y=y
                    )

                    # Display the area chart in Streamlit
                    st.altair_chart(area_chart, use_container_width=True)
                except Exception as e:
                    print(e)
            elif visu_sele[i] == "Box plots":
                st.title("Box plots")
                try:
                    x = st.selectbox(label="boxX", options=df.columns)
                    y = st.selectbox(label="boxY", options=df.columns)

                    chart = alt.Chart(df).mark_boxplot().encode(
                        x=x,
                        y=y
                    )

                    # Display chart in Streamlit
                    st.altair_chart(chart, use_container_width=True)

                except Exception as e:
                    print(e)
            elif visu_sele[i] == "Violin plots":
                try:
                    x = st.selectbox(label="violine X",options=df.columns)
                    y = st.selectbox(label="violine Y",options=df.columns)
                    sns.violinplot(x=x, y=y, data=df)

                    # Show the plot
                    plt.show()

                except Exception as e:
                    print(e)



        st.title("describe Data")
        describ = st.multiselect("select the describe the columns",options=df.columns)
        c1, c2, c3 = st.columns(3)
        k = 1
        for i in range(len(describ)):
            if k == 1:
                with c1:
                    d = df[describ[i]].describe()
                    st.dataframe(d)
                k += 1
            elif k == 2:
                with c2:
                    d = df[describ[i]].describe()
                    st.dataframe(d)
                k += 1
            else:
                with c3:
                    d = df[describ[i]].describe()
                    st.dataframe(d)
                k = 1
        st.title("Data modification")
        rowlist = []
        colu_list = []
        valuelsit = []

        row = st.text_area(label='Enter multiple inputs, separated by a new line row')
        row_l = row.split('\n')
        col = st.text_area(label='Enter multiple inputs, separated by a new line col')
        col_l = col.split('\n')
        input_text = st.text_area(label='Enter multiple inputs, separated by a new line'
                                  )
        input_list = input_text.split('\n')
        for i in input_list:
            valuelsit.append(i)

        if st.button('Update'):
            for i in range(len(row_l)):
                df.iloc[int(row_l[i]), int(col_l[i])] = valuelsit[i]




    # Display the updated DataFrame
        st.write('Updated Dataset:')
        st.write(df)

        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="modified_dataset.csv">Download CSV</a>'

        st.markdown(href, unsafe_allow_html=True)
        return df
def about():
    st.title("About Page")
    st.write("This is the about page.")
    uploaded_file1 = st.file_uploader("Choose a excel file 1", type='xlsx')
    # df = "ganesh"
    if uploaded_file1:
        st.markdown('---')
        df = pd.read_excel(uploaded_file1, engine='openpyxl')

        sel_col = st.sidebar.multiselect(" select filter column ", options=df.columns)
        sele_df = st.dataframe(df[sel_col])
        st.write(sele_df)
        y = ['>=','<=','==','<','>','!=']
        #
        csv1 = sele_df.to_csv(index=False)
        b604 = base64.b64encode(csv1.encode()).decode()
        href1 = f'<a href="data:file/csv;base64,{b604}" download="modified_datase.csv">Download CSV</a>'
        st.markdown(href1, unsafe_allow_html=True)









#------------------------------------------------------------------------------------

















# def add(u,sele_df):
        #
        #     selected_col = st.sidebar.multiselect(" select filter column "+str(u),options=df.columns)
        #     condition = st.sidebar.multiselect("select filter condition"+str(u),options=y)
        #     value = st.sidebar.text_area(label='Enter the value'+str(u))
        #
        #     if condition[0] == '>=':
        #         st.title("filtered data")
        #         st.dataframe(sele_df[sele_df[selected_col[0]] >= int(value)])
        #     elif condition[0] == '<=':
        #         st.title("filtered data")
        #         st.dataframe(sele_df[sele_df[selected_col[0]] <= int(value)])
        #     elif condition[0] == '<':
        #         st.title("filtered data")
        #         st.dataframe(sele_df[sele_df[selected_col[0]] < int(value)])
        #     elif condition[0] == '>':
        #         st.title("filtered data")
        #         st.dataframe(sele_df[sele_df[selected_col[0]] > int(value)])
        #     elif condition[0] == '==':
        #         st.title("filtered data")
        #         st.dataframe(sele_df[sele_df[selected_col[0]] == int(value)])
        #     elif condition[0] == '!=':
        #         st.title("filtered data")
        #         st.dataframe(sele_df[sele_df[selected_col[0]] != int(value)])


        #     if len(selected_col)>0:
        #         add(u+1,sele_df)
        # add(0,sele_df)












