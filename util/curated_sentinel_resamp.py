import numpy as np
from PIL import Image
from torchvision.transforms import v2
import sys
import os

def resamp_and_save(in_res, out_res, im_dir, label_dir, output, curr_ind, im_size, split):
    in_res = [float(in_res[0]), float(in_res[1])]
    out_res = [float(out_res[0]), float(out_res[1])]

    im1 = Image.open(im_dir.split(',')[0]+'/A/'+im_dir.split(',')[1])
    im2 = Image.open(im_dir.split(',')[0]+'/B/'+im_dir.split(',')[1])
    label = Image.open(label_dir)
    y_resamp = in_res[np.argmin(np.array(in_res))]/out_res[np.argmin(np.array(in_res))] if np.argmin(np.array(im1)[:-1]) == 0 else in_res[np.argmax(np.array(in_res))]/out_res[np.argmax(np.array(in_res))]
    x_resamp = in_res[np.argmin(np.array(in_res))]/out_res[np.argmin(np.array(in_res))] if np.argmin(np.array(im1)[:-1]) == 1 else in_res[np.argmax(np.array(in_res))]/out_res[np.argmax(np.array(in_res))]

    trans = v2.Compose([
        v2.Resize((int(y_resamp*np.array(im1).shape[0]), int(x_resamp*np.array(im1).shape[1])))
    ])

    new_im1 = np.array(trans(im1))
    new_im2 = np.array(trans(im2))
    new_label = np.array(trans(label))
    
    chip_out_image_new(new_im1, im_size, int(im_size*0.8), curr_ind, output+'/A', 'A', split)
    chip_out_image_new(new_im2, im_size, int(im_size*0.8), curr_ind, output+'/B', 'B', split)
    new_curr_ind = chip_out_image_new(new_label, im_size, int(im_size*0.8), curr_ind, output+'/label', 'label', split)
        
    return new_curr_ind


