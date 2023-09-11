from shiny import App, ui, render
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def table(df):
    import plotly.graph_objs as go
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                align='left'),
    cells=dict(values=[df[i] for i in df.columns],           
                align='left'))
    ])
    return fig

intel = pd.read_csv("intel_new_table.csv", sep=",")

app_ui = ui.page_fluid(
    ui.row(ui.tags.h2("Python Shiny Dashboard ")),
    ui.row(
        ui.column(4,
                  ui.input_select(id="generation",
                                  label="Intel genration core",
                                  choices=list(
                                      intel["nGeneration"].unique()) + [""],
                                  selected=""
                                  )

                  ),

        ui.column(3,
                  ui.input_select(id="brand",
                                  label="Brande core",
                                  choices=list(
                                      intel["brand"].unique()) + [""],
                                  selected=""

                                  )
                  ),
        ui.column(3,
                  ui.input_slider("nbrCores", label="Number of cores", value=[
                                  4, 18], step=2, min=intel["nbr_cores"].min(), max=intel["nbr_cores"].max())
                  )

    ),
    ui.row(
        ui.output_plot("graphique_test")
    ),
    ui.row(
        ui.output_plot("table_gpu_intel"
                        )
    )
)


def server(input, output, session):

    @output
    @render.plot
    def table_gpu_intel():

        generation_values = [input.generation()] if input.generation(
        ) != "" else intel["nGeneration"].unique()
        brand_values = [input.brand()] if input.brand(
        ) != "" else intel["brand"].unique()
        nbr_cores_values = [input.nbrCores()] if input.nbrCores(
        ) != "" else intel["nbr_cores"].unique()

        generation_filter = intel["nGeneration"].isin(generation_values)
        brand_filter = intel["brand"].isin(brand_values)
        nbr_cores_filter = intel["nbr_cores"].isin(input.nbrCores())

        intel_filter = intel[generation_filter &
                             brand_filter & nbr_cores_filter]

        return render.DataTable(self, data=intel_filter, *, width='fit-content', height='500px', summary=True, filters=False, row_selection_mode='none')

    @output
    @render.plot
    def graphique_test():

        color = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99',
                 '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a']

        sns.set(style="whitegrid")

        fig, (ax1, ax2) = plt.subplots(nrows=1,
                                       ncols=2,
                                       figsize=(10, 6), 
                                       facecolor='lightskyblue',
                                       layout='constrained')

        sns.histplot(
            data=intel,
            x="brand",
            hue="nbr_cores",
            shrink=.6,
            multiple="stack",
            palette=color,
            legend=True,
            ax=ax1,
                    )

        ax1.set_xlabel("Brand")
        ax1.set_ylabel("Frequency")
        legend = ax1.get_legend()

        

        # Changer le titre de la légende
        legend.set_title("Number of Cores")

        fig.suptitle("Histogram of Branad by Number of Cores")

        return fig


app = App(ui=app_ui, server=server)
