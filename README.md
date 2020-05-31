This script requires a raspberry pi to run it along with the terminal. To utilize it, one must have the tesseract module installed via the terminal, along with the openCV module.
After installing the openCV and tesseract module, be sure to have an imagine of a vehicle ith the license plate showing titled "image.jpg" in the pictures category.

WARNING: The tesseract module along with the openCV module CAN be very buggy because it recognizes from ITS point of view on what it thinks is a license plate but is not.
When the modules recognize the license plate it uses contouring, bilateral filtering to find it, and produces a single cropped image on what it found.
