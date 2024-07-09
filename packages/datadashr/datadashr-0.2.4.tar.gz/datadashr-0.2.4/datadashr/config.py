import os
import warnings
from datadashr.core.utilities.logger import LogManager
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()

# Suppress warnings
warnings.filterwarnings("ignore")  # Suppress all warnings
warnings.filterwarnings("ignore", message="Number of requested results *")  # Suppress warnings from Chromadb

# Set paths
PATH = os.path.dirname(os.path.realpath(__file__))
CACHE_DIR = os.path.join(PATH, "data", "cache_dir")
CHART_DIR = os.path.join(PATH, "data", "charts", "datadashr.png")
LOG_DIR = os.path.join(PATH, "data", "logs", "datadashr_log.duckdb")
CSV_DIR = os.path.join(PATH, "data", "csv")
DUCKDB_PATH = os.path.join(PATH, "data", "db", "datadashr.db")
VECTOR_DIR = os.path.join(PATH, "data", "vectors")
FANCY_RESPONSE_TEMPLATE = os.path.join(PATH, "core", "utilities")

# Set logger
log_manager = LogManager(LOG_DIR, verbose=True)
