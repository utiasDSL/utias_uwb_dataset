#!/bin/bash
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
read -s -p "Please enter password for sudo: " sudoPW
echo $sudoPW | sudo add-apt-repository universe
echo -en "\e[1A"
echo -e "\e[0K"
echo $sudoPW | sudo apt update
echo -en "\e[1A"
echo -e "\e[0K"
echo $sudoPW | sudo apt install -y p7zip-full
echo -en "\e[1A"
echo -e "\e[0K"
echo $sudoPW | sudo apt install curl
echo -en "\e[1A"
echo -e "\e[0K"
echo -e "${BLUE}Grab a cup of coffee and relax${NC}\n"
curl -L https://github.com/utiasDSL/utias_uwb_dataset/releases/download/Dataset-v1.0/dataset.7z > dataset.7z
7z x ./dataset.7z
rm dataset.7z
echo -e "${GREEN}Setup complete${NC}\n"



