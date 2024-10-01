import pandas as pd
import plotly.express as px
import streamlit as st

# Set page configuration
st.set_page_config(page_title='Quantitative Insights Platform', page_icon='📈')

# Add custom CSS to enhance styling
st.markdown(
    """
    <style>
        .reportview-container {
            background: #F0F2F5;  /* Light background */
        }
        .sidebar .sidebar-content {
            background-color: transparent;  /* Make sidebar background transparent */
            color: #1E90FF;  /* Text color for sidebar */
        }
        .sidebar h1, .sidebar h2, .sidebar h3, .sidebar h4, .sidebar .stButton, .sidebar .stSelectbox {
            color: #1E90FF;  /* Set sidebar text color */
        }
        h1, h2, h3, h4 {
            color: #1E90FF;  /* Title color */
            margin: 0;  /* Remove margins from headings */
            padding-bottom: 8px;  /* Add slight padding below headings */
        }
        .stButton>button {
            background-color: #1E90FF;  /* Button color */
            color: white;  /* Button text color */
            margin: 5px 0;  /* Reduced margin for buttons */
            padding: 8px 12px;  /* Reduced padding for buttons */
            border-radius: 4px;  /* Rounded button corners */
        }
        .stButton>button:hover {
            background-color: #0056b3;  /* Button hover color */
        }
        .stSelectbox, .stMultiselect, .stSlider, .stTextInput, .stNumberInput {
            background-color: transparent;  /* Input fields background */
            border: 1px solid #E0E0E0;  /* Input fields border */
            margin: 5px 0;  /* Reduced margin for input fields */
            padding: 8px;  /* Padding for input fields */
            border-radius: 4px;  /* Rounded input field corners */
            color: #1E90FF;  /* Text color for input fields */
        }
        .stSelectbox:focus, .stMultiselect:focus, .stSlider:focus, .stTextInput:focus, .stNumberInput:focus {
            border-color: #1E90FF;  /* Focus border color */
        }
        .stExpander {
            margin: 5px 0;  /* Reduced margin for expanders */
        }
        .stTabs {
            margin: 5px 0;  /* Reduced margin for tabs */
        }
        /* Remove background from all visualization panels */
        .streamlit-expander, .streamlit-card {
            background-color: transparent;  /* Remove background color */
            border: none;  /* Remove border */
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Title of the page
st.title(':rainbow[Data Analytics Portal]')
st.subheader(':green[Explore the insights about your data]')
st.divider()

# File uploader for CSV and Excel
file = st.file_uploader('Drop CSV and Excel', type=['csv', 'xlsx'])

if file is not None:
    # Load data from the uploaded file
    if file.name.endswith('csv'):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)
    
    st.dataframe(data)
    st.info('File was uploaded successfully', icon='✅')
    
    # Basic information about the data
    st.subheader(':rainbow[Basic Information about the data]')
    tab_labels = ['Summary', 'Top and Bottom Rows', 'Data Type', 'Columns']
    tabs = st.tabs(tab_labels)

    with tabs[0]:
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.')
        st.subheader(':gray[Statistical Summary of the data]')
        st.dataframe(data.describe())
    
    with tabs[1]:
        st.subheader(':gray[Top Rows]')
        toprows = st.slider('Number of rows to display', 1, data.shape[0], key='topslider')
        st.dataframe(data.head(toprows))
        st.subheader(':gray[Bottom Rows]')
        bottomrows = st.slider('Number of rows to display', 1, data.shape[0], key='bottomslider')
        st.dataframe(data.tail(bottomrows))
        
    with tabs[2]:
        st.subheader(':gray[Data Types of the column]')
        st.dataframe(data.dtypes)

    with tabs[3]:
        st.subheader(':gray[Columns of the data]')
        st.dataframe(list(data.columns))

    # Value Count Section
    st.subheader(':rainbow[Column Values To Count]')
    st.divider()
    
    with st.expander('Value Count'):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose Column Name', options=list(data.columns))
        with col2:
            toprows_count = st.number_input('Choose the number of Top rows', min_value=1, step=1)

        count = st.button('Count')
        if count:
            # Get value counts and rename columns to 'index' and 'count'
            result = data[column].value_counts().reset_index().head(toprows_count)
            result.columns = ['index', 'count']  # Rename to 'index' and 'count'
            
            st.dataframe(result)
            st.subheader('Visualization of Data')

            # Create visualizations
            # Bar Chart
            fig_bar = px.bar(data_frame=result, x='index', y='count', 
                             labels={'index': column, 'count': 'Count'},
                             title=f"Top {toprows_count} Value Counts for {column}",
                             text='count',  # Display count on bars
                             color='count', color_continuous_scale='Blues')

            st.plotly_chart(fig_bar)
            
            # Line Chart
            fig_line = px.line(data_frame=result, x='index', y='count', 
                               labels={'index': column, 'count': 'Count'},
                               title=f"Line Chart of Top {toprows_count} Value Counts for {column}",
                               markers=True)  # Add markers for each point

            st.plotly_chart(fig_line)
            
            # Pie Chart
            fig_pie = px.pie(data_frame=result, names='index', values='count',
                             title=f"Pie Chart of Top {toprows_count} Value Counts for {column}",
                             color_discrete_sequence=px.colors.sequential.RdBu)
            
            fig_pie.update_traces(textinfo='percent+label')  # Show percentage and label
            st.plotly_chart(fig_pie)
    
    # Group by functionality
    with st.expander('Group by your columns'):
        col1, col2, col3 = st.columns(3)

        # Multiselect column(s) to group by
        with col1:
            groupby_columns = st.multiselect('Choose column(s) to group by', options=list(data.columns))

        # Choose a column for aggregation if groupby_columns is selected
        operation_col = None
        if groupby_columns:
            with col2:
                numeric_cols = data.select_dtypes(include=['number']).columns
                non_numeric_cols = data.select_dtypes(exclude=['number']).columns

                # Select operation column based on numeric or non-numeric
                if numeric_cols.size > 0:
                    operation_col = st.selectbox('Choose column for operation', options=numeric_cols)
                else:
                    operation_col = st.selectbox('Choose column for operation', options=non_numeric_cols)

            # Show only applicable operations for numeric or non-numeric columns
            with col3:
                operation = st.selectbox('Choose operation to perform', options=['sum', 'mean', 'median', 'max', 'min'] if operation_col in numeric_cols else ['mode'])

            # Perform group by operation and display the result
            if operation_col:
                if operation != 'mode':
                    groupby_result = data.groupby(groupby_columns)[operation_col].agg(operation).reset_index(name=operation_col)
                else:
                    # Handle mode separately because it may return multiple values
                    groupby_result = data.groupby(groupby_columns)[operation_col].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None).reset_index(name=operation_col)

                st.write(f"Result of {operation} operation on '{operation_col}' grouped by {groupby_columns}")
                st.dataframe(groupby_result)

                # Visualization Section
                st.sidebar.header('Data Visualization Options')

                # Summarize the groupby_result to provide users with an overview
                if not groupby_result.empty:
                    st.subheader('Grouped Data Summary')
                    st.write(groupby_result.describe(include='all'))

                    # Options for graph type selection
                    graphs = st.sidebar.selectbox('Choose Graph Visualization', options=['Line', 'Bar', 'Scatter', 'Pie', 'Sunburst'])

                    # Axis and color selections
                    x_axis = st.sidebar.selectbox('Choose X axis', options=list(groupby_result.columns))
                    y_axis = operation_col  # Use the operation column directly

                    # Color selection with a placeholder for no color
                    color = st.sidebar.selectbox('Choose Color', options=[None] + list(groupby_result.columns))

                    # Additional column selection for faceting
                    facet_col = st.sidebar.selectbox('Choose Additional Columns for Faceting', options=[None] + list(groupby_result.columns))

                    # Create visualization based on selected graph type
                    if graphs == 'Line':
                        fig = px.line(data_frame=groupby_result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, markers=True)
                        fig.update_layout(title=f'Line Chart of {y_axis} by {x_axis}', template='plotly_white')
                        st.plotly_chart(fig)

                    elif graphs == 'Bar':
                        fig = px.bar(data_frame=groupby_result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
                        fig.update_layout(title=f'Bar Chart of {y_axis} by {x_axis}', template='plotly_white')
                        st.plotly_chart(fig)

                    elif graphs == 'Scatter':
                        fig = px.scatter(data_frame=groupby_result, x=x_axis, y=y_axis, color=color, facet_col=facet_col)
                        fig.update_layout(title=f'Scatter Plot of {y_axis} by {x_axis}', template='plotly_white')
                        st.plotly_chart(fig)

                    elif graphs == 'Pie':
                        fig = px.pie(data_frame=groupby_result, names=x_axis, values=y_axis, title=f'Pie Chart of {y_axis}')
                        fig.update_layout(template='plotly_white')
                        st.plotly_chart(fig)

                    elif graphs == 'Sunburst':
                        path = st.sidebar.multiselect('Choose Path for Sunburst', options=list(groupby_result.columns))
                        if path:
                            fig = px.sunburst(data_frame=groupby_result, path=path, values=y_axis)
                            fig.update_layout(title=f'Sunburst Chart of {y_axis}')
                            st.plotly_chart(fig)
                        else:
                            st.warning("Please select at least one path for the sunburst chart.")

                else:
                    st.warning("The grouped result is empty. Please adjust your selections to generate data.")
