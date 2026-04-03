#!/bin/bash

# install librespot
sudo apt-get update
sudo apt-get install -y git build-essential pkg-config libssl-dev libasound2-dev
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
git clone https://github.com/librespot-org/librespot
cd librespot
cargo build --release --no-default-features --features alsa-backend
sudo cp target/release/librespot /usr/local/bin/
cd ..

# install python dependencies
pip3 install spotipy tinydb RPi.GPIO

# create systemd service for librespot
sudo tee /etc/systemd/system/librespot.service << EOF
[Unit]
Description=Librespot Spotify Client
After=network.target sound.target

[Service]
ExecStart=/usr/local/bin/librespot \
  --name "Jukebox" \
  --device-type avr \
  --backend alsa \
  --device hw:0 \
  --bitrate 320 \
  --initial-volume 80
Restart=always
RestartSec=5
User=pi

[Install]
WantedBy=multi-user.target
EOF

# create systemd service for jukebox python app
sudo tee /etc/systemd/system/jukebox.service << EOF
[Unit]
Description=Jukebox Controller
After=network.target librespot.service

[Service]
ExecStart=/usr/bin/python3 /home/pi/jukebox/main.py
WorkingDirectory=/home/pi/jukebox
Restart=always
RestartSec=5
User=pi

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable librespot
sudo systemctl enable jukebox
sudo systemctl start librespot
sudo systemctl start jukebox

echo "Jukebox setup complete!"