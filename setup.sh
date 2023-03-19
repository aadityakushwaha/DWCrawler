sudo apt update -y
sudo apt upgraed -y
sudo apt install python3-pip -y
pip install -r requirements.txt
sudo apt install mysql-server -y
sudo mysql_secure_installation
python3 database.py
sudo apt install adminer -y
sudo a2enconf adminer
sudo systemctl reload apache2
