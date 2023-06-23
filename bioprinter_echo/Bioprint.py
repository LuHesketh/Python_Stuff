
from bioprinter import bioprint

bioprint(
    image_filename="SNOWMAN_3.jpeg",
    output_filename="SNOWMAN_3.csv",
    bg_color=[0, 0, 255],  # blue background represents empty wells
    pigments_wells={"A1": [0, 0, 0], # black yeast in source well A1
                    "A2": [255, 255, 255]}, # white yeast in source well A2
    quantified_image_filename="SNOWMAN_3_PREVIEW.jpeg"
    )

