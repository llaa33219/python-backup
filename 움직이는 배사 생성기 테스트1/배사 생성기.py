from tkinter import Tk, filedialog
from PIL import Image, ImageSequence
import base64
from io import BytesIO
import os

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def gif_to_svg(gif_path, output_folder):
    from PIL import Image, ImageSequence
    import base64
    from io import BytesIO
    import os

    def image_to_base64(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

    gif = Image.open(gif_path)
    frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]
    total_duration = sum(frame.info.get('duration', 100) for frame in frames) / 1000.0  # Total animation duration in seconds

    # Reverse the frames list before encoding to base64
    frames_base64 = [image_to_base64(frame) for frame in reversed(frames)]

    svg_images = "".join([
        f'<image id="frame{i}" xlink:href="data:image/png;base64,{base64_str}" x="0" y="0" '
        f'height="{gif.height}px" width="{gif.width}px" style="opacity:0;"/>'
        for i, base64_str in enumerate(frames_base64)
    ])

    # Adjust the animation setup for the reversed frames
    animations_css = "".join([
        f"""#frame{i} {{
            animation: play {total_duration}s steps(1) infinite;
            animation-delay: {-i * (total_duration / len(frames))}s;
        }}"""
        for i in range(len(frames))
    ])

    keyframes_css = f"""
    @keyframes play {{
        0%, 100% {{ opacity: 0; }}
        {"; ".join([f"{(100/len(frames))*i}% {{ opacity: 1; }}" for i in range(len(frames))])}
        {"; ".join([f"{(100/len(frames))*i}% {{ opacity: 0; }}" for i in range(1, len(frames)+1)])}
    }}
    """

    svg_content = f"""<svg width="{gif.width}px" height="{gif.height}px" viewBox="0 0 {gif.width} {gif.height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <style>
        {animations_css}
        {keyframes_css}
    </style>
    {svg_images}
    </svg>
    """
    output_path = os.path.join(output_folder, 'animated_svg.svg')
    with open(output_path, 'w') as file:
        file.write(svg_content)
    print(f'SVG file has been saved to: {output_path}')





def main():
    Tk().withdraw() # We don't want a full GUI, so keep the root window from appearing
    gif_path = filedialog.askopenfilename(title="Select a GIF file", filetypes=[("GIF files", "*.gif")])
    if not gif_path:
        print("No file selected.")
        return
    output_folder = filedialog.askdirectory(title="Select output folder")
    if not output_folder:
        print("No folder selected.")
        return
    gif_to_svg(gif_path, output_folder)

if __name__ == "__main__":
    main()
