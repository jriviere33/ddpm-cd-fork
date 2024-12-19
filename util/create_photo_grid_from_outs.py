from PIL import Image
import numpy as np
import sys
from torchvision.utils import make_grid, save_image
import os
import torch

if __name__ == '__main__':
    output_path = sys.argv[1]
    output = sys.argv[2]

    for i in range (108):
        #grid = make_grid([torch.Tensor(Image.open(output_path+f'/img_A_{i}.png')).permute(2,0,1), \
        #        torch.Tensor(Image.open(output_path+f'/img_B_{i}.png')).permute(2,0,1), \
        #        torch.Tensor(Image.open(output_path+f'/img_gt_cm{i}.png')).permute(2,0,1), \
        #        torch.Tensor(Image.open(output_path+f'/img_pred_cm{i}.png')).permute(2,0,1)], \
        #        nrow=4
        #)
        im1 = np.array(Image.open(output_path+f'/img_A_{i}.png'))
        im2 = np.array(Image.open(output_path+f'/img_B_{i}.png'))
        im3 = np.array(Image.open(output_path+f'/img_gt_cm{i}.png'))
        im4 = np.array(Image.open(output_path+f'/img_pred_cm{i}.png'))
        new_im = np.zeros((256,1024+6,3))
        #new_im = np.zeros((256,768+4,3))
        new_im[:,:256,:] = im1[:,:,:]
        new_im[:,256:258,:] = 255
        new_im[:,258:514,:] = im2[:,:,:]
        new_im[:,514:516,:] = 255
        new_im[:,516:772,:] = im3[:,:,:]
        new_im[:,772:774,:] = 255
        new_im[:,774:,:] = im4[:,:,:]
        #print(type(grid))
        #print(grid.shape)
        #Image.fromarray(grid.numpy().astype('uint8')).save(output+f'/image_{i}.png')
        #save_image(grid, output+f'/image_{i}.png')
        Image.fromarray(new_im.astype('uint8')).save(output+f'/image_{i}.png')
