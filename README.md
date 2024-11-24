# Pathfinder-Listops

## Project Structure

```
Pathfinder-Listops/
│
├── data/
│   |── hard_5_128/
│   |    └── [Dataset files]   # Example dataset after image generation
│   |
|   └── lra_release/           # Official dataset
│
├── lra_benchmark/
│   └── pathfinder.py          # Script for pathfinding algorithms
│
├── notebooks/
│   └── pathfinder.ipynb       # Notebook for experiments
│
├── snakes/
│   ├── snakes_wrapper.py      # Wrapper functions for snake operations
│   ├── snakes.py              # Core snake logic and functions
│   ├── snakes2_wrapper.py     # Additional wrapper functions for snake
│   └── snakes2.py             # Extended snake logic and functions
│
├── poetry.lock                # Dependency lock file for Poetry
├── pyproject.toml             # Project dependencies
└── README.md                  # Project overview and documentation
```

### Dependencies
For installing all needed dependencies run:

```
poetry install
```

### How to generate images:

```
python3 snakes/snakes2_wrapper_new.py <n_images> <image_size> <difficulty>
```

Example with 100 images with window size [128x128] in *hard* modification:

```
python3 snakes/snakes2_wrapper_new.py 100 128 hard
```

The script creates a directory for saving images `data/hard_100_128`

The special parameters for each modification you can find below.


## Info about files

### LRA benchmarks code

