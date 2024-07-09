import panel as pn
import subprocess
import ollama
import webbrowser
import polars as pl
import uuid
import json
import pandas as pd
from datadashr import DataDashr
from datadashr.config import *
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from bokeh.models.widgets.tables import NumberFormatter, BooleanFormatter, HTMLTemplateFormatter

# Theme configuration
pn.config.theme = 'default'
pn.extension('echarts', 'tabulator')


class App:
    def __init__(self):
        self.allowed_models = ['codestral', 'mixtral']
        self.available_models = []

        self.llm_selector = pn.widgets.Select(name='Select LLM', options=self.available_models, value=None)
        self.cache_switch = pn.widgets.Switch(name='Enable Cache', value=True)
        self.verbose_switch = pn.widgets.Switch(name='Enable Verbose', value=False)
        self.file_input = pn.widgets.FileInput(name='Upload CSV', accept='.csv')
        self.cache_label = pn.pane.Str('Enable Cache')
        self.verbose_label = pn.pane.Str('Enable Verbose')
        self.chat_interface = pn.chat.ChatInterface(callback=self.generate_response, styles={'width': '100%'})

        self.df = None

        self.initialize_app()

    def initialize_app(self):
        if not self.verify_if_ollama_server_is_running() or not self.check_ollama_list():
            logger.error("Ollama server is not available. Please check the installation.")
            exit()

        self.available_models = self.check_accepted_models()
        if not self.available_models:
            logger.error("None of the accepted models are available.")
            exit()

        self.llm_selector.options = self.available_models
        self.llm_selector.value = self.available_models[0] if self.available_models else None

        self.setup_ui()
        self.setup_watchers()

        self.chat_interface.send("Hi! How can I help you?", user="Datadashr",
                                 avatar='https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.png',
                                 respond=False)

    def get_allama_llm_list(self):
        models = ollama.list()
        return [model['name'] for model in models['models']]

    def verify_if_ollama_server_is_running(self):
        try:
            models = ollama.list()
            return True
        except Exception as e:
            logger.error(f"Ollama server is not running: {e}")
            return False

    def check_ollama_list(self):
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
            if result.stdout:
                return True
            logger.error("Ollama server is not running")
            webbrowser.open('https://ollama.com/download')
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Error checking ollama list: {e}")
            return False

    def check_accepted_models(self):
        models = self.get_allama_llm_list()
        if not models:
            logger.error("Nessun modello disponibile.")
            return []

        available_models = []
        logger.info(f"Models: {models}")

        # Normalizzo i nomi dei modelli disponibili rimuovendo tutto dopo il primo `:`
        normalized_models = {}
        for model in models:
            prefix = model.split(':')[0]
            if prefix not in normalized_models:
                normalized_models[prefix] = []
            normalized_models[prefix].append(model)

        for model in self.allowed_models:
            if model in normalized_models:
                available_models.extend(normalized_models[model])

        if not available_models:
            logger.error("Nessuno dei modelli accettati è disponibile.")
            return []

        return available_models

    def setup_ui(self):
        self.box_file = pn.WidgetBox('# Choose file', self.file_input, width=350, styles={'margin-bottom': '10px'})
        self.box_llm = pn.WidgetBox('# Choose LLM', self.llm_selector, width=350, styles={'margin-bottom': '10px'})
        self.box_switch = pn.WidgetBox('# Settings', self.cache_label, self.cache_switch, self.verbose_label,
                                       self.verbose_switch, width=350,
                                       styles={'margin-bottom': '10px'})

    def setup_watchers(self):
        self.llm_selector.param.watch(self.update_datadashr, 'value')
        self.cache_switch.param.watch(self.update_datadashr, 'value')
        self.verbose_switch.param.watch(self.update_datadashr, 'value')
        self.file_input.param.watch(self.update_datadashr, 'value')

    def update_datadashr(self, event=None):
        selected_llm = self.llm_selector.value
        enable_cache = self.cache_switch.value
        enable_verbose = self.verbose_switch.value

        if not self.file_input.value:
            logger.error("File CSV non caricato. Carica un file per continuare.")
            self.chat_interface.send("Please upload a CSV file to proceed.", user="Datadashr",
                                     avatar='https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.png',
                                     respond=False)
            return

        # generate random file name to avoid conflicts
        file_name = f"{uuid.uuid4()}.csv"
        file_path = os.path.join(CSV_DIR, file_name)

        # create the file and write the content of the file input
        with open(file_path, 'wb') as f:
            f.write(self.file_input.value)

        import_data = {
            'sources': [
                {
                    "source_name": "uploaded_csv",
                    "file_path": file_path,
                    "source_type": "csv",
                    "description": "Uploaded CSV file for analysis.",
                },
            ],
        }

        llm = OllamaLLM(model=selected_llm, params={"temperature": 0.0}, verbose=enable_verbose)

        self.df = DataDashr(
            data=import_data,
            llm_instance=llm,
            verbose=enable_verbose,
            enable_cache=enable_cache,
            format_type='panel',
            reset_db=True,
        )

        try:
            self.df.df = pl.read_csv(file_path)
        except Exception as e:
            logger.error(f"Error {e} decoding the CSV file. Try loading a file with a different encoding.")
            self.chat_interface.send("Error decoding the CSV file. Please upload a file with a different encoding.",
                                     user="Datadashr",
                                     avatar='https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.png',
                                     respond=False)
            return

    def generate_echarts(self, data, title='Chart'):
        if not data:
            return pn.pane.Markdown("No data available for chart.")

        # logger.info(f"Data: {data}")

        # Check if data is a list of dictionaries
        if isinstance(data, dict):
            data = [data]

        # Dynamically determine column names
        columns = list(data[0].keys())
        if len(columns) < 2:
            return pn.pane.Markdown("Insufficient data for chart.")

        x_column, y_column = columns[:2]

        x_data = [str(entry[x_column]) for entry in data]
        y_data = [entry[y_column] for entry in data]

        echart_bar = {
            'title': {'text': title},
            'tooltip': {},
            'legend': {'data': [y_column]},
            'xAxis': {'data': x_data},
            'yAxis': {},
            'series': [{
                'name': y_column,
                'type': 'bar',
                'data': y_data
            }],
        }
        return pn.pane.ECharts(echart_bar, height=480, width=640)

    def generate_tabulator(self, data):
        formatted_data = [self.normalize_data(row) for row in data]

        # Convert the data to a DataFrame
        df = pd.DataFrame(formatted_data)

        # count the number of rows
        row_count = len(df)

        if row_count == 0:
            return pn.pane.Markdown("No data available for table.")

        # count the number of columns
        column_count = len(df.columns)

        if column_count == 0:
            return pn.pane.Markdown("No columns available for table.")

        if row_count == 1 and column_count == 1:
            return pn.pane.Markdown(f"## {str(df.iloc[0, 0])}                        ")


        # Automatically identify image fields and set formatters
        tabulator_formatters = {}
        bokeh_formatters = {}
        excluded_columns = []
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, str) and self.is_image_url(x)).any():
                tabulator_formatters[col] = {'type': 'image', 'height': '200px'}
                excluded_columns.append(col)
            elif df[col].apply(lambda x: isinstance(x, str) and self.is_valid_url(x)).any():
                bokeh_formatters[col] = HTMLTemplateFormatter(
                    template='<a href="<%= value %>" target="_blank">LINK</a>')
                excluded_columns.append(col)

        # Define column filters
        column_filters = {col: {'type': 'input', 'func': 'like', 'placeholder': f'Enter {col}'} for col in df.columns if
                          col not in excluded_columns and col not in ['index', 'id']}

        return (
            pn.widgets.Tabulator(
                df,
                pagination='remote',
                page_size=10,
                layout='fit_data_table',
                formatters=tabulator_formatters | bokeh_formatters,
                show_index=False,
                header_filters=column_filters,
            )
            if row_count > 10
            else pn.widgets.Tabulator(
                df,
                layout='fit_data_table',
                formatters=tabulator_formatters | bokeh_formatters,
                show_index=False,
            )
        )

    def normalize_data(self, row):
        formatted_row = {}
        for key, value in row.items():
            if isinstance(value, str):
                try:
                    date_value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                    formatted_row[key] = date_value.strftime('%Y-%m-%d')
                except ValueError:
                    formatted_row[key] = value  # Keep the URL as is for the image or link
            else:
                formatted_row[key] = value
        return formatted_row

    def is_image_url(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        return any(path.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif'])

    def is_valid_url(self, url):
        parsed_url = urlparse(url)
        return all([parsed_url.scheme, parsed_url.netloc])

    def update_layout(self, response):
        layout = pn.Column()

        # Parsing della risposta JSON
        response_data = json.loads(response)
        # logger.info(f"Response data: {response_data}")

        # Generazione dei grafici
        if 'chart' in response_data and response_data['chart']:
            echart_pane = self.generate_echarts(response_data['chart'], title='Chart')
            layout.append(echart_pane)

        # Generazione delle tabelle o delle schede
        if 'table' in response_data and response_data['table']:
            table_data = response_data['table']
            tabulator_widget = self.generate_tabulator(table_data)
            layout.append(tabulator_widget)

        return layout

    def generate_response(self, contents: str, user: str, chat_interface: pn.chat.ChatInterface):
        if not self.df:
            chat_interface.send("Please upload a CSV file to start the analysis.", user="Datadashr",
                                avatar='https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.png',
                                respond=False)
            return

        # logger.info(f"Request: {contents}")
        response = self.df.chat(contents)

        # Parse the response and update the layout
        layout = self.update_layout(response)

        # Send the layout to the chat interface
        chat_interface.send(layout, user="Datadashr",
                            avatar='https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.png', respond=False)

    def serve(self):
        settings_panel = pn.Column(
            self.box_file, self.box_llm, self.box_switch,
            styles={"padding": "15px", 'border': '1px solid white'}
        )

        chat_panel = pn.Column(
            self.chat_interface,
            sizing_mode='stretch_width',
            styles={"padding": "15px", 'border': '1px solid white'}
        )

        return pn.Column(
            pn.pane.SVG(
                "https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.svg",
                height=30,
            ),
            pn.Row(settings_panel, chat_panel),
            sizing_mode='stretch_width',
            styles={"padding": "15px", 'border': '1px solid white'},
        )


# To run the app
if __name__ == '__main__':
    app = App()
    app.serve().show()