def chip_out_image(image, im_size, stride, curr_ind, output, mode):
    for row in range((image.shape[0]//im_size) + ((image.shape[0]//im_size)*(abs(stride-im_size))//im_size) + (1 if image.shape[0] % im_size != 0 else 0)):
        for col in range(image.shape[1]//im_size + ((image.shape[1]//im_size)*(abs(stride-im_size))//im_size) + (1 if image.shape[1] % im_size != 0 else 0)):
            row_start = ((row*im_size) - abs(stride-im_size)) if row != 0 else row*im_size
            row_end = row_start + im_size
            col_start = ((col*im_size) - abs(stride-im_size)) if col != 0 else col*im_size
            col_end = col_start + im_size

            if row_end > image.shape[0]:
                row_end = image.shape[0]
                row_start = row_end - im_size

            if col_end > image.shape[1]:
                col_end = image.shape[1]
                col_start = col_end - im_size

            chip = image[row_start:row_end,col_start:col_end,:] if mode != 'label' else image[row_start:row_end,col_start:col_end,0]
            Image.fromarray(chip.astype('uint8')).save(output+f'/train_{curr_ind}.png')
            curr_ind += 1
            # if curr_ind > 30: return curr_ind
    return curr_ind

def chip_out_image_new(image, im_size, stride, curr_ind, output, mode, split):
    row_done = False
    col_done = False
    curr_row_ind = 0
    curr_col_ind = 0
    tolerance = 0

    while not row_done:
        chip = image[curr_row_ind:curr_row_ind+im_size, curr_col_ind:curr_col_ind+im_size, 0] if (mode == 'label' and len(image.shape)==3) else image[curr_row_ind:curr_row_ind+im_size, curr_col_ind:curr_col_ind+im_size]
        Image.fromarray(chip.astype('uint8')).save(output+f'/{split}_{curr_ind}.png')
        curr_ind += 1
        # if curr_ind > 30: return curr_ind
        curr_col_ind += stride
        if (curr_col_ind+im_size) > image.shape[1]:
            chip = image[curr_row_ind:curr_row_ind+im_size, image.shape[1]-im_size:image.shape[1], 0] if (mode == 'label' and len(image.shape)==3) else image[curr_row_ind:curr_row_ind+im_size, image.shape[1]-im_size:image.shape[1]]
            Image.fromarray(chip.astype('uint8')).save(output+f'/{split}_{curr_ind}.png')
            curr_ind += 1
            col_done = True
            curr_row_ind += stride
            curr_col_ind = 0

        if col_done and (curr_row_ind+im_size) > image.shape[0]:
            if tolerance == 0:
                tolerance += 1
                curr_row_ind = image.shape[0]-im_size
                col_done = False
            else:
                row_done = True

    return curr_ind




if __name__ == '__main__':
    # image_res_m = sys.argv[1].split(',')
    # new_res_m = sys.argv[2].split(',')
    # image_dir = sys.argv[3]
    # label_dir = sys.argv[4]
    # output_dir = sys.argv[5]
    # curr_ind = int(sys.argv[6])
    # im_size = int(sys.argv[7])

    # resamp_and_save(in_res=image_res_m, out_res=new_res_m, im_dir=image_dir, label_dir=label_dir, output=output_dir)

    # new_curr_ind = resamp_and_save(in_res=image_res_m, out_res=new_res_m, im_dir=image_dir, label_dir=label_dir, output=output_dir, curr_ind=curr_ind, im_size=im_size)
    # print(new_curr_ind)

    # Hard coding some paths and params to do this quickly
    
    # Hard coded image resolution dict from running the onera_processing python script
    # resolution_dict = {
    #    'paris': [12.951762522562007, 8.528940920475153],
    #    'mumbai': [10.335629167243322, 9.757747949160347],
    #    'valencia': [11.011589540882943, 9.171694404394309],
    #    'aguasclaras': [9.840771874814296, 10.226241260670045],
    #    'milano': [12.00102763897067, 8.817561118904282],
    #    'abudhabi': [10.460433026229062, 9.53510057932481],
    #    'nantes': [11.197899625973678, 9.445592566449736],
    #    'montpellier': [11.383523992576059, 9.22192542828326],
    #    'rennes': [8.478656630523682, 12.720880574829943],
    #    'chongqing': [10.762813497410976, 9.360053329511215],
    #    'rio': [9.645022195541468, 10.466879801058672],
    #    'bercy': [12.958168007130249, 8.519894380406253],
    #    'bordeaux': [12.10875166225906, 8.57862869264421],
    #    'hongkong': [10.403869413421642, 9.62296485708686],
    #    'pisa': [11.978308803707773, 8.650227184682771],
    #    'norcia': [8.834171326319224, 12.044163199160186],
    #    'saclay_e': [11.884138166587272, 9.081757986507915],
    #    'beirut': [11.013739417450802, 9.14402096300481],
    #    'dubai': [10.558186941501955, 9.555140342605306],
    #    'saclay_w': [11.884138166587272, 9.081757986050109],
    #    'beihai': [10.402273768226493, 9.665103032570997],
    #    'brasilia': [9.844074417337165, 10.21547935237714],
    #    'lasvegas': [11.178605449295718, 9.039437996744189],
    #    'cupertino': [11.36698831594937, 9.025413733974437]
    #}

    resolution_dict = {
        'image_1': [6.1947342769832, 6.1916668499858005],
        'image_2': [6.676706087311209, 6.669145417620403],
        'image_3': [6.071866846211567, 6.070022645769181],
        'image_4': [6.6331889487555475, 6.620956502870322],
        'image_5': [6.619338285013577, 6.610192339801532],
        'image_6': [6.653603399495559, 6.663989517035176],
        'image_7': [6.858372849659992, 6.8669172455018295],
        'image_8': [6.858372849659992, 6.8669172455018295],
        'image_9': [6.495517915829335, 6.480323944959383],
        'image_10': [6.495517915829335, 6.480323944959383]
    }

    im_size = 256
    im_dir = '/Users/jacobriviere/Desktop/Personal_Projects/Curated_sentinel_2_dataset_2'

    # TEST
    train_label_dir = '/Users/jacobriviere/Desktop/Personal_Projects/Curated_sentinel_2_dataset_2/label'
    output_dir = '/Users/jacobriviere/Desktop/Personal_Projects/Curated_sentinel_2_dataset_2/test_256'
    out_res_m = [5, 5]
    curr_ind = 0
    for tr_inner in os.listdir(train_label_dir):
        
        if tr_inner[-4:] != '.txt' and tr_inner != '.DS_Store':
            print(tr_inner)
            new_curr_ind = resamp_and_save(in_res=resolution_dict[tr_inner[:-4]], out_res=out_res_m, im_dir=im_dir+','+tr_inner, label_dir=train_label_dir+f'/{tr_inner}', output=output_dir, curr_ind=curr_ind, im_size=im_size, split='test')
            curr_ind = new_curr_ind

