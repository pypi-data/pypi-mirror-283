from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
import cv2

def flip_horizontal_image(image):
    img = Image.fromarray(image)
    return np.array(ImageOps.mirror(img))

def flip_vertical_image(image):
    img = Image.fromarray(image)
    return np.array(ImageOps.flip(img))

def rotate_image(image, angle=90):
    img = Image.fromarray(image)
    return np.array(img.rotate(angle))

def random_rotation(image):
    angle = np.random.randint(1, 360)
    img = Image.fromarray(image)
    return np.array(img.rotate(angle))

def random_shear(image, shear_factor=0.2):
    img = Image.fromarray(image)
    shear_factor = np.random.uniform(-shear_factor, shear_factor)
    return np.array(img.transform(img.size, Image.AFFINE, (1, shear_factor, 0, 0, 1, 0), resample=Image.BICUBIC))

def random_crop(image, crop_percent=0.2):
    img = Image.fromarray(image)
    width, height = img.size
    left = np.random.randint(0, int(crop_percent * width))
    upper = np.random.randint(0, int(crop_percent * height))
    right = width - np.random.randint(0, int(crop_percent * width))
    lower = height - np.random.randint(0, int(crop_percent * height))
    return np.array(img.crop((left, upper, right, lower)))

def apply_blur(image, radius=2):
    img = Image.fromarray(image)
    return np.array(img.filter(ImageFilter.GaussianBlur(radius=radius)))

def apply_exposure(image, exposure_factor=1.5):
    img = Image.fromarray(image)
    enhancer = ImageEnhance.Brightness(img)
    return np.array(enhancer.enhance(exposure_factor))

def apply_random_noise(image, noise_factor=20):
    img = Image.fromarray(image)
    
    num_channels = len(img.getbands())
    noise = [np.random.normal(scale=noise_factor, size=img.size[::-1]) for _ in range(num_channels)]
    noise = [np.clip(channel, 0, 255) for channel in noise]
    noisy_img = np.stack(noise, axis=-1).astype(np.uint8)
    noisy_img = np.clip(np.array(img) + noisy_img, 0, 255)
    
    return noisy_img

def cutout(image, cutout_size=100):
    img = Image.fromarray(image)
    width, height = img.size
    left = np.random.randint(0, width - cutout_size)
    upper = np.random.randint(0, height - cutout_size)
    right = left + cutout_size
    lower = upper + cutout_size
    img.paste((0, 0, 0), (left, upper, right, lower))
    return np.array(img)

def mosaic(image, mosaic_size=5):
    img = Image.fromarray(image)
    width, height = img.size
    for _ in range(mosaic_size):
        left = np.random.randint(0, width)
        upper = np.random.randint(0, height)
        right = np.random.randint(left, width)
        lower = np.random.randint(upper, height)
        img.crop((left, upper, right, lower)).paste(img.crop((left, upper, right, lower)).resize((1, 1)))
    return np.array(img)

def color_jitter(image, brightness_factor=0.5, contrast_factor=0.5, saturation_factor=0.5, hue_factor=0.5):
    img = Image.fromarray(image)
    
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1 + brightness_factor * np.random.uniform(-1, 1))
    
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1 + contrast_factor * np.random.uniform(-1, 1))
    
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1 + saturation_factor * np.random.uniform(-1, 1))
    
    img = img.convert('HSV')
    img = np.array(img)
    img[:, :, 0] = (img[:, :, 0] + hue_factor * 255) % 256
    img = Image.fromarray(img, 'HSV').convert('RGB')
    
    return np.array(img)

def rotate_with_bounding_box(image, angle=30):
    img = Image.fromarray(image)
    rotated_img = img.rotate(angle, resample=Image.BICUBIC, center=(img.width // 2, img.height // 2))
    return np.array(rotated_img)

def clahe_equalization(image, clip_limit=2.0, grid_size=(8, 8)):
    img = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
    img[:, :, 0] = clahe.apply(img[:, :, 0])
    img = cv2.cvtColor(img, cv2.COLOR_LAB2RGB)
    return img

def random_zoom(image, zoom_range=(0.8, 1.2)):
    img = Image.fromarray(image)
    zoom_factor = np.random.uniform(*zoom_range)
    new_size = tuple(int(dim * zoom_factor) for dim in img.size)
    img = img.resize(new_size, Image.BICUBIC)
    return np.array(img)

def channel_shuffle(image):
    img = Image.fromarray(image)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    channels = list(img.split())
    np.random.shuffle(channels)
    shuffled_img = Image.merge(img.mode, channels)
    return np.array(shuffled_img)

def histogram_equalization(image):
    img = Image.fromarray(image)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img = ImageOps.equalize(img)
    return np.array(img)
