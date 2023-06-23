#!/bin/bash
#
#RED='\033[0;31m'
#GREEN='\033[0;32m'
#YELLOW='\033[0;33m'
#NC='\033[0m'
#
#echo_color() {
#  local color=$1
#  local message=$2
#  echo -e "${color}${message}${NC}"
#}
#
#echo_red() {
#  local message=$1
#  echo_color "${RED}" "$message"
#}
#
#echo_green() {
#  local message=$1
#  echo_color "${GREEN}" "$message"
#}
#
#echo_yellow() {
#  local message=$1
#  echo_color "${YELLOW}" "$message"
#}

#echo_red "This is an error message."
#echo_green "This is a success message."
#echo_yellow "This is a warning message."
#echo "This is a normal message."
echo -e "\e[32mCloning repository...\e[0m"
git clone https://github.com/Naveen-X/Mr.Stark

echo -e "\e[32mInstalling apt-utils...\e[0m"
apt-get install apt-utils -y

echo -e "\e[32mUpdating system packages...\e[0m"
sudo apt-get update && sudo apt-get upgrade -y

echo -e "\e[32mInstalling Wget...\e[0m"
sudo apt install wget

echo -e "\e[32mInstalling AI MODEL...\e[0m"
wget https://people.eecs.berkeley.edu/~rich.zhang/projects/2016_colorization/files/demo_v2/colorization_release_v2.caffemodel -P ./resources/ai_helpers/

echo -e "\e[32mInstalling mediainfo...\e[0m"
sudo apt-get install mediainfo -y

echo -e "\e[32mInstalling libgl1-mesa-glx...\e[0m"
sudo apt-get install libgl1-mesa-glx -y

echo -e "\e[32mInstalling ffmpeg...\e[0m"
sudo apt-get install ffmpeg -y

echo -e "\e[32mInstalling gifsicle...\e[0m"
sudo apt-get install gifsicle -y

echo -e "\e[32mUpdating repository...\e[0m"
cd "Mr.Stark" && git pull && pip install -r req.txt

echo -e "\e[32mRunning Stark...\e[0m"
python3 -m "Stark"

#
#
#git clone https://github.com/Naveen-X/Mr.Stark
#cd "Mr.Stark" && git pull && pip install -r req.txt
#sudo apt-get update && apt upgrade -y
#sudo apt-get install mediainfo -y
#sudo apt-get install libgl1-mesa-glx -y
#sudo apt-get install python3-opencv -y
#sudo apt-get install ffmpeg -y
#sudo apt-get install gifsicle -y
#python3 -m "Stark"
