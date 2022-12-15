# School Bell System
## About
![image](https://user-images.githubusercontent.com/55328925/195398593-111a9cf2-1c18-423a-8d8c-aa6cc8934359.png)
This is a project to automate the work of school bells. The main features are the ease of installation of the system and simple configuration through a convenient web interface.

## Techincal Stack
#### Hardware
1. RPi 3B (Or any another Raspberry PI or it's copies, like Orange Pi)
2. 3.5 mm audio system
#### Backend
1. Python + Playsound lib
2. Flask - REST API
3. Sqlite3 - Database
#### Frontend
<b>Native stack</b></br>
1. HTML5 + CSS3 + Pure JS(Modern fetch api for ajax api)

## Installation
Clone this repository to your Raspberry PI</br>
```
git clone https://github.com/ret7020/SchoolBellProject
```
Start the installer(WITH ROOT PRIVILAGES)</br>
```
chmod +x installer.sh
sudo ./installer.sh
```
Change SECRET_KEY in `config.py` to long random string</br>
Run project<b>(only for current ssh session without autostart)</b></br>
```
./run.sh
```
</br>
<b>Default password from admin panel: 12345</b>

## Production deployment
### Autorun on boot
This is an instruction for systemd systems(systems with systemd as init). In the other cases refer to documentation for your init system.</br>
<b>If you clone repository in local user(named with pi) folder you will not have to change systemd service config. </b>
1. Open `./configs/school-bells.service` with `vim`, `nano` or another text editor.
```
vim school-bells.service
```
2. Edit line number <b>7</b>, change `/home/pi/Documents/Progs/SchoolBellProject/` with your <b>absolute</b> path to directory with SchoolBellProject 
3. Edit line number <b>8</b>, change `/home/pi/Documents/Progs/SchoolBellProject/run.sh` with <b>absolute</b> path to `run.sh` file SchoolBellProject dir
4. Edit line number <b>9</b>, change `/home/pi/.local/lib/python3.9/site-packages` with <b>absolute</b> path to your python env(with installed libraies from `requirements.txt`)
5. Then execute script `setup_autorun.sh`
6. After it you can check service status (if must be active)
```
sudo systemctl start school-bells.service
```


### Enable port 80 for Flask (via nginx forwarding)
The installer script immediately installs nginx, adds it to autoload and applies a special config that redirects port 8080 from the flask server to 80 nginx port.
### Test final deployment steps
1. Check web ui on port 80.
2. Reboot RPi and check autorun on boot


## Development workflow
### ToDo
1. Base timetable watcher :heavy_check_mark:
2. Bell ring method :heavy_check_mark:
3. WebUI to edit timetable :heavy_check_mark:
4. WebUI ability to upload melodies :heavy_check_mark:
5. Adaptive WebUI for smartphones :heavy_check_mark:
6. Bindings to weekdays(DISABLE bell on Saturday and Sunday) :heavy_check_mark:
7. Design as a REST API application with mostly AJAX WebUI as client :heavy_check_mark:
8. Create Production Setup :heavy_check_mark:
9. Create first release (1.0.0) :heavy_check_mark:

10. Delete melody from list
11. Modify Lesson start melody and finish melody

## Screenshots
![image](https://user-images.githubusercontent.com/55328925/193130050-b140f16a-6967-4fa3-97ed-22f834dda666.png)
![image](https://user-images.githubusercontent.com/55328925/193130146-8b1dc113-df6a-4f62-bccd-d0cf18536115.png)
![image](https://user-images.githubusercontent.com/55328925/193130209-2b89f378-8bed-4159-8fa7-5ee436584c8f.png)