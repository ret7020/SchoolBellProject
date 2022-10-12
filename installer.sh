echo -e "\033[33mInstalling python depends"
sudo apt --yes install python3-gst-1.0
python3 -m pip install -r requirements.txt
echo -e "\033[33mInstalling nginx"
sudo apt --yes install nginx
sudo systemctl start nginx.service
sudo systemctl enable nginx.service
sudo cp ./configs/nginx.conf /etc/nginx/nginx.conf
sudo /etc/init.d/nginx reload
echo -e "\033[32mInstallation complete! Run using run.sh"