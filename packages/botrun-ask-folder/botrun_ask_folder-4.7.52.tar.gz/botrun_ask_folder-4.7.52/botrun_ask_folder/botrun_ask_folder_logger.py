import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class BotrunAskFolderLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BotrunAskFolderLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        current_folder_path = Path(__file__).resolve().absolute().parent
        parent_folder_path = current_folder_path.parent
        log_folder_path = parent_folder_path / "users" / "botrun_ask_folder"
        if not log_folder_path.exists():
            log_folder_path.mkdir(parents=True)
        # Configure the logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=log_folder_path / "botrun_ask_folder.log",
            # Specify your log file path here
            filemode='a'  # 'a' means append (add to existing log), 'w' means overwrite
        )
        # Create a logger
        self.logger = logging.getLogger("BotrunAskFolderLogger")
        self.logger.setLevel(logging.DEBUG)
        max_bytes = 1 * 1024 * 1024  # 1 MB
        backup_count = 1
        file_handler = RotatingFileHandler(
            log_folder_path / "botrun_ask_folder.log",
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger
