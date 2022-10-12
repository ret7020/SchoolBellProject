sudo cp ./configs/school-bells.service /lib/systemd/system/school-bells.service
sudo systemctl start school-bells.service
sudo systemctl enable school-bells.service
sudo systemctl daemon-reload