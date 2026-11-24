#!/usr/bin/env python3
"""news-23 b92 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

SRC_NAME = "entry.png"
MIN_BYTES = 10000
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def validate_png(path):
    """Parse the PNG header manually (struct) and walk every chunk, checking CRCs."""
    with open(path, "rb") as fh:
        data = fh.read()
    if len(data) < MIN_BYTES:
        return fail("entry.png too small: %d bytes" % len(data))
    if len(data) > MAX_BYTES:
        return fail("entry.png too large: %d bytes" % len(data))
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("bad PNG signature")
    off = 8
    first = True
    saw_idat = False
    idat_bytes = 0
    while off < len(data):
        if off + 8 > len(data):
            return fail("truncated chunk header")
        (length,) = struct.unpack(">I", data[off:off + 4])
        ctype = data[off + 4:off + 8]
        if off + 12 + length > len(data):
            return fail("truncated chunk %r" % ctype)
        payload = data[off + 8:off + 8 + length]
        (stored_crc,) = struct.unpack(">I", data[off + 8 + length:off + 12 + length])
        if binascii.crc32(ctype + payload) & 0xFFFFFFFF != stored_crc:
            return fail("CRC mismatch in chunk %r" % ctype)
        if first:
            if ctype != b"IHDR" or length != 13:
                return fail("first chunk must be a 13-byte IHDR")
            w, h, depth, ctype_code = struct.unpack(">IIBB", payload[:10])
            if (w, h) != (1024, 1024):
                return fail("IHDR is %dx%d, expected 1024x1024" % (w, h))
            if depth != 8 or ctype_code not in (2, 6):
                return fail("unexpected IHDR bit depth / colour type")
            first = False
        if ctype == b"IDAT":
            saw_idat = True
            idat_bytes += length
        if ctype == b"IEND":
            if length != 0:
                return fail("IEND must be empty")
            if off + 12 + length != len(data):
                return fail("trailing data after IEND")
            break
        off += 12 + length
    else:
        return fail("no IEND chunk found")
    if not saw_idat or idat_bytes < 1000:
        return fail("no usable IDAT payload")
    return data


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    if out_dir_abs == here or out_dir_abs.startswith(here + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo: %s" % out_dir)
    # Same check on the real path, so a symlink into the repo cannot slip past.
    real_out = os.path.realpath(out_dir_abs)
    real_here = os.path.realpath(here)
    if real_out == real_here or real_out.startswith(real_here + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR resolves inside the repo: %s" % out_dir)
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory: %s" % out_dir)
    data = validate_png(src)
    if isinstance(data, int):
        return data
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, SRC_NAME)
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source image")
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        back = fh.read()
    if back != data:
        return fail("re-read output does not match source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
