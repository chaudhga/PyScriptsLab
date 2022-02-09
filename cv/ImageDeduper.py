from imagededup.methods import PHash
from imagededup.utils import plot_duplicates

phasher = PHash()

# Generate encodings for all images in an image directory
encodings = phasher.encode_images(image_dir='C:/Users/chaud/PycharmProjects/pythonProject/ImgTrain/Master')

# Find duplicates using the generated encodings
duplicates = phasher.find_duplicates(encoding_map=encodings)

# plot duplicates obtained for a given file using the duplicates dictionary

plot_duplicates(image_dir='C:/Users/chaud/PycharmProjects/pythonProject/ImgTrain/Master',
                duplicate_map=duplicates,
                filename='2492.jpg')
