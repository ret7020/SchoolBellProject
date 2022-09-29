# School Bell System
## About
![image](https://user-images.githubusercontent.com/55328925/192607462-cd2e86d0-51f6-4301-b7c3-0341b899c6db.png)
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
1. Html5 + CSS3 + Pure JS(Modern fetch api for ajax api)

## Installation
Clone this repository to your Raspberry PI</br>
```
git clone https://github.com/ret7020/SchoolBellProject
```
Start the installer(WITH ROOT PRIVILAGES)</br>
```
sudo ./installer.sh
```
Run project</br>
```
./run.sh
```
## Production deployment
### Parts:
1. Autorun on boot
2. Enable port 80 for Flask
3. Test final deployment steps

## Development workflow
### ToDo
1. Base timetable watcher :heavy_check_mark:
2. Bell ring method :heavy_check_mark:
3. WebUI to edit timetable :heavy_check_mark:
4. WebUI ability to upload melodies :heavy_check_mark:
5. Adaptive WebUI for smartphones :heavy_check_mark:
6. Bindings to weekdays(DISABLE bell on Saturday and Sunday)
7. Design as a REST API application with mostly AJAX WebUI as client :heavy_check_mark:
8. Create Production Setup

## Screenshots
![image](https://user-images.githubusercontent.com/55328925/193130050-b140f16a-6967-4fa3-97ed-22f834dda666.png)
![image](https://user-images.githubusercontent.com/55328925/193130146-8b1dc113-df6a-4f62-bccd-d0cf18536115.png)
![image](https://user-images.githubusercontent.com/55328925/193130209-2b89f378-8bed-4159-8fa7-5ee436584c8f.png)
