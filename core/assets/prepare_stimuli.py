import os
import requests
import pathlib
import cairosvg
from collections import Counter
from PIL import Image
import numpy as np

try:
    import scour
    import subprocess
    skip_simplify = False
except ModuleNotFoundError:
    print("Scour not found, skipping simplification.")
    skip_simplify = True


def download_svgs_from_file(file_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    current_title = None
    counter = 1

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Skip lines starting with '##'
            if line.startswith("##"):
                continue

            # Detect section title
            if line.startswith("# "):
                current_title = line[2:].strip().replace(" ", "_")
                counter = 1
                continue

            # If it's an URL, download the svg
            if line.startswith("http") and current_title:
                try:
                    filename = f"{current_title}_{counter:02d}.svg"
                    filepath = os.path.join(output_dir, filename)
                    stripped = filepath.replace(".svg", "_strip.svg")
                    if not os.path.isfile(filepath) and not os.path.isfile(stripped):
                        response = requests.get(line)
                        response.raise_for_status()

                        with open(filepath, "wb") as svg_file:
                            svg_file.write(response.content)

                        print(f"Downloaded: {filename}")
                    else:
                        print(f"Skipped {current_title}_{counter:02d}.svg")

                    counter += 1
                except Exception as e:
                    print(f"Failed to download {line}: {e}")


def convert_svg_to_png(file: str):
    png_path =  file.as_posix().replace(".svg", ".png")
    try:
        cairosvg.svg2png(url=file.as_posix(), write_to=png_path, output_width=400)
        print(f"Converted: {file} → {os.path.basename(png_path)}")
    except Exception as e:
        print(f"Failed to convert {file}: {e}")


def multiplicative_recolor(input_file, output_file, new_color=(255, 255, 255), luminance=None):

    def increase_luminance(img, target_lum=0.85, contrast_factor=0.75, margin=0.075, min_lum=0.1, max_lum=0.95):
        """
        img: RGBA or RGB PIL image
        factor: multiplicative luminance increase (>1 to brighten)
        margin: fraction of 0-1 to avoid clipping to pure black/white
        """
        img = img.convert("RGBA")
        data = np.array(img, dtype=float) / 255.0

        r, g, b, a = data[...,0], data[...,1], data[...,2], data[...,3]

        # Mask to only non-transparent pixels
        mask = (a > 0) & ~((r < 20 / 255.0) & (g < 20 / 255.0) & (b < 20 / 255.0)) & ~((r > 230 / 255.0) & (g > 230 / 255.0) & (b > 230 / 255.0))

        print(mask.sum())
        # Current luminanc
        def get_lum(r, g, b):
            return 0.299*r + 0.587*g + 0.114*b # 0.333*r + 0.333*g + 0.333*b #
        lum = get_lum(r, g, b)
        lum_masked = lum[mask]
        print(lum_masked)
        # Compute offset to lift minimum luminance

        # Apply min and max luminance bounds
        current_min = np.min(lum_masked)
        current_max = np.max(lum_masked)

        # Compute offsets for min and max
        min_offset = max(0, min_lum - current_min)
        max_scale = (max_lum - min_lum) / (current_max - current_min + 1e-8)

        # First lift minimum
        r[mask] += min_offset
        g[mask] += min_offset
        b[mask] += min_offset

        # Scale to fit max_lum
        r[mask] = (r[mask] - min_lum) * max_scale + min_lum
        g[mask] = (g[mask] - min_lum) * max_scale + min_lum
        b[mask] = (b[mask] - min_lum) * max_scale + min_lum

        # Adaptive luminance scaling to target mean
        #lum_scaled = 0.299*r + 0.587*g + 0.114*b
        #mean_lum = np.mean(lum_scaled[mask])
        #factor = target_lum / (mean_lum + 1e-8)
        #r[mask] *= factor
        #g[mask] *= factor
        #b[mask] *= factor

        # Contrast adjustment
        lum_scaled =  get_lum(r, g, b)
        lum_mean = np.mean(lum_scaled[mask])
        # Contrast normalization: move pixel values towards mean
        lum_mean = np.mean(lum_scaled[mask])
        r[mask] = (r[mask] - lum_mean) * contrast_factor + lum_mean
        g[mask] = (g[mask] - lum_mean) * contrast_factor + lum_mean
        b[mask] = (b[mask] - lum_mean) * contrast_factor + lum_mean

        # Clip to avoid clipping to black/white
        r[mask] = np.clip(r[mask], margin, 1 - margin)
        g[mask] = np.clip(g[mask], margin, 1 - margin)
        b[mask] = np.clip(b[mask], margin, 1 - margin)

        data[...,0], data[...,1], data[...,2] = r, g, b

        return Image.fromarray((data*255).astype(np.uint8), "RGBA")

    img = Image.open(input_file).convert("RGBA")
    bbox = img.getbbox()  # bounding box of non-transparent pixels
    img = img.crop(bbox)

    target_size = (400, 400)
    img = img.copy()
    img.thumbnail(target_size, Image.Resampling.LANCZOS)  # keeps aspect ratio
    new_img = Image.new("RGBA", target_size, (0, 0, 0, 0)) # transparent background
    left = (target_size[0] - img.width) // 2
    top = (target_size[1] - img.height) // 2

    new_img.paste(img, (left, top))

    img = new_img

    if luminance is not None:
        img = increase_luminance(img, target_lum=luminance[0], contrast_factor=luminance[1], min_lum=luminance[2])

    data = np.array(img, dtype=float)
    gray = np.array(img.convert("L"), dtype=float)  # convert to grayscale (1 channel)
    data[..., :3] = np.stack([gray]*3, axis=-1)    #

    r, g, b, a = data[..., 0], data[..., 1], data[..., 2], data[..., 3]


    # Mask: ignore transparent, black, white
    mask = (a > 0) & ~((r < 20) & (g < 20) & (b < 20)) & ~((r > 235) & (g > 235) & (b > 235))

    factors = np.array(new_color) / 255.0


    # Apply multiplicative recoloring only inside mask
    for i in range(3):
        data[..., i][mask] = data[..., i][mask] * factors[i]

    data = np.clip(data, 0, 255).astype(np.uint8)


    Image.fromarray(data, "RGBA").save(output_file, "PNG")
    print(f"Recolored (multiplicative): {os.path.basename(output_file)}")

if __name__ == "__main__":

    base_dir = pathlib.Path(__file__).parent.resolve()
    input_file = base_dir / "stimuli.txt"
    output_folder = base_dir / "stimuli_svg"
    download_svgs_from_file(str(input_file), str(output_folder))

    for file in output_folder.glob("*.svg"):
        if "_strip" not in file.name:
            subprocess.run([
            "scour",
            "-i", file,
            "-o", file.as_posix().replace(".svg", "_strip.svg"),
            "--enable-viewboxing",
            "--enable-id-stripping",
            "--enable-comment-stripping",
            "--shorten-ids"
            ], check=True)
            print(f"Optimized: {file}")
            if os.path.isfile(file.as_posix().replace(".svg", "_strip.svg")):
                file.unlink()

    for file in output_folder.glob("*_strip.svg"):
        convert_svg_to_png(file)

    for file in output_folder.glob("*_strip.png"):
        multiplicative_recolor(file.as_posix(), file.as_posix().replace("_strip.png", "_rec.png"), new_color=(255, 255, 255), luminance=(0.85, 1.35, 0.6))
        multiplicative_recolor( file.as_posix().replace("_strip.png", "_rec.png"), file.as_posix().replace("_strip.png", "_test.png"),
        new_color=(60 + 15, 109 + 15, 86 + 15), luminance=None)
