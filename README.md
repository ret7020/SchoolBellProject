# School Bell System
## About
![image](https://user-images.githubusercontent.com/55328925/195398593-111a9cf2-1c18-423a-8d8c-aa6cc8934359.png)
This is a project to automate the work of school bells. The main features are the ease of installation of the system and simple configuration through a convenient web interface.

## Techincal Stack
#### Hardware
1. RPi 3B (Or anyanother Raspberry PI or it's copies, like Orange Pi)
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
Run project(only for current ssh session)</br>
```
./run.sh
```
## Production deployment
### Autorun on boot
This is an instruction for systemd systems(systems with systemd as init). In the other cases refer to documentation for your init system.</br>
1. Open `./configs/school-bells.service` with `vim`, `nano` or another text editor.
```
vim school-bells.service
```
2. Edit line number <b>7</b>, change `/home/pi/Documents/Progs/SchoolBellProject/` with your <b>absolute</b> path to directory with SchoolBellProject 
3.

### Enable port 80 for Flask (via nginx forwarding)
The installer script immediately installs nginx, adds it to autoload and applies a special config that redirects port 8080 from the flask server to 80 nginx port.
### Test final deployment steps
No content for now

## Development workflow
### ToDo
1. Base timetable watcher :heavy_check_mark:
2. Bell ring method :heavy_check_mark:
3. WebUI to edit timetable :heavy_check_mark:
4. WebUI ability to upload melodies :heavy_check_mark:
5. Adaptive WebUI for smartphones :heavy_check_mark:
6. Bindings to weekdays(DISABLE bell on Saturday and Sunday)
7. Design as a REST API application with mostly AJAX WebUI as client :heavy_check_mark:
8. Create Production Setup :heavy_check_mark:
9. Create first release (1.0.0)

## Screenshots
![image](https://user-images.githubusercontent.com/55328925/193130050-b140f16a-6967-4fa3-97ed-22f834dda666.png)
![image](https://user-images.githubusercontent.com/55328925/193130146-8b1dc113-df6a-4f62-bccd-d0cf18536115.png)
![image](https://user-images.githubusercontent.com/55328925/193130209-2b89f378-8bed-4159-8fa7-5ee436584c8f.png)