Link to [lra_benchmarks](https://github.com/google-research/long-range-arena/blob/main/lra_benchmarks/data/pathfinder.py)
    
File ```lra_benchmarks_data/pathfinder.py```

Parameters for generation

For all versions of the dataset, three levels of complexity are used, which are determined using the parameter ```file_pattern```:

- easy: curv_baseline
- intermediate: curv_contour_length_9
- hard: curv_contour_length_14

The function of code is below:

```
def _split_generators(self, dl_manager):
"""Downloads the data and defines the splits."""

return [
    tfds.core.SplitGenerator(
        name='easy', gen_kwargs={'file_pattern': 'curv_baseline'}),
    tfds.core.SplitGenerator(
        name='intermediate',
        gen_kwargs={'file_pattern': 'curv_contour_length_9'}),
    tfds.core.SplitGenerator(
        name='hard', gen_kwargs={'file_pattern': 'curv_contour_length_14'})
]
```

Pathfinder **32 Hard**

- window_size: [32, 32]
- contour_length: (14 - hard modification)
- distractor_length = contour_length // 3
- num_distractor_snakes: 20 // distractor_length
- paddle_margin_list: [1]
- padding: 1
- paddle_length: 2
- marker_radius: 1.5
- paddle_thickness: 0.5
- antialias_scale: 2
- seed_distance: 7
- continuity: 1.0
- snake_contrast_list: [2]
- paddle_contrast_list: [0.75]

Pathfinder **128 Easy & Hard** 

- window_size: [128, 128]
- contour_length: (6 - easy, 9 - intermediate, 14 - hard modification)
- distractor_length: contour_length / 3
- num_distractor_snakes: 35 / distractor_length
- paddle_margin_list: [2, 3]
- padding: 1
- marker_radius: 3
- paddle_thickness: 1.5
- antialias_scale: 2
- seed_distance: 20
- continuity: 1.8 (from 1.8 to 0.8, with steps of 66%)
- snake_contrast_list: [0.9]

Pathfinder **256 Easy & Hard**

- window_size: [256, 256]
- contour_length: (6 - easy, 9 - intermediate, 14 - hard modification)
- distractor_length: contour_length / 3
- num_distractor_snakes: 30 / distractor_length
- paddle_margin_list: [3]
- marker_radius: 5
- paddle_thickness: 2
- antialias_scale: 2
- continuity: 1.8
- snake_contrast_list: [1.0]

***

### Pathfinder

Links to [Pathfinder](https://github.com/drewlinsley/pathfinder/tree/master) and [small paper about](https://openreview.net/pdf?id=06p6DzsKQcg)
    
- About ```snakes.py```

    Script draw train image with "snakes" and target image (with correct "snake").

    If the script is run directly, it calls the test function to demonstrate its functionality.

    The main algorithm of 'snakes' generation:

    **ALGORITHM**
    ```
    1. compute initial point
        current_start = translate(last_endpoint, last_orientation, dilation+1)
    2. draw current_endpoint (distance = line_length + dilation)
        compute current_orientation
        M' <--- dilate(M, dilation+2)
        sample endpoint using M'
        trial_count += 1
    3. compute line and mask
        l_current, m_current = draw_line_n_mask(translate(current_start, current_orientation, dilation), current_endpoint, dilation)
    4. check if max(M + m_current) > 2
            yes -> check if retrial_count > max_count
                yes -> return with failure flag
                no -> goto 2
            no -> goto 5
    5. draw image I += l_current
    6. draw mask M = max(M, m_last)
    7. m_last = m_current.copy()
    8. retrial_count = 0
    ```

    About functions in script:

    - **save_metadata**: Saves metadata about the generated images to a file.
    - **accumulate_meta**: Collects metadata information about each generated image.
    - **make_many_snakes**: Generates multiple "snakes" (curved lines) on an image. It uses helper functions to create these patterns and ensures they don't overlap excessively.
    - **find_available_coordinates**: Finds coordinates on the image where new segments can be drawn without overlapping existing ones.
    - **make_snake**: Creates a single snake by drawing segments sequentially.
    - **seed_snake** and **extend_snake**: Helper functions to start a snake and extend it by adding more segments.
    - **get_coords_cmf**: Calculates possible coordinates for the next segment of a snake based on continuity and available space.
    - **draw_line_n_mask**: Draws a line segment and its corresponding mask on the image.
    - **binary_dilate_custom** and **generate_dilation_struct**: Perform image dilation operations to help with collision detection and spacing.
    - **translate_coord** and **flip_by_pi**: Utility functions for coordinate transformations. Orientation is in radian.
    - **gray2red** and **gray2gray**: Convert grayscale images to RGB with specific color channels.
    - **imsum**: Combines two images.
    - **test**: A test function to generate and display a sample image with snakes.
    - **from_wrapper**: A function to generate a batch of images based on provided arguments.

- About ```snakes_wrapper.py```

    Imports necessary modules and the ```snakes``` module. It defines an ```Args``` class to encapsulate parameters for image generation.

    Class ```Args``` holds configuration parameters for generating images, such as image size, number of images, contour lengths, and other properties related to the snakes.

    Main Execution:

    - Argument Parsing: The script expects command-line arguments to specify the number of machines, start ID, batch ID, and total number of images.
    - Dataset Generation: It sets up various configurations for generating datasets with different properties (e.g., contour length, continuity, contrast). It calls the from_wrapper function from snakes.py to generate images for each configuration.
    - Timing: Measures and prints the time taken to generate the datasets.

- The scripts ```snakes2.py``` and `snakes2_wrapper.py` are extensions of the previous scripts. They are designed to generate synthetic images of "snakes" with circles

- About `snakes2.py`

    The script does not have a main execution block, as it is intended to be used as a module.

    About functions in script:
    
    - **accumulate_meta** and **accumulate_meta_segment**: collect metadata about the generated images, including information about the image path, filename, and various parameters used in image generation.
    - **two_snakes**: generates two snakes on an image. It samples contrast values for the snakes and uses helper functions to initialize and extend the snakes. It returns the images of the snakes, a mask, and the coordinates of the origin and terminal tips of the snakes.
    - **initialize_two_seeds**: initializes the first segments of two snakes. It samples random orientations and positions for the initial segments and ensures they are within the image boundaries.
    - **draw_circle**: draws a circle on the image, which can be used as a marker for the start or end of a snake.
    - **from_wrapper**: generates a batch of images based on provided arguments. It creates two snakes, adds distractor snakes and paddles, and optionally adds markers to the image. It saves the generated images and metadata if specified.

- About `snakes2_wrapper.py`

    Main script for 'snakes' generation

    Such as a `snakes_wrapper.py`, imports `snakes2` module and defines an `Args` class to encapsulate parameters for image generation.

    The **Args** class is a container for all the parameters used in the image generation process. It initializes with default values for various parameters, such as contour path, number of images, window size, and more. The class uses the `__dict__.update()` method to dynamically update its attributes based on local variables, excluding `self`.

    About functions in script:

    - **parse_arguments**

        This function is responsible for parsing command-line arguments using the argparse module. It defines both required and optional parameters:

        Required Parameters:

        `n_images`: Number of images to generate.
        `image_size`: Size of the output images.
        `difficulty`: Difficulty level of the images, with choices of "easy", "intermediate", or "hard".

        Optional Parameters:

        These are derived from the default values in the **Args** class, excluding `n_images` and `window_size`.

        The function returns the parsed arguments.

    - **get_difficulty_params**

        This function returns a dictionary of parameters specific to the chosen difficulty level. It adjusts settings such as dataset_subpath and contour_length based on whether the difficulty is *easy*, *intermediate*, or *hard*.


    - **main**

        The main function orchestrates the image generation process:


        It parses command-line arguments and initializes an Args object.

        Updates the main parameters with parsed arguments.

        Retrieves and applies difficulty-specific parameters.

        Configures additional general settings for image generation.

        Constructs the dataset path and ensures the directory exists.

        Initiates the image generation process using the `snakes2.from_wrapper function`.

        Measures and prints the elapsed time for generating the images.

