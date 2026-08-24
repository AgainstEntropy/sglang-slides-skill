# /// script
# requires-python = ">=3.10"
# dependencies = ["qrcode[pil]"]
# ///
"""Generate a brand-styled QR png.  Usage: uv run make_qr.py <url> <out.png>"""

import sys

import qrcode

url, out = sys.argv[1], sys.argv[2]
qr = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="#1A1A1A", back_color="white")  # INK on white
img.save(out)
print(f"wrote {out} ({img.size[0]}x{img.size[1]}) -> {url}")
