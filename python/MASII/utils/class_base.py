import logging
class WinLogger(logging.Handler):
    def __init__(self, text_window):
        super().__init__()
        self.widget = text_window
        self.widget.setReadOnly(True)

    def register_logger(self):
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self)
        # You can control the logging level
        logging.getLogger().setLevel(logging.INFO)  

    def emit(self, record):
        msg = self.format(record)
        text = self.widget.toPlainText()
        if len(text) > 5120:
            self.widget.setPlainText('Clear\n')
        self.widget.appendPlainText(msg)

    def disable_console(self):
        logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(name)s - %(levelname)s - %(message)s')