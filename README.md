# tv_effect_crypt

Small pet project: hide and extract ASCII messages inside PNG images under the disguise of an "old TV" vertical scanline effect.

## Quickstart

1. Create and activate virtual environment:
```bash
python -m venv .venv
# Linux/mac:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\Activate.ps1
Install dependency:

bash
Копировать код
pip install -r requirements.txt
Put a PNG file photo.png (RGB) in repo root.

Embed message (interactive):

bash
Копировать код
python src/tv_effect_crypt.py --mode input --image photo --black-bit 0 --step 2
Extract message:

bash
Копировать код
python src/tv_effect_crypt.py --mode output --image photo --black-bit 0 --step 2
