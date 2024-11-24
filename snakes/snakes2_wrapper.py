import time
import sys
import os
import argparse
import snakes2


class Args:
    def __init__(
        self,
        contour_path="./contour",
        batch_id=0,
        n_images=5,
        window_size=[300, 300],
        padding=22,
        antialias_scale=4,
        LABEL=1,
        seed_distance=27,
        marker_radius=3,
        contour_length=15,
        distractor_length=5,
        num_distractor_snakes=6,
        snake_contrast_list=[1.0],
        use_single_paddles=True,
        max_target_contour_retrial=4,
        max_distractor_contour_retrial=4,
        max_paddle_retrial=2,
        continuity=1.4,
        paddle_length=5,
        paddle_thickness=1.5,
        paddle_margin_list=[4],
        paddle_contrast_list=[1.0],
        pause_display=False,
        save_images=True,
        save_metadata=True,
        segmentation_task=False,
    ):

        # Update the instance dictionary with local variables, excluding 'self'
        self.__dict__.update(locals())
        del self.__dict__["self"]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate snake images")

    # Required parameters
    parser.add_argument("n_images", type=int, help="Number of images to generate")
    parser.add_argument("image_size", type=int, help="Size of the output images")
    parser.add_argument(
        "difficulty",
        choices=["easy", "intermediate", "hard"],
        help="Difficulty level of the images",
    )

    # Optional parameters with default values from Args.__init__
    args_defaults = Args().__dict__
    for key, value in args_defaults.items():
        if key not in ["n_images", "window_size"]:  # Exclude required parameters
            parser.add_argument(f"--{key}", default=value, type=type(value))

    return parser.parse_args()


def get_difficulty_params(difficulty, size):
    difficulty_settings = {
        "easy": {"dataset_subpath": "curv_baseline", "contour_length": 6},
        "intermediate": {
            "dataset_subpath": "curv_contour_length_9",
            "contour_length": 9,
        },
        "hard": {"dataset_subpath": "curv_contour_length_14", "contour_length": 14},
    }

    size_seetings_num_distractor_snakes = {
        32: 20,
        128: 35,
        256: 30
    }
    return difficulty_settings[difficulty], size_seetings_num_distractor_snakes[size]


def main():
    parsed_args = parse_arguments()

    args = Args()

    # Update main parameters with parsed arguments
    args.n_images = parsed_args.n_images
    args.window_size = [parsed_args.image_size, parsed_args.image_size]

    # Get parameters based on difficulty level
    difficulty_params, size_seetings = get_difficulty_params(parsed_args.difficulty, parsed_args.image_size)

    # Configure parameters based on difficulty
    args.contour_length = difficulty_params["contour_length"]
    args.distractor_length = args.contour_length / 3
    args.num_distractor_snakes = size_seetings / args.distractor_length

    # General settings
    args.padding = 1
    args.marker_radius = 3
    args.seed_distance = 20
    args.paddle_thickness = 1.5
    args.antialias_scale = 2
    args.continuity = 1.8
    args.paddle_margin_list = [2, 3]
    args.snake_contrast_list = [0.9]
    args.use_single_paddles = False

    # dataset_root = './data/new_128_2'
    dataset_name = "_".join(
        [parsed_args.difficulty, str(parsed_args.n_images), str(parsed_args.image_size)]
    )
    dataset_root = os.path.join('../data', dataset_name)
    os.makedirs(dataset_root, exist_ok=True)
    args.contour_path = os.path.join(dataset_root, difficulty_params["dataset_subpath"])

    # Start image generation
    t = time.time()
    snakes2.from_wrapper(args)
    elapsed = time.time() - t

    print(f"Generated {args.n_images} images")
    print(f"Elapsed time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
