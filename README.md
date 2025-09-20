# tv_effect_crypt

Small pet project: hide and extract ASCII messages inside PNG images under the disguise of an "old TV" vertical scanline effect.

---

## Quickstart

### 1. Create and activate virtual environment

```bash
python -m venv .venv
```
* **Linux/macOS**:

  ```bash
  source .venv/bin/activate
  ```
* **Windows PowerShell**:

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare image

Put a PNG file named `photo.png` (RGB) in the project root.

### 4. Embed a message

```bash
python src/tv_effect_crypt.py --mode input --image photo --black-bit 0 --step 2
```

### 5. Extract a message

```bash
python src/tv_effect_crypt.py --mode output --image photo --black-bit 0 --step 2
```

---

## Parameters

* `--mode` — choose `input` to embed text or `output` to extract text.
* `--image` — PNG filename without extension.
* `--black-bit` — define whether `0` or `1` is encoded as black.
* `--step` — column step (controls spacing between vertical lines).


