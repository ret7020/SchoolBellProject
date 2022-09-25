from flask import Flask, render_template
import logging
import datetime

class WebUI:
    def __init__(self, name, dbm, tm, host='0.0.0.0', port='8080'):
        self.app = Flask(name, template_folder="webui/templates",
                         static_url_path='/static', static_folder='webui/static')
        self.host = host
        self.port = port
        self.app.config["TEMPLATES_AUTO_RELOAD"] = True
        self.dbm = dbm
        self.tm = tm

        # Disable requests logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    
        @self.app.route('/')
        def __index():
            return self.index()
    
    def index(self):
        config = self.dbm.get_config()
        time_table_display = []
        for lessons_counter in range(len(self.tm.timetable)):
            try:
                break_start = datetime.datetime.strptime(self.tm.timetable[lessons_counter][2], "%H:%M")
                break_finish = datetime.datetime.strptime(self.tm.timetable[lessons_counter + 1][1], "%H:%M")
                time_table_display.append((lessons_counter + 1, self.tm.timetable[lessons_counter][1], self.tm.timetable[lessons_counter][2], int((break_finish - break_start).seconds / 60)))
            except IndexError:
                pass
        lessons_cnt = len(time_table_display)
        return render_template('index.html', building_number=config["building_number"], timetable=time_table_display, lessons_cnt=lessons_cnt)

    
    def run(self):
        self.app.run(host=self.host, port=self.port)

if __name__ == "__main__":
    web = WebUI(__name__)
    web.run()
