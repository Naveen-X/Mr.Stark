git clone https://S4tyendra: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@github.com/Naveen-X/Mr.Stark
apt-get update && apt upgrade -y
apt-get install mediainfo -y
cd "Mr.Stark" && git pull && pip install -r req.txt
python3 -m "Stark"