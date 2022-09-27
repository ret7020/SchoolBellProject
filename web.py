from flask import Flask, render_template, jsonify, request, redirect
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

        @self.app.route('/api/get_timetable')
        def __get_timetable():
            return self.get_timetable()

        @self.app.route('/api/update_timetable', methods=['POST'])
        def __update_timetable():
            return self.update_timetable()
        
        @self.app.route('/api/get_lesson_data')
        def __get_lesson_data():
            return self.get_lesson_data()

        @self.app.route('/api/update_lesson', methods=['POST'])
        def __update_lesson():
            return self.update_lesson()

        @self.app.route('/api/hard_refresh')
        def __hard_refresh():
            return self.hard_refresh()

    def parse_timetable(self):
        time_table_display = []
        for lessons_counter in range(len(self.tm.timetable)):
            lesson_finish = datetime.datetime.strptime(self.tm.timetable[lessons_counter][2], "%H:%M")
            going_now = False
            if datetime.datetime.strptime(self.tm.timetable[lessons_counter][1], "%H:%M").time() <= datetime.datetime.now().time() < lesson_finish.time():
                going_now = True
            try:
                break_start = datetime.datetime.strptime(self.tm.timetable[lessons_counter][2], "%H:%M")
                break_finish = datetime.datetime.strptime(self.tm.timetable[lessons_counter + 1][1], "%H:%M")
                time_table_display.append((lessons_counter + 1, self.tm.timetable[lessons_counter][1], self.tm.timetable[lessons_counter][2], int((break_finish - break_start).seconds / 60), going_now))
            except IndexError:
                time_table_display.append((lessons_counter + 1, self.tm.timetable[lessons_counter][1], self.tm.timetable[lessons_counter][2], 0, going_now))
        lessons_cnt = len(time_table_display)
        return time_table_display, lessons_cnt

    def index(self):
        config = self.dbm.get_config()
        time_table_display, lessons_cnt = self.parse_timetable()
        return render_template('index.html', building_number=config["building_number"], time_table=render_template('lessons.html', timetable=time_table_display, lessons_cnt=lessons_cnt))
    
    def get_timetable(self):
        tm_formatted = ''
        for lesson in self.tm.timetable:
            tm_formatted += f"{lesson[1]}\n"
        return jsonify({"status": True, "timetable": tm_formatted, "heights_px": len(self.tm.timetable) * 30})

    def update_timetable(self):
        new_timetable_lessons = request.form.get("timetable-raw")
        new_tmtb = []
        for lesson_start_time in new_timetable_lessons.split("\n"):
            lesson_start_time = lesson_start_time.rstrip()
            if len(lesson_start_time) > 1:
                try:
                    lesson_strt = datetime.datetime.strptime(lesson_start_time, "%H:%M")
                    lesson_finish = lesson_strt + datetime.timedelta(minutes=45)
                    
                    #print(lesson_start_time, lesson_finish.strftime("%H:%M"))
                    new_tmtb.append((lesson_start_time, lesson_finish.strftime("%H:%M")))
                except ValueError: # Skip invalid time format. This exception can be raised from datetime.datetime.strptime
                    pass
        self.dbm.update_timetable(new_tmtb)
        self.tm.update_timetable()
        time_table_display, lessons_cnt = self.parse_timetable()
        return jsonify({"status": True, "new_time_table": render_template('lessons.html', timetable=time_table_display, lessons_cnt=lessons_cnt)})
    
    def get_lesson_data(self):
        lesson_id = int(request.args.get("lesson_id"))
        dt = self.dbm.get_lesson(lesson_id)
        all_melodies = self.dbm.get_all_melodies()
        print(dt)
        return jsonify({"status": True, "lesson_start": dt[1], "lesson_finish": dt[2], "melody_id": dt[3], "all_melodies": render_template('melodies.html', melodies=all_melodies, selected=dt[3])})
    
    def update_lesson(self):
        self.dbm.update_lesson(int(request.form.get("lesson_id")), request.form.get("lesson-start"), request.form.get("lesson-finish"))
        self.tm.update_timetable()
        time_table_display, lessons_cnt = self.parse_timetable()
        return jsonify({"status": True, "new_time_table": render_template('lessons.html', timetable=time_table_display, lessons_cnt=lessons_cnt)})
        

    def hard_refresh(self):
        self.tm.update_timetable()
        return redirect('/')

    def run(self):
        self.app.run(host=self.host, port=self.port)

if __name__ == "__main__":
    web = WebUI(__name__)
    web.run()
