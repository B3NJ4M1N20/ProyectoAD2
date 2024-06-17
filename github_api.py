from github import Github
import os
from dotenv import load_dotenv
from github import GithubException, RateLimitExceededException, UnknownObjectException
import time
import logging

load_dotenv()

logging.basicConfig(filename="github_api.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class NoJsonFilesFound(Exception):
    pass

class GitHubClient:
    def __init__(self, token=None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.client = Github(self.token)
        self.repo = self.client.get_repo("B3NJ4M1N20/LabRedesAvanzadas")

    def get_content(self, path):
        try:
            logging.debug(f"Intentando obtener contenido de '{path}'")
            file_content = self.repo.get_contents(path)
            if isinstance(file_content, list):
                for item in file_content:
                    if item.type == "file" and item.name.endswith(".json"):
                        logging.debug(f"Contenido de '{path}' obtenido exitosamente")
                        return item.decoded_content.decode()
                raise NoJsonFilesFound(f"No se encontraron archivos JSON en '{path}'")
            else:
                logging.debug(f"Contenido de '{path}' obtenido exitosamente")
                return file_content.decoded_content.decode()
        except UnknownObjectException:
            logging.error(f"Archivo o carpeta '{path}' no encontrado en GitHub.")
            raise FileNotFoundError(f"Archivo o carpeta '{path}' no encontrado en GitHub.")
        except NoJsonFilesFound as e:
            logging.error(str(e))
            raise  # Re-lanzar la excepción para que sea manejada en otro lugar

    def upload_file(self, content, path):
        try:
            logging.debug(f"Intentando subir archivo a '{path}'")
            contents = self.get_content(path)
            if contents:
                self.repo.update_file(path, "Actualización de datos", content, contents.sha, branch="main")
                logging.info(f"Archivo {path} actualizado exitosamente en GitHub.")
            else:
                self.repo.create_file(path, "Creación de datos", content, branch="main")
                logging.info(f"Archivo {path} creado exitosamente en GitHub.")
        except GithubException as e:
            if e.status == 422:  # Código de estado para Unprocessable Entity
                logging.error(f"Error al procesar la entidad en GitHub: {e}")
            else:
                logging.error(f"Error general al subir archivo a GitHub (código {e.status}): {e.data['message']}")
            raise

    def download_file(self, path):
        try:
            logging.debug(f"Intentando descargar archivo de '{path}'")
            return self.get_content(path)
        except GithubException as e:
            if e.status == 401:  # Código de estado para Bad Credentials
                logging.error(f"Credenciales inválidas para acceder a GitHub: {e}")
            elif e.status == 404:  # Código de estado para UnknownObjectException (Not Found)
                logging.error(f"Archivo o carpeta '{path}' no encontrado en GitHub.")
                raise FileNotFoundError(f"Archivo o carpeta '{path}' no encontrado en GitHub.")
            else:
                logging.error(f"Error general al descargar archivo de GitHub (código {e.status}): {e.data['message']}")
            raise

class RateLimitHandler:
    @staticmethod
    def handle_rate_limit(func):
        def wrapper(*args, **kwargs):
            while True:
                if args[0].client.client.rate_limiting[0] > 0:  # Accede a través de client.client
                    try:
                        return func(*args, **kwargs)
                    except RateLimitExceededException as e:
                        reset_timestamp = e.rate_limiting_resettime
                        sleep_time = reset_timestamp - time.time() + 1  # Add 1 second to be safe
                        logging.warning(f"Límite de tasa excedido. Esperando {sleep_time:.0f} segundos...")
                        time.sleep(sleep_time)
                else:
                    reset_timestamp = args[0].client.client.rate_limiting_resettime  # Accede a través de client.client
                    sleep_time = reset_timestamp - time.time() + 1  # Add 1 second to be safe
                    logging.warning(f"Límite de tasa excedido. Esperando {sleep_time:.0f} segundos...")
                    time.sleep(sleep_time)
        return wrapper

class GitHubAPI:
    def __init__(self, token=None):
        self.client = GitHubClient(token)

    @RateLimitHandler.handle_rate_limit
    def upload_file(self, content, path):
        return self.client.upload_file(content, path)

    @RateLimitHandler.handle_rate_limit
    def download_file(self, path):
        return self.client.download_file(path)
