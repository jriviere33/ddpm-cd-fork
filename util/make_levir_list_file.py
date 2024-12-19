import os

if __name__ == '__main__':
    list_dir = '/Users/jacobriviere/Desktop/Personal_Projects/Curated_sentinel_2_dataset_2/test_256/list'
    img_dir = '/Users/jacobriviere/Desktop/Personal_Projects/Curated_sentinel_2_dataset_2/test_256/A'
    split = 'test'

    with open(list_dir+f'/{split}.txt', 'a') as f:
        for i in range(len(os.listdir(img_dir))-1):
            f.write(f'{split}_{i+1}.png\n')
