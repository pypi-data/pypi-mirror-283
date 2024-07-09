from pydantic import BaseModel


class SQLConfig(BaseModel):
    """
    SQLConfig is a Pydantic model that defines the configuration for an SQL database connection.

    Attributes:
        dialect (str): The SQL dialect to use (e.g., 'postgresql', 'mysql').
        driver (str): The database driver to use (e.g., 'psycopg2', 'pymysql').
        host (str): The hostname of the database server.
        port (int): The port number on which the database server is listening.
        database (str): The name of the database to connect to.
        username (str): The username to use for authentication.
        password (str): The password to use for authentication.
    """

    dialect: str
    driver: str
    host: str
    port: int
    database: str
    username: str
    password: str

    class Config:
        """
        Pydantic model configuration to forbid extra attributes during model initialization.
        """
        extra = 'forbid'
