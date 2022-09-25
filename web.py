from flask import Flask
import logging

class WebUI:
    def __init__(self, name, host='0.0.0.0', port='8080'):
        self.app = Flask(name, template_folder="webui/templates",
                         static_url_path='', static_folder='webui/static')
        self.host = host
        self.port = port
        self.app.config["TEMPLATES_AUTO_RELOAD"] = True

        # Disable requests logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    
        @self.app.route('/')
        def __index():
            return self.index()
    
    def index(self):
        return "WebUI works!"

    
    def run(self):
        self.app.run(host=self.host, port=self.port)

if __name__ == "__main__":
    web = WebUI(__name__)
    web.run()
    