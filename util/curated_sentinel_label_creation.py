import os
from PIL import Image
import numpy as np

def label_creation(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename != '.DS_Store':
            im = np.array(Image.open(input_dir+'/'+filename))
            label_im = Image.fromarray(np.zeros((im.shape[0], im.shape[1])).astype('uint8'))
            label_im.save(output_dir+'/'+filename)

if __name__ == '__main__':
    input_dir = '/Users/jacobriviere/Desktop/Personal_Projects/Curated_sentinel_2_dataset_2/A'
    output_dir = '/Users/jacobriviere/Desktop/Personal_Projects/Curated_sentinel_2_dataset_2/label'

    label_creation(input_dir, output_dir)
