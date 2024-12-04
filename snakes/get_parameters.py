def get_parameters(image_size, difficulty):
    # Define all parameter sets
    params = {
        (32, "hard"): {
            "window_size": [32, 32],
            "contour_length": 14,
            "paddle_margin_list": [1],
            "padding": 1,
            "paddle_length": 2,
            "marker_radius": 1.5,
            "paddle_thickness": 0.5,
            "antialias_scale": 2,
            "seed_distance": 7,
            "continuity": 1.0,
            "snake_contrast_list": [2],
            "paddle_contrast_list": [0.75],
        },
        (128, "easy"): {
            "window_size": [128, 128],
            "contour_length": 6,
            "paddle_margin_list": [2, 3],
            "padding": 1,
            "paddle_length": 5,
            "marker_radius": 3,
            "paddle_thickness": 1.0,
            "antialias_scale": 2,
            "seed_distance": 20,
            "continuity": 1.8,
            "snake_contrast_list": [0.9],
        },
        (128, "medium"): {
            "window_size": [128, 128],
            "contour_length": 9,
            "num_distractor_snakes": 20,  # Fixed value
            "paddle_margin_list": [2, 3],
            "padding": 1,
            "marker_radius": 3,
            "paddle_thickness": 1.5,
            "antialias_scale": 2,
            "seed_distance": 20,
            "continuity": 1.8,
            "snake_contrast_list": [0.9],
        },
        (128, "hard"): {
            "window_size": [128, 128],
            "contour_length": 14,
            "num_distractor_snakes": 20,  # Fixed value
            "paddle_margin_list": [2, 3],
            "padding": 1,
            "marker_radius": 3,
            "paddle_thickness": 1.5,
            "antialias_scale": 2,
            "seed_distance": 20,
            "continuity": 1.8,
            "snake_contrast_list": [0.9],
        },
        (256, "easy"): {
            "window_size": [256, 256],
            "contour_length": 6,
            "paddle_margin_list": [3],
            "marker_radius": 5,
            "paddle_thickness": 2,
            "paddle_length": 5,
            "antialias_scale": 2,
            "continuity": 1.8,
            "snake_contrast_list": [1.0],
        },
        (256, "medium"): {
            "window_size": [256, 256],
            "contour_length": 9,
            "num_distractor_snakes": 7,  # Fixed value
            "paddle_margin_list": [3],
            "marker_radius": 5,
            "paddle_thickness": 2,
            "paddle_length": 5,
            "antialias_scale": 2,
            "continuity": 1.8,
            "snake_contrast_list": [1.0],
        },
        (256, "hard"): {
            "window_size": [256, 256],
            "contour_length": 14,
            "paddle_margin_list": [3],
            "marker_radius": 5,
            "paddle_thickness": 2,
            "paddle_length": 5,
            "antialias_scale": 2,
            "continuity": 1.8,
            "snake_contrast_list": [1.0],
        },
    }

    # Get the base parameters for the specified size and difficulty
    base_params = params.get((image_size, difficulty))
    if not base_params:
        raise ValueError(
            f"No parameters found for size={image_size} and difficulty={difficulty}"
        )

    base_params["distractor_length"] = base_params["contour_length"] // 3

    # Set num_distractor_snakes if not explicitly defined
    if "num_distractor_snakes" not in base_params:
        if image_size == 32:
            base_params["num_distractor_snakes"] = (
                20 // base_params["distractor_length"]
            )
        elif image_size == 128:
            base_params["num_distractor_snakes"] = (
                35 // base_params["distractor_length"]
            )
        elif image_size == 256:
            base_params["num_distractor_snakes"] = (
                30 // base_params["distractor_length"]
            )

    return base_params
