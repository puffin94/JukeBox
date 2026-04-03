# JukeBox
This project is designed to work with Python 3.14, and a Raspberry Pi 2W.

## Design Plans
### 1. Overall System Architecture
```mermaid
flowchart TB
    subgraph CABINET["Jukebox Cabinet"]
        BUTTONS["Button Matrix\nA1 .. E10"]
        subgraph PI["Raspberry Pi Zero 2W"]
            PYTHON["jukebox\nPython"]
            LIBRE["librespot\nsystemd"]
        end
        DAC["HifiBerry DAC"]
        AMP["Amplifier"]
        SPEAKERS["Speakers"]
    end

    BUTTONS -->|GPIO| PYTHON
    PYTHON -->|Spotify API| LIBRE
    LIBRE -->|I2S| DAC
    DAC -->|RCA/Jack| AMP
    AMP --> SPEAKERS
```
### 2. Button Press to Audio

```mermaid
flowchart TD
    A["User presses button e.g. B3"]
    B["GPIO matrix scan detects B3"]
    C["main.py looks up B3 in TinyDB"]
    D["Returns track URI, title, artist"]
    E["Track added to queue"]
    F{"Anything\nplaying?"}
    G["Stays queued"]
    H["spotify.py calls /v1/me/player/play"]
    I["librespot receives command"]
    J["Streams audio from Spotify"]
    K["I2S -> DAC -> Amp -> Speakers"]

    A --> B --> C --> D --> E --> F
    F -->|Yes| G
    F -->|No| H --> I --> J --> K
```
### 3. Auth Flow

```mermaid
flowchart TD
    A["main.py starts"]
    B{"Cached token\nexists?"}
    C["Read .cache file"]
    D["Ready"]
    E["Open browser - Spotify login"]
    F["User logs in"]
    G["Spotify redirects to localhost:8080"]
    H["spotipy captures token + refresh token"]
    I["Saves to .cache on Pi"]

    A --> B
    B -->|Yes| C --> D
    B -->|No| E --> F --> G --> H --> I --> D
```

### 4. Service Relationship
```mermaid
flowchart TD
    BOOT["Boot"]
    SD["systemd"]
    LS["librespot.service"]
    JB["jukebox.service"]
    REG["Registers as Spotify Connect device"]
    WAIT["Waits for playback commands"]
    ENV["Loads .env + TinyDB"]
    GPIO["Scans GPIO"]
    PLAY["Button press -> Spotify API -> librespot plays"]

    BOOT --> SD
    SD --> LS
    SD --> JB
    LS --> REG --> WAIT
    JB --> ENV --> GPIO --> PLAY
```