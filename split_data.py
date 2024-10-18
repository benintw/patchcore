import os
import random
import shutil
from PIL import Image, ImageDraw
from icecream import ic


def add_random_dots(image, num_dots):

    draw = ImageDraw.Draw(image)

    width, height = image.size

    for _ in range(num_dots):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        dot_size = 8

        color = random.choice(["black", "white"])

        draw.ellipse(
            (x - dot_size, y - dot_size, x + dot_size, y + dot_size), fill=color
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
        modified_image = add_random_dots(image, num_dots)

        output_path = os.path.join(output_dir, image_file)
        modified_image.save(output_path)

    print(
        f"Processed and saved {num_images_to_modify} images with red dots to '{output_dir}'."
    )


def split_data(nominal_img_dir, training_dir, testing_dir, training_split) -> None:

    good_dir = os.path.join(testing_dir, "good")
    defect_dir = os.path.join(testing_dir, "defect")

    # Remove existing directories if they exist to overwrite them
    if os.path.exists(training_dir):
        shutil.rmtree(training_dir)
    if os.path.exists(testing_dir):
        shutil.rmtree(testing_dir)

    # Ensure directories exist
    os.makedirs(training_dir, exist_ok=True)
    os.makedirs(testing_dir, exist_ok=True)
    os.makedirs(good_dir, exist_ok=True)
    os.makedirs(defect_dir, exist_ok=True)

    nominal_img_names = [f for f in os.listdir(nominal_img_dir) if f.endswith(".jpg")]
    TOTAL_IMGS = len(nominal_img_names)
    ic(TOTAL_IMGS)

    selected_imgs = random.sample(nominal_img_names, int(TOTAL_IMGS * training_split))
    training_set = set(nominal_img_names) - set(selected_imgs)

    # Save training images to 'training_imgs' directory
    for img_name in training_set:
        img_path = os.path.join(nominal_img_dir, img_name)
        img_output_path = os.path.join(training_dir, img_name)
        img = Image.open(img_path)
        img.save(img_output_path)
    print(f"{len(training_set)} Training images saved to '{training_dir}'")

    # Save the randomly selected images AND then add 5 defected images
    for img_name in selected_imgs:
        img_path = os.path.join(nominal_img_dir, img_name)
        img_output_path = os.path.join(good_dir, img_name)
        img = Image.open(img_path)
        img.save(img_output_path)
    process_images(nominal_img_dir, defect_dir, percentage=training_split)
