#!/bin/bash

# Renk tanımları
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}>>> Evren Simülasyonu Kurulumu Başlatılıyor...${NC}"

# 1. Python kontrolü
if ! command -v python3 &> /dev/null
then
    echo "Hata: python3 bulunamadı. Lütfen Python yükleyin."
    exit
fi

# 2. Sanal ortam (venv) oluşturma
echo -e "${GREEN}>>> Sanal ortam oluşturuluyor (venv)...${NC}"
python3 -m venv venv

# 3. Sanal ortamı aktif etme
source venv/bin/activate

# 4. Bağımlılıkları yükleme
echo -e "${GREEN}>>> Bağımlılıklar yükleniyor (requirements.txt)...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${BLUE}>>> Kurulum başarıyla tamamlandı!${NC}"
echo -e "${GREEN}>>> Simülasyonu başlatmak için şu komutu kullanın:${NC}"
echo -e "${BLUE}source venv/bin/activate && python3 main.py${NC}"
