# How to install rfid libs

## Installations

```bash
git clone https://github.com/pimylifeup/MFRC522-python.git
```

Then, you should have a folder added named `MFRC522-python`

```bash
cd MFRC522-python
```

Once you're in the folder, you can install the library :

```bash
sudo python setup.py install
```

## Connections

| **RF522 Module** | **Raspberry Pi**       |
|------------------|------------------------|
| SDA              | Pin 24 / GPIO8 (CE0)   |
| SCK              | Pin 23 / GPIO11 (SCKL) |
| MOSI             | Pin 19 / GPIO10 (MOSI) |
| MISO             | Pin 21 / GPIO9 (MISO)  |
| IRQ              | —                      |
| GND              | Pin6 (GND)             |
| RST              | Pin22 / GPIO25         |
| 3.3V             | Pin 1 (3V3)            |
