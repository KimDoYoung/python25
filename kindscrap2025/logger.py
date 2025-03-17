import logging
from pathlib import Path
from datetime import datetime


class BatchLogger:
    def __init__(self, log_dir, level=logging.INFO, use_file_handler=True, use_console_handler=True):
        """
        로거핸들러 설정

        :param log_dir: 저장폴더
        :param level: 로그 레벨
        :param use_file_handler: 파일사용여부 default True
        :param use_console_handler: 콘솔 사용여부 default True
        """
        # Generate daily log file name
        today = datetime.now().strftime("%Y_%m_%d")
        log_file =  Path(log_dir) / f"kindscrap_{today}.log"

        # Use log_file as the logger's name
        self.logger = logging.getLogger(str(log_file))
        self.logger.setLevel(level)
        self.logger.propagate = False  # Prevent duplicate logs if root logger is configured

        # Ensure the log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)

        # Add file handler if enabled
        if use_file_handler:
            file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(file_handler)

        # Add console handler if enabled
        if use_console_handler:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(console_handler)

    def get_logger(self):
        """Return the logger instance."""
        return self.logger
