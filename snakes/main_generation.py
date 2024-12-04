import os
import cv2
from skimage.metrics import structural_similarity as ssim
import sys
import snakes2_wrapper


def run_snake_image_generator(n_images, image_size, difficulty):
    # Create a mock of command-line arguments
    sys.argv = ["snakes2_wrapper.py", str(n_images), str(image_size), difficulty]

    snakes2_wrapper.main()


def load_images_from_folder(folder):
    """
    Loads all images from a specified folder and returns them in a dictionary.

    Args:
        folder (str): The path to the folder containing images.

    Returns:
        dict: A dictionary where keys are filenames and values are the corresponding grayscale images.
    """
    images = {}
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            images[filename] = img
    return images


def compare_and_delete_images(folder1, folder2, similarity_threshold=0.9):
    """
    Compares images from two folders and deletes images from the first folder if they are similar to any image in the second folder.

    Args:
        folder1 (str): The path to the first folder containing images to be compared and potentially deleted.
        folder2 (str): The path to the second folder containing images to compare against.
        similarity_threshold (float): The threshold for similarity (default is 0.9).

    Returns:
        None
    """
    images1 = load_images_from_folder(folder1)
    images2 = load_images_from_folder(folder2)

    for img1_name, img1 in images1.items():
        for img2_name, img2 in images2.items():
            if img1.shape == img2.shape:
                score, _ = ssim(img1, img2, full=True)
                if score >= similarity_threshold:
                    os.remove(os.path.join(folder1, img1_name))
                    print(
                        f"Deleted {img1_name} from {folder1} (similar to {img2_name} in {folder2}) with score {score}"
                    )


def process_all_subfolders(gen_base_path, orig_base_path, similarity_threshold=0.9):
    """
    Process all subfolders in the imgs directories and compare images.

    Args:
        gen_base_path (str): Base path to the generated images folder
        orig_base_path (str): Base path to the original images folder
        similarity_threshold (float): Threshold for image similarity
    """
    # Get the base imgs directories
    gen_imgs_path = os.path.join(gen_base_path, "imgs")
    orig_imgs_path = os.path.join(orig_base_path, "imgs")

    # Check if the directories exist
    if not os.path.exists(gen_imgs_path) or not os.path.exists(orig_imgs_path):
        print("One or both of the imgs directories don't exist")
        return

    # Iterate through all subfolders in the generated imgs directory
    for subfolder in os.listdir(gen_imgs_path):
        gen_subfolder_path = os.path.join(gen_imgs_path, subfolder)
        orig_subfolder_path = os.path.join(orig_imgs_path, subfolder)

        # Check if both subfolders exist and are directories
        if os.path.isdir(gen_subfolder_path) and os.path.isdir(orig_subfolder_path):
            print(f"Processing subfolder: {subfolder}")
            compare_and_delete_images(
                gen_subfolder_path, orig_subfolder_path, similarity_threshold
            )


if __name__ == "__main__":
    n_images = int(sys.argv[1])
    image_size = int(sys.argv[2])
    difficulty = sys.argv[3]
    similarity_threshold = float(sys.argv[4])

    difficulty_settings = {
        "easy": "curv_baseline",
        "medium": "curv_contour_length_9",
        "hard": "curv_contour_length_14",
    }

    # Get paths from get_parameters
    sys.path.append("../snakes/")
    gen_path = f"../data/{difficulty}_{n_images}_{image_size}/{difficulty_settings[difficulty]}/imgs/0/"
    orig_path = f"../data/lra_release/lra_release/pathfinder{image_size}/{difficulty_settings[difficulty]}/imgs/0/"

    # Generate images
    run_snake_image_generator(n_images, image_size, difficulty)

    # Clean duplicates
    compare_and_delete_images(gen_path, orig_path, similarity_threshold)
    # process_all_subfolders(gen_path, orig_path, similarity_threshold)
