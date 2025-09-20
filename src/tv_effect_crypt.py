#!/usr/bin/env python3
"""
steg_image.py
Simple column-based steganography: embed/extract ASCII text in PNG images.

Usage (examples):
  # embed interactive
  python src/steg_image.py --mode input --image photo --black-bit 0 --step 2

  # extract
  python src/steg_image.py --mode output --image photo --black-bit 0 --step 2
Notes:
  - Input image must be: <image>.png
  - Embedding writes: <image>_lightened.png and <image>_steg.png (final)
  - Extraction reads: <image>_steg.png
"""

from pathlib import Path
from PIL import Image
import argparse
import sys

# -------------------------
# Core helpers
# -------------------------

def lighten_image_min(image_stem):
    """
    Open <image_stem>.png, add +1 to each RGB channel for each pixel (clamped to 255),
    save as <image_stem>_lightened.png and return the Path.
    """
    src = Path(f"{image_stem}.png")
    out = Path(f"{image_stem}_lightened.png")

    if not src.exists():
        raise FileNotFoundError(f"Source image not found: {src}")

    img = Image.open(src).convert("RGB")
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            pixels[x, y] = (min(r+1, 255), min(g+1, 255), min(b+1, 255))

    img.save(out)
    return out

def text_to_bits_flat(text):
    """Convert ASCII string to flat list of bits (8 bits per char)."""
    bits = []
    for ch in text:
        bits.extend([int(b) for b in format(ord(ch), "08b")])
    return bits

def embed_text_bits_into_image(text, image_stem, black_bit_value, column_step=2):
    """
    Embed bits into <image_stem>_lightened.png by scanning columns with given step.
    - black_bit_value: 0 or 1 (which bit value will be encoded as black)
    - column_step: integer step for columns (e.g., 2 -> every 2nd column)
    Behavior:
      * If there are bits left: if bit == black_bit_value -> paint pixel black; else leave it unchanged.
      * If bits exhausted: paint remaining visited pixels black.
    Save result as <image_stem>_steg.png and return its Path.
    """
    lightened = Path(f"{image_stem}_lightened.png")
    out = Path(f"{image_stem}_steg.png")

    if not lightened.exists():
        raise FileNotFoundError(f"Lightened file not found: {lightened}")

    img = Image.open(lightened).convert("RGB")
    pixels = img.load()
    w, h = img.size

    bits = text_to_bits_flat(text)
    idx = 0

    for x in range(1, w, column_step):
        for y in range(h):
            if idx >= len(bits):
                pixels[x, y] = (0, 0, 0)
            else:
                if bits[idx] == black_bit_value:
                    pixels[x, y] = (0, 0, 0)
                else:
                    # leave pixel as is
                    pass
            idx += 1

    img.save(out)
    return out

def bits_to_text(bits_flat):
    """Convert flat list of bits into a string. Ignore last partial byte (<8 bits)."""
    chars = []
    for i in range(0, len(bits_flat), 8):
        byte = bits_flat[i:i+8]
        if len(byte) < 8:
            break
        s = ''.join(str(b) for b in byte)
        chars.append(chr(int(s, 2)))
    return ''.join(chars)

def extract_text_from_image(image_stem, black_bit_value, column_step=2):
    """
    Read <image_stem>_steg.png, scan columns with step, decode bits:
      - pixel == black => bit = black_bit_value
      - otherwise => bit = 1 - black_bit_value
    Then convert bits to text (ignore trailing partial byte).
    """
    steg = Path(f"{image_stem}_steg.png")
    if not steg.exists():
        raise FileNotFoundError(f"Stego image not found: {steg}")

    img = Image.open(steg).convert("RGB")
    pixels = img.load()
    w, h = img.size

    bits = []
    for x in range(1, w, column_step):
        for y in range(h):
            is_black = pixels[x, y] == (0, 0, 0)
            bits.append(black_bit_value if is_black else (1 - black_bit_value))

    return bits_to_text(bits)

# -------------------------
# CLI / main
# -------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Simple steganography by columns (PNG).")
    parser.add_argument("--mode", choices=("input", "output"), required=True,
                        help="'input' to embed text, 'output' to extract text")
    parser.add_argument("--image", required=True,
                        help="Base image name without extension (e.g. 'photo' for photo.png)")
    parser.add_argument("--black-bit", choices=("0", "1"), default="0",
                        help="Which bit value is represented by a black pixel (0 or 1). Default: 0")
    parser.add_argument("--step", type=int, default=2,
                        help="Column step (positive integer). Default: 2")
    return parser.parse_args()

def main():
    args = parse_args()
    image_stem = args.image
    black_bit = int(args.black_bit)
    step = args.step

    try:
        if args.mode == "input":
            src = Path(f"{image_stem}.png")
            if not src.exists():
                print(f"Source image does not exist: {src}")
                sys.exit(1)

            text = input("Enter text to embed: ")
            print("Lightening image...")
            lighten_image_min(image_stem)
            print("Embedding text...")
            out_path = embed_text_bits_into_image(text, image_stem, black_bit, step)
            print(f"Saved stego image: {out_path}")

            # remove temporary file
            temp = Path(f"{image_stem}_lightened.png")
            if temp.exists():
                try:
                    temp.unlink()
                    print("Temporary lightened file removed.")
                except Exception:
                    print("Warning: could not remove temporary file.")

        else:  # output
            print("Extracting text from stego image...")
            text = extract_text_from_image(image_stem, black_bit, step)
            print("---- Extracted text ----")
            print(text)
            print("------------------------")

    except FileNotFoundError as e:
        print("File error:", e)
        sys.exit(2)
    except Exception as e:
        print("Unexpected error:", e)
        sys.exit(3)

if __name__ == "__main__":
    main()
