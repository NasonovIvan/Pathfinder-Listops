#!/bin/bash

# generate_and_clean.sh

# Default values
N_IMAGES=10
IMAGE_SIZE=256
DIFFICULTY="hard"
SIMILARITY_THRESHOLD=0.9

# Function to show usage
usage() {
    echo "Usage: $0 [-n number_of_images] [-s image_size] [-d difficulty] [-t similarity_threshold]"
    echo "Options:"
    echo "  -n: Number of images to generate (default: 10)"
    echo "  -s: Image size (default: 256)"
    echo "  -d: Difficulty level (easy/medium/hard) (default: hard)"
    echo "  -t: Similarity threshold (default: 0.9)"
    exit 1
}

# Parse command line arguments
while getopts "n:s:d:t:h" opt; do
    case $opt in
        n) N_IMAGES="$OPTARG";;
        s) IMAGE_SIZE="$OPTARG";;
        d) DIFFICULTY="$OPTARG";;
        t) SIMILARITY_THRESHOLD="$OPTARG";;
        h) usage;;
        ?) usage;;
    esac
done

# Execute the Python script
python3 main_generation.py "$N_IMAGES" "$IMAGE_SIZE" "$DIFFICULTY" "$SIMILARITY_THRESHOLD"
