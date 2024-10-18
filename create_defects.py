import os
import random
from PIL import Image, ImageDraw
from icecream import ic


def add_random_red_dots(image, num_dots):

    draw = ImageDraw.Draw(image)

    width, height = image.size

    for _ in range(num_dots):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        dot_size = 8
        draw.ellipse(
            (x - dot_size, y - dot_size, x + dot_size, y + dot_size), fill="red"
        )

    return image


def process_images(input_dir, output_dir, percentage=0.1):

    jpg_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".jpg")]
    print(f"num images in input_dir: {len(jpg_files)}")

    num_images_to_modify = max(1, int(len(jpg_files) * percentage))

    selected_images = random.sample(jpg_files, num_images_to_modify)

    for image_file in selected_images:

        image_path = os.path.join(input_dir, image_file)
        image = Image.open(image_path)

        num_dots = random.randint(1, 5)
        modified_image = add_random_red_dots(image, num_dots)

        output_path = os.path.join(output_dir, image_file)
        modified_image.save(output_path)

    print(
        f"Processed and saved {num_images_to_modify} images with red dots to '{output_dir}'."
    )


if __name__ == "__main__":
    input_dir = "nominal_processed_by_hugo"
    output_dir = "testing_images"

    os.makedirs(output_dir, exist_ok=True)

    process_images(input_dir, output_dir)
