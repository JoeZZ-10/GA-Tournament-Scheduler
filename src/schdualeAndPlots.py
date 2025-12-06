import io
import matplotlib.pyplot as plt
from PIL import Image
import math

def create_round_image(round_matches, round_number):
    # Create a round image
    # Increase width & height
    fig_width = 12  # width in inches
    fig_height = max(4, len(round_matches) * 1.0 + 1)  # height depends on number of matches
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis("off")

    # Header
    ax.text(0.05, 1.0, f"Round {round_number}", fontsize=18, fontweight="bold",
            ha="left", va="bottom", transform=ax.transAxes)

    # Column titles
    col_y = 0.92
    ax.text(0.05, col_y, "Teams", fontsize=14, fontweight="bold", ha="left")
    ax.text(0.5, col_y, "Venue", fontsize=14, fontweight="bold", ha="center")
    ax.text(0.95, col_y, "Date/Timeslot", fontsize=14, fontweight="bold", ha="right")

    # Matches
    for i, match in enumerate(round_matches):
        y = col_y - (i + 1) * 0.07
        teams_text = f"{match['home']} vs {match['away']}"
        venue_text = match['venue']
        date_text = f"{match['timeslot']}"

        ax.text(0.05, y, teams_text, fontsize=12, ha="left", va="center")
        ax.text(0.5, y, venue_text, fontsize=12, ha="center", va="center")
        ax.text(0.95, y, date_text, fontsize=12, ha="right", va="center")

    plt.tight_layout()

    # Save figure to a bytes buffer in memory with higher DPI
    buf = io.BytesIO()
    fig.savefig(buf, format='PNG', dpi=200)  # higher DPI for sharper image
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

    
def generate_all_round_images(schedule_individual):
    """
    Generate all round images in memory (PIL Images) without saving
    """
    images = []
    for i, round_matches in enumerate(schedule_individual.schedule, start=1):
        img = create_round_image(round_matches, i)
        images.append(img)
    return images

import math

def merge_images_grid(images, columns=4, max_width=3500, max_height=3500, output_file="Final_Schedule.png"):
    """
    Merge in-memory images into a grid and resize to fit max_width/max_height
    """
    num_rows = math.ceil(len(images) / columns)

    # Compute target width & height for each image
    target_width = max_width // columns
    target_height = max_height // num_rows

    resized_images = [im.resize((target_width, target_height), Image.Resampling.LANCZOS) for im in images]

    # Total size of final image
    total_width = target_width * columns
    total_height = target_height * num_rows

    combined_image = Image.new("RGB", (total_width, total_height), color=(255, 255, 255))

    # Paste images in grid
    for idx, im in enumerate(resized_images):
        row = idx // columns
        col = idx % columns
        x_offset = col * target_width
        y_offset = row * target_height
        combined_image.paste(im, (x_offset, y_offset))

    combined_image.save(output_file)
