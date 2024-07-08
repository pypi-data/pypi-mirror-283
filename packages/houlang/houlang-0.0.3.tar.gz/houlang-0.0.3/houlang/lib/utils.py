import pathlib

def path_is_img(path):
    """
    Check if a path point to an image file.

    Args:
        path (str or pathlib.Path): The path to the file.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)
    return path.suffix in ['.jpg', '.jpeg', '.jp2', '.png', '.bmp', '.tiff', '.tif', '.gif']