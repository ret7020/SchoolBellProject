from flask import Flask, render_template, jsonify, request, redirect, Blueprint
from werkzeug.utils import secure_filename
import logging
import datetime
import os


class MelodiesStorage:
    def __init__(self):
        self.blueprint = Blueprint('melodies', __name__, static_url_path='/melodies', static_folder='./data/sounds')


class WebUI:
    def __init__(self, name, dbm, tm, aud, melodies_storage, host='0.0.0.0', port='8080', dev_mode=False):
        self.app = Flask(name, template_folder="webui/templates",
                         static_url_path='/static', static_folder='webui/static')
        self.host = host
        self.port = port
        self.app.config["TEMPLATES_AUTO_RELOAD"] = True
        self.dbm = dbm
        self.tm = tm
        self.aud = aud

        # Disable requests logging
        if not dev_mode:
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)

        # Apply blueprints
        self.app.register_blueprint(melodies_storage.blueprint)

    
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

        @self.app.route('/api/get_melodies')
        def __get_melodies():
            return self.get_melodies()

        @self.app.route('/api/upload_melody', methods=['POST'])
        def __upload_melody():
            return self.upload_melody()

        @self.app.route('/api/update_melody_title', methods=['POST'])
        def __update_melody_title():
            return self.update_melody_title()

        @self.app.route('/api/hard_refresh')
        def __hard_refresh():
            return self.hard_refresh()

        @self.app.route('/api/manual_bell')
        def __manual_bell():
            return self.manual_bell()

        @self.app.route('/api/update_config', methods=['POST'])
        def __update_config():
            return self.update_config()

    def parse_timetable(self):
        time_table_display = []
        for lessons_counter in range(len(self.tm.timetable)):
            lesson_finish = datetime.datetime.strptime(self.tm.timetable[lessons_counter][2], "%H:%M")
            going_now = False
            break_going_now = False
            if datetime.datetime.strptime(self.tm.timetable[lessons_counter][1], "%H:%M").time() <= datetime.datetime.now().time() < lesson_finish.time():
                going_now = True
            try:
                break_start = datetime.datetime.strptime(self.tm.timetable[lessons_counter][2], "%H:%M")
                break_finish = datetime.datetime.strptime(self.tm.timetable[lessons_counter + 1][1], "%H:%M")
                if not going_now and break_start.time() <= datetime.datetime.now().time() < break_finish.time():
                    break_going_now = True
                time_table_display.append((lessons_counter + 1, self.tm.timetable[lessons_counter][1], self.tm.timetable[lessons_counter][2], int((break_finish - break_start).seconds / 60), going_now, break_going_now))
            except IndexError:
                time_table_display.append((lessons_counter + 1, self.tm.timetable[lessons_counter][1], self.tm.timetable[lessons_counter][2], 0, going_now, break_going_now))
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
        return jsonify({"status": True, "lesson_start": dt[1], "lesson_finish": dt[2], "melody_id": dt[3], "all_melodies": render_template('melodies.html', melodies=all_melodies, selected=dt[3])})
    
    def update_lesson(self):
        self.dbm.update_lesson(int(request.form.get("lesson_id")), request.form.get("lesson-start"), request.form.get("lesson-finish"), int(request.form.get("melodySelect")))
        self.tm.update_timetable()
        time_table_display, lessons_cnt = self.parse_timetable()
        return jsonify({"status": True, "new_time_table": render_template('lessons.html', timetable=time_table_display, lessons_cnt=lessons_cnt)})
        
    def get_melodies(self):
        return jsonify({"status": True, "melodies": self.dbm.get_all_melodies()})

    def update_melody_title(self):
        new_title = request.form.get('title')
        self.dbm.update_melody_title(int(request.form.get('melody_id')), new_title)
        return jsonify({"status": True, "new_title": new_title})

    def check_file_extension(self, filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['wav', 'mp3']

    
    def hard_refresh(self):
        self.tm.update_timetable()
        return redirect('/')

    def upload_melody(self):
        if 'melody_file' in request.files:
            melody_file = request.files['melody_file']
            if melody_file.filename:
                if melody_file and self.check_file_extension(melody_file.filename):
                    filename = secure_filename(melody_file.filename)
                    melody_file.save(os.path.join("./data/sounds", filename))
                    melody_id = self.dbm.add_melody(filename, filename)
                    return jsonify({"status": True, "melody_name": filename, "melody_id": melody_id})
        return jsonify({"status": False})

    def manual_bell(self):
        self.aud.ring_bell("mp3.mp3")
        return jsonify({"status": True})

    def update_config(self):
        self.dbm.update_config(request.form.get("building_number"), request.form.get("new_password"))
        return jsonify({"status": True})

    def run(self):
        self.app.run(host=self.host, port=self.port)

if __name__ == "__main__":
    web = WebUI(__name__)
    web.run()
