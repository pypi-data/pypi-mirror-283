import os
import numpy as np
from PIL import Image
import zipfile
import tarfile
from datetime import datetime
from .augmentations import *

# Mapping of augmentation methods to their descriptions
AUGMENTATION_DESCRIPTIONS = {
    1: 'Horizontal Flip',
    2: 'Vertical Flip',
    3: 'Rotate 90 Degrees',
    4: 'Random Rotation',
    5: 'Random Shear',
    6: 'Random Crop',
    7: 'Apply Gaussian Blur',
    8: 'Apply Exposure',
    9: 'Apply Random Noise',
    10: 'Cutout',
    11: 'Mosaic',
    12: 'Color Jitter',
    13: 'Rotate with Bounding Box',
    14: 'CLAHE Equalization',
    15: 'Random Zoom',
    16: 'Channel Shuffle',
    17: 'Histogram Equalization'
}

def get_augmentation_descriptions():
    """Returns a dictionary of augmentation method numbers to descriptions."""
    return AUGMENTATION_DESCRIPTIONS

def get_custom_augmented_images(input_dir, output_dir, user_choices):
    image_augmentation_functions = {
        1: flip_horizontal_image,
        2: flip_vertical_image,
        3: rotate_image,
        4: random_rotation,
        5: random_shear,
        6: random_crop,
        7: apply_blur,
        8: apply_exposure,
        9: apply_random_noise,
        10: cutout,
        11: mosaic,
        12: color_jitter,
        13: rotate_with_bounding_box,
        14: clahe_equalization,
        15: random_zoom,
        16: channel_shuffle,
        17: histogram_equalization
    }

    image_augmentation_names = {
        1: 'horizontally_flipped',
        2: 'vertically_flipped',
        3: '90_rotated',
        4: 'random_rotated',
        5: 'random_sheared',
        6: 'random_cropped',
        7: 'blurred',
        8: 'exposed',
        9: 'random_noised',
        10: 'cutout',
        11: 'mosaic',
        12: 'color_jittered',
        13: 'bounding_box_rotated',
        14: 'clahe_equalized',
        15: 'random_zoomed',
        16: 'channel_shuffled',
        17: 'histogram_equalized'
    }

    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        original_image = np.array(Image.open(os.path.join(input_dir, filename)))
        for method in user_choices:
            method_name = image_augmentation_names.get(method, f'unknown_{method}')
            method_function = image_augmentation_functions.get(method)

            if method_function is not None:
                augmented_image = method_function(original_image)
                Image.fromarray(augmented_image).save(os.path.join(output_dir, f'{method_name}_{filename}'))
                print(f'{method_name} augmentation done for {filename}')
            else:
                print(f'Error: Method {method} not found.')

def apply_all_augmentations(input_dir, output_dir):
    all_methods = list(range(1, 18))
    get_custom_augmented_images(input_dir, output_dir, all_methods)

def create_zip(zip_filename, output_dir):
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for filename in os.listdir(output_dir):
            image_path = os.path.join(output_dir, filename)
            zip_file.write(image_path, filename)

def create_tar_gz(output_dir, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=os.path.relpath(file_path, output_dir))

def create_tar_gz_with_timestamp(output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f'augmented_images_{timestamp}.tar.gz'
    create_tar_gz(output_dir, output_filename)
    
def welcome():
    print('Welcome into the Amplify Verse\nThanks for installing me my lord!!')