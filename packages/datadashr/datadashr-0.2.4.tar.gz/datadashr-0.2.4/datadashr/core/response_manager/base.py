import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
import io
from PIL import Image
from datadashr.config import *


class ResponseFormatterBase:
    def __init__(self, result, full_code, connector_type, df_columns, query, chart_dir=CHART_DIR):
        self.result = result
        self.full_code = full_code
        self.connector_type = connector_type
        self.df_columns = df_columns
        self.query = query
        self.chart_dir = chart_dir

    def format(self):
        """
        Format the response
        :return:
        """
        raise NotImplementedError("Subclasses should implement this method")

    def generate_chart_from_response(self, response):
        """
        Select the right method to generate a chart from the response
        :param response:
        :return:
        """
        if self.connector_type == 'pandas':
            return self.pandas_chart(response)
        elif self.connector_type == 'polars':
            return self.polars_chart(response)
        else:
            return None

    def pandas_chart(self, response):
        """
        Generate a chart from the response
        :param response:
        :return:
        """
        try:
            if isinstance(response['data'], list):
                # Caso in cui i dati sono forniti come una lista di dizionari
                data = pd.DataFrame(response['data'])
            elif isinstance(response['data'], dict):
                # Caso in cui i dati sono forniti come un dizionario con chiavi 'x' e 'y'
                if isinstance(response['data']['x'], list) and isinstance(response['data']['y'], list):
                    data = pd.DataFrame({
                        response['x_label']: response['data']['x'],
                        response['y_label']: response['data']['y']
                    })
                else:
                    # Caso in cui i dati sono forniti come un dizionario con indici
                    data = pd.DataFrame(list(response['data'].items()),
                                        columns=[response['x_label'], response['y_label']])
            else:
                # Caso in cui i dati sono forniti come JSON
                data = pd.read_json(io.StringIO(response['data']))

            # Verifica che le colonne esistano
            if response['x_label'] not in data.columns or response['y_label'] not in data.columns:
                raise KeyError(f"Columns {response['x_label']} or {response['y_label']} not found in data")

            fig, ax = plt.subplots()

            if response["chart_type"] == "bar":
                ax.bar(data[response["x_label"]], data[response["y_label"]])
                ax.set_xlabel(response["x_label"])
                ax.set_ylabel(response["y_label"])
                for i in range(len(data)):
                    ax.text(i, data[response["y_label"]].iloc[i] / 2, f'{data[response["y_label"]].iloc[i]:.2f}',
                            ha='center', va='center')
            elif response["chart_type"] == "line":
                ax.plot(data[response["x_label"]], data[response["y_label"]])
                ax.set_xlabel(response["x_label"])
                ax.set_ylabel(response["y_label"])
            elif response["chart_type"] == "histogram":
                ax.hist(data[response["y_label"]], bins=10)
                ax.set_xlabel(response["y_label"])
                ax.set_ylabel('Frequency')
            else:
                ax.text(0.5, 0.5, 'No valid chart type specified', horizontalalignment='center',
                        verticalalignment='center')

            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img = Image.open(buf)

            if self.chart_dir:
                img.save(self.chart_dir)
                print(f"Image saved to {self.chart_dir}")

            return self.chart_dir or img
        except Exception as e:
            logger.error(f"Error generating chart: {e}")
            return None

    def polars_chart(self, response):
        """
        Generate a chart from the response
        :param response:
        :return:
        """
        try:
            # Convert the data to a Polars DataFrame
            data = pl.DataFrame(response['data'])

            logger.info(f"Data: {data}")

            # Ottieni il nome effettivo della colonna dopo l'aggregazione
            actual_x_label = data.columns[0]
            actual_y_label = data.columns[1]

            # Verifica che le colonne esistano
            if actual_x_label not in data.columns or actual_y_label not in data.columns:
                raise KeyError(f"Columns {actual_x_label} or {actual_y_label} not found in data")

            # Aggiorna le etichette nel dizionario di risposta
            response['x_label'] = actual_x_label
            response['y_label'] = actual_y_label

            fig, ax = plt.subplots()

            if response["chart_type"] == "bar":
                ax.bar(data[response['x_label']].to_list(), data[response['y_label']].to_list())
                ax.set_xlabel(response["x_label"])
                ax.set_ylabel(response["y_label"])
                for i, value in enumerate(data[response['y_label']]):
                    ax.text(i, value / 2, f'{value:.2f}', ha='center', va='center')
            elif response["chart_type"] == "line":
                ax.plot(data[response['x_label']].to_list(), data[response['y_label']].to_list())
                ax.set_xlabel(response["x_label"])
                ax.set_ylabel(response["y_label"])
            elif response["chart_type"] == "histogram":
                ax.hist(data[response['y_label']].to_list(), bins=10)
                ax.set_xlabel(response["y_label"])
                ax.set_ylabel('Frequency')
            else:
                ax.text(0.5, 0.5, 'No valid chart type specified', horizontalalignment='center',
                        verticalalignment='center')

            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            img = Image.open(buf)

            if self.chart_dir:
                img.save(self.chart_dir)
                print(f"Image saved to {self.chart_dir}")

            return self.chart_dir or img
        except Exception as e:
            logger.error(f"Error generating chart: {e}")
            return None

    def generate_echart_from_response(self, response):
        pass
