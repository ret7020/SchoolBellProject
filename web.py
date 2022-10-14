from flask import Flask, render_template, jsonify, request, redirect, Blueprint
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import logging
import datetime
import os
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from models import LoginnedUserModel
import ntplib
import pytz
from stats import get_stats


class MelodiesStorage:
    def __init__(self, path_to_dir='./data/sounds'):
        self.blueprint = Blueprint(
            'melodies', __name__, static_url_path='/melodies', static_folder=path_to_dir)


class WebUI:
    def __init__(self, name, dbm, tm, aud, melodies_storage, ntp_server, secret_key='DEF_KEY', host='0.0.0.0', port='8080', dev_mode=False):
        self.app = Flask(name, template_folder="webui/templates",
                         static_url_path='/static', static_folder='webui/static')
        self.app.config['MAX_CONTENT_LENGTH'] = 16 * \
            1000 * 1000  # 16 Mb max upload
        # Auto - reload html/css/sources without server reboot
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True
        self.app.config['SECRET_KEY'] = secret_key
        self.host = host
        self.port = port

        self.dbm = dbm  # Link to database object
        self.tm = tm  # Link to timemanager object
        self.aud = aud  # Link to audio manager object
        self.login_manager = LoginManager(self.app)
        self.ntp_server = ntp_server
        self.ntc = ntplib.NTPClient()

        # Disable requests logging in production mode
        if not dev_mode:
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)

        # Apply blueprints
        # Blueprint for custom melodies location
        self.app.register_blueprint(melodies_storage.blueprint)

        # UI routes
        @self.app.route('/')
        def __index():
            return self.index()

        @self.app.route('/login')
        def __login():
            return self.login()

        # API routes

        @self.app.route('/api/login', methods=['POST'])
        def __login_api():
            return self.login_api()

        @self.app.route('/api/logout')
        def __logout():
            return self.logout()

        @self.app.route('/api/get_timetable')
        @login_required
        def __get_timetable():
            '''
            Get all day timetable data
            '''
            return self.get_timetable()

        @self.app.route('/api/update_timetable', methods=['POST'])
        @login_required
        def __update_timetable():
            '''
            Recreate timetable via lessons start times
            '''
            return self.update_timetable()

        @self.app.route('/api/get_lesson_data')
        @login_required
        def __get_lesson_data():
            '''
            Get concrete lesson data(time, melody, e.t.c)
            '''
            return self.get_lesson_data()

        @self.app.route('/api/update_lesson', methods=['POST'])
        @login_required
        def __update_lesson():
            '''
            Change concrete lesson data(time, melody and e.t.c)
            '''
            return self.update_lesson()

        @self.app.route('/api/get_melodies')
        @login_required
        def __get_melodies():
            '''
            Get all uploaded and registered melodies for bell
            '''
            return self.get_melodies()

        @self.app.route('/api/upload_melody', methods=['POST'])
        @login_required
        def __upload_melody():
            '''
            Upload and register new melody for bell
            '''
            return self.upload_melody()

        @self.app.route('/api/update_melody_title', methods=['POST'])
        @login_required
        def __update_melody_title():
            '''
            Change concrete melody title(display title)
            '''
            return self.update_melody_title()

        @self.app.route('/api/hard_refresh')
        @login_required
        def __hard_refresh():
            '''
            Reload timemanager data directly from database
            '''
            return self.hard_refresh()

        @self.app.route('/api/manual_bell')
        @login_required
        def __manual_bell():
            '''
            Test bell
            '''
            return self.manual_bell()

        @self.app.route('/api/update_config', methods=['POST'])
        @login_required
        def __update_config():
            '''
            Change system configuration
            '''
            return self.update_config()

        @self.app.route('/api/get_sys')
        @login_required
        def __get_system_info():
            return self.get_system_info()

        @self.app.route('/api/get_mute_mode')
        @login_required
        def __get_mute_mode():
            return self.get_mute_mode()

        @self.app.route('/api/toggle_mute_mode')
        @login_required
        def __toggle_mute_mode():
            return self.change_mute_mode(request.args.get("current_mode"))

        @self.login_manager.user_loader
        def load_user(user_id: str):
            return LoginnedUserModel.get(user_id)

    def parse_timetable(self):
        '''
        Load and process timetable from timemanger
        '''
        time_table_display = []
        # Iterate over lessons
        for lessons_counter in range(len(self.tm.timetable)):
            lesson_finish = datetime.datetime.strptime(
                self.tm.timetable[lessons_counter][2], "%H:%M")
            going_now = False  # This lesson is going now flag
            break_going_now = False
            if datetime.datetime.strptime(self.tm.timetable[lessons_counter][1], "%H:%M").time() <= datetime.datetime.now().time() < lesson_finish.time():
                going_now = True
            try:
                break_start = datetime.datetime.strptime(
                    self.tm.timetable[lessons_counter][2], "%H:%M")
                break_finish = datetime.datetime.strptime(
                    self.tm.timetable[lessons_counter + 1][1], "%H:%M")
                if not going_now and break_start.time() <= datetime.datetime.now().time() < break_finish.time():
                    break_going_now = True
                time_table_display.append((lessons_counter + 1, self.tm.timetable[lessons_counter][1], self.tm.timetable[lessons_counter][2], int(
                    (break_finish - break_start).seconds / 60), going_now, break_going_now))
            except IndexError:  # Try to locate break after lesson. We will get IndexError after last lesson
                time_table_display.append(
                    (lessons_counter + 1, self.tm.timetable[lessons_counter][1], self.tm.timetable[lessons_counter][2], 0, going_now, break_going_now))
        lessons_cnt = len(time_table_display)
        return time_table_display, lessons_cnt

    def login_api(self):
        correct = self.dbm.check_password(request.form.get('password'))
        if correct:
            login_user(LoginnedUserModel(1))
        return jsonify({"status": correct})

    def login(self):
        if not current_user.is_authenticated:
            return render_template('login.html')
        else:
            return redirect('/')

    def logout(self):
        logout_user()
        return redirect('/login')

    def index(self):
        if current_user.is_authenticated:
            config = self.dbm.get_config()
            time_table_display, lessons_cnt = self.parse_timetable()
            return render_template('index.html', building_number=config["building_number"], time_table=render_template('lessons.html', timetable=time_table_display, lessons_cnt=lessons_cnt))
        else:
            return redirect('/login')

    def get_timetable(self):
        tm_formatted = ''
        for lesson in self.tm.timetable:  # Format lessons as text like '10:00\n15:00\n20:00\n'
            tm_formatted += f"{lesson[1]}\n"
        return jsonify({"status": True, "timetable": tm_formatted, "heights_px": len(self.tm.timetable) * 30})

    def update_timetable(self):
        new_timetable_lessons = request.form.get("timetable-raw")
        new_tmtb = []
        for lesson_start_time in new_timetable_lessons.split("\n"):
            lesson_start_time = lesson_start_time.rstrip()
            if len(lesson_start_time) > 1:
                try:
                    lesson_strt = datetime.datetime.strptime(
                        lesson_start_time, "%H:%M")
                    # Calculate lesson finish time
                    lesson_finish = lesson_strt + \
                        datetime.timedelta(minutes=45)
                    new_tmtb.append(
                        (lesson_start_time, lesson_finish.strftime("%H:%M")))
                except ValueError:  # Skip invalid time format. This exception can be raised from datetime.datetime.strptime
                    pass
        self.dbm.update_timetable(new_tmtb)  # Save to databse
        self.tm.update_timetable()  # Reload timetable in timemanager
        time_table_display, lessons_cnt = self.parse_timetable()
        return jsonify({"status": True, "new_time_table": render_template('lessons.html', timetable=time_table_display, lessons_cnt=lessons_cnt)})

    def get_lesson_data(self):
        lesson_id = int(request.args.get("lesson_id"))
        dt = self.dbm.get_lesson(lesson_id)
        all_melodies = self.dbm.get_all_melodies()
        return jsonify({"status": True, "lesson_start": dt[1], "lesson_finish": dt[2], "melody_id": dt[3], "all_melodies": render_template('melodies.html', melodies=all_melodies, selected=dt[3]), "saturday_work": dt[4], "sunday_work": dt[5]})

    def update_lesson(self):
        self.dbm.update_lesson(int(request.form.get("lesson_id")), request.form.get("lesson-start"), request.form.get("lesson-finish"),
                               int(request.form.get("melodySelect")), request.form.get("work_at_saturday"), request.form.get("work_at_sunday"))
        self.tm.update_timetable()
        time_table_display, lessons_cnt = self.parse_timetable()
        return jsonify({"status": True, "new_time_table": render_template('lessons.html', timetable=time_table_display, lessons_cnt=lessons_cnt)})

    def get_melodies(self):
        return jsonify({"status": True, "melodies": self.dbm.get_all_melodies(only_names=True)})

    def update_melody_title(self):
        new_title = request.form.get('title')
        self.dbm.update_melody_title(
            int(request.form.get('melody_id')), new_title)
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
        self.aud.ring_bell("./data/sounds/mp3.mp3")
        return jsonify({"status": True})

    def update_config(self):
        self.dbm.update_config(request.form.get(
            "building_number"), request.form.get("new_password"), request.form.get("new_password_confirm"))
        return jsonify({"status": True})

    def get_system_info(self):
        current_time_raw = datetime.datetime.now()
        current_time_fr = current_time_raw.strftime("%H:%M:%S")

        try:
            response = self.ntc.request(self.ntp_server, version=3)
            ntp_time = datetime.datetime.fromtimestamp(
                response.tx_time, pytz.timezone("Europe/Moscow")).strftime("%H:%M:%S")
        except ntplib.NTPException:
            ntp_time = "N/A"
        base_data = {"status": True, "server_time": current_time_fr,
                     "ntp_time": ntp_time, "ntp_server": self.ntp_server}
        base_data.update(get_stats())
        return jsonify(base_data)

    def get_mute_mode(self):
        mute_data = self.tm.mute_mode.copy()
        mute_data[1] = [mute_data[1].day,
                        mute_data[1].month, mute_data[1].year]
        return jsonify({"status": True, "mute_mode": mute_data})

    def change_mute_mode(self, current_mode):
        if current_mode == "true":
            self.dbm.set_mute_mode()
        else:
            self.dbm.reset_mute_mode()
        return jsonify({"status": True})

    def run(self):
        self.app.run(host=self.host, port=self.port)


if __name__ == "__main__":
    web = WebUI(__name__)
    web.run()
