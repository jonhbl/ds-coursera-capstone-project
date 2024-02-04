# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()
site_dicts = [
    {"label": site, "value": site} for site in spacex_df["Launch Site"].unique()
]
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                *site_dicts,
            ],
            value="ALL",
            placeholder="Select a Launch Site",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=min_payload,
            max=max_payload,
            step=1000,
            marks={0: "0", max_payload: "100"},
            value=[min_payload, max_payload],
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        fig = px.pie(
            spacex_df,
            names="Launch Site",
            title="Success vs. Failed Launches for All Sites",
        )
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        fig = px.pie(
            filtered_df,
            names="class",
            title=f"Success vs. Failed Launches for {entered_site}",
        )

    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
    Input(component_id="payload-slider", component_property="value"),
)
def get_scatter_chart(entered_site, payload_range):
    print("Params: {} {}".format(entered_site, payload_range))
    if entered_site == "ALL":
        filtered_df = spacex_df[
            (spacex_df["Payload Mass (kg)"] >= int(payload_range[0]))
            & (spacex_df["Payload Mass (kg)"] <= int(payload_range[1]))
        ]
        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="All sites - payload mass between {:8,d}kg and {:8,d}kg".format(
                int(payload_range[0]), int(payload_range[1])
            ),
        )
    else:
        filtered_df = spacex_df[
            (spacex_df["Launch Site"] == entered_site)
            & (spacex_df["Payload Mass (kg)"] >= int(payload_range[0]))
            & (spacex_df["Payload Mass (kg)"] <= int(payload_range[1]))
        ]
        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Site {} - payload mass between {:8,d}kg and {:8,d}kg".format(
                entered_site, int(payload_range[0]), int(payload_range[1])
            ),
        )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server()
