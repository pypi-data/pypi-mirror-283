import panel as pn
import polars as pl
import pandas as pd
from datadashr.core.response_manager.base import ResponseFormatterBase
from io import StringIO
from datadashr.config import *


class PanelResponseFormatter(ResponseFormatterBase):
    def format(self):
        """
        Format the response for Panel
        :return:
        """
        logger.info(self.result)
        try:
            if isinstance(self.result, (pd.DataFrame, pl.DataFrame)):
                return pn.widgets.DataFrame(self.result)
            elif isinstance(self.result, dict):
                return self.generate_chart_from_response(self.result)
            elif self.result is not None:
                return pn.pane.Markdown(str(self.result))
            else:
                return pn.pane.Markdown("No result available.")
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return pn.pane.Markdown("Error formatting response.")

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

    def polars_chart(self, response):
        """
        Generate a chart from the response using polars
        :param response:
        :return:
        """
        try:
            data_type = type(response['data'])
            logger.info(f"Data type: {data_type}")

            logger.info(f"Response: {response}")



            # Caso in cui i dati sono forniti come una lista di dizionari
            if isinstance(response['data'], list):
                data = pl.DataFrame(response['data'])

            # Caso in cui è un dataframe
            elif isinstance(response['data'], pl.DataFrame):
                data = response['data']

            # Caso in cui i dati sono forniti come un dizionario con chiavi 'x' e 'y'
            elif isinstance(response['data'], dict) and isinstance(response['data']['x'], list) and isinstance(
                    response['data']['y'], list):
                data = pl.DataFrame({
                    response['x_label']: response['data']['x'],
                    response['y_label']: response['data']['y']
                })

            # Caso in cui i dati sono forniti come JSON
            elif isinstance(response['data'], str):
                data = pl.read_json(StringIO(response['data']))

            else:
                raise ValueError("Unsupported data format")

            # estrai i nomi delle colonne da data
            columns = data.columns

            # assegna i nomi delle colonne a x_label e y_label se sono diversi da quelli passati
            if response['x_label'] not in columns:
                response['x_label'] = columns[0]
            if response['y_label'] not in columns:
                response['y_label'] = columns[1]

            actual_x_label = response['x_label']
            actual_y_label = response['y_label']

            if response['chart_type'] == 'bar':
                echart_data = {
                    'title': {'text': 'Bar Chart'},
                    'tooltip': {
                        'trigger': 'axis',
                        'axisPointer': {'type': 'shadow'}
                    },
                    'legend': {'data': [actual_y_label]},
                    'xAxis': {
                        'type': 'category',
                        'data': data[actual_x_label].to_list()  # Convert to list for categorical axis
                    },
                    'yAxis': {},
                    'series': [{
                        'name': actual_y_label,
                        'type': 'bar',
                        'data': data[actual_y_label].to_list()
                    }]
                }
            elif response['chart_type'] == 'line':
                echart_data = {
                    'title': {'text': 'Line Chart'},
                    'tooltip': {},
                    'legend': {'data': [actual_y_label]},
                    'xAxis': {'data': data[actual_x_label].to_list()},
                    'yAxis': {},
                    'series': [{
                        'name': actual_y_label,
                        'type': 'line',
                        'data': data[actual_y_label].to_list()
                    }]
                }
            elif response['chart_type'] == 'histogram':
                # Creiamo l'istogramma manualmente
                if actual_x_label not in columns:
                    raise ValueError(f"Column '{actual_x_label}' not found in data")

                data_bins = data.select([
                    (pl.col(actual_x_label) // 10).alias('bin')  # Binning manuale
                ])
                histogram_data = data_bins.groupby('bin').count().sort('bin')
                histogram_data = histogram_data.with_columns([
                    (pl.col('bin') * 10).alias(actual_x_label)
                ])

                echart_data = {
                    'title': {'text': 'Histogram'},
                    'tooltip': {},
                    'legend': {'data': [actual_y_label]},
                    'xAxis': {
                        'type': 'category',  # Treat x-axis as categorical for histograms
                        'data': histogram_data[actual_x_label].to_list()  # Convert to list for categorical axis
                    },
                    'yAxis': {},
                    'series': [{
                        'name': actual_y_label,
                        'type': 'bar',
                        'data': histogram_data['count'].to_list()
                    }]
                }
            else:
                raise ValueError(f"Unsupported chart type: {response['chart_type']}")

            return pn.pane.ECharts(echart_data, height=480, width=640)

        except Exception as e:  # Cattura tutte le eccezioni
            logger.error(f"Error generating EChart: {e}")
            return pn.pane.Markdown(f"Error generating EChart: {e}")

    def pandas_chart(self, response):
        """
        Generate a chart from the response
        :param response:
        :return:
        """
        try:
            # Caso in cui i dati sono forniti come una lista di dizionari
            if isinstance(response['data'], list):
                data = pd.DataFrame(response['data'])

            # Caso in cui è un dataframe
            elif isinstance(response['data'], pd.DataFrame):
                data = response['data']

            # Caso in cui i dati sono forniti come un dizionario con chiavi 'x' e 'y'
            elif isinstance(response['data'], dict) and isinstance(response['data']['x'], list) and isinstance(
                    response['data']['y'], list):
                data = pd.DataFrame({
                    response['x_label']: response['data']['x'],
                    response['y_label']: response['data']['y']
                })
            else:
                # Caso in cui i dati sono forniti come JSON
                data = pd.read_json(StringIO(response['data']))

            # estrai i nomi delle colonne da data
            columns = data.columns.tolist()

            # assegna i nomi delle colonne a x_label e y_label se sono diversi da quelli passati
            if response['x_label'] not in columns:
                response['x_label'] = columns[0]
            if response['y_label'] not in columns:
                response['y_label'] = columns[1]

            actual_x_label = response['x_label']
            actual_y_label = response['y_label']

            if response['chart_type'] == 'bar':
                echart_data = {
                    'title': {'text': 'Bar Chart'},
                    'tooltip': {
                        'trigger': 'axis',
                        'axisPointer': {'type': 'shadow'}
                    },
                    'legend': {'data': [actual_y_label]},
                    'xAxis': {
                        'type': 'category',
                        'data': data[actual_x_label].astype(str).tolist()  # Convert to string for categorical axis
                    },
                    'yAxis': {},
                    'series': [{
                        'name': actual_y_label,
                        'type': 'bar',
                        'data': data[actual_y_label].tolist()
                    }]
                }
            elif response['chart_type'] == 'line':
                echart_data = {
                    'title': {'text': 'Line Chart'},
                    'tooltip': {},
                    'legend': {'data': [actual_y_label]},
                    'xAxis': {'data': data[actual_x_label].tolist()},
                    'yAxis': {},
                    'series': [{
                        'name': actual_y_label,
                        'type': 'line',
                        'data': data[actual_y_label].tolist()
                    }]
                }
            elif response['chart_type'] == 'histogram':
                counts, bins = pd.cut(data[actual_x_label], bins=10, retbins=True)
                histogram_data = pd.DataFrame({
                    actual_x_label: bins[:-1],
                    actual_y_label: counts.value_counts(sort=False)
                })
                echart_data = {
                    'title': {'text': 'Histogram'},
                    'tooltip': {},
                    'legend': {'data': [actual_y_label]},
                    'xAxis': {
                        'type': 'category',  # Treat x-axis as categorical for histograms
                        'data': histogram_data[actual_x_label].astype(str).tolist()
                        # Convert to string for categorical axis
                    },
                    'yAxis': {},
                    'series': [{
                        'name': actual_y_label,
                        'type': 'bar',
                        'data': histogram_data[actual_y_label].tolist()
                    }]
                }
            else:
                raise ValueError(f"Unsupported chart type: {response['chart_type']}")

            return pn.pane.ECharts(echart_data, height=480, width=640)

        except Exception as e:  # Cattura tutte le eccezioni
            logger.error(f"Error generating EChart: {e}")
            return pn.pane.Markdown(f"Error generating EChart: {e}")
