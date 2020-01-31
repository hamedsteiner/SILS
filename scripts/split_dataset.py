"""
Split the dataset without GT triplets exposed to each other
"""
import os
import random

RANDOM = '-random'      # '-random' | ''

# # for intrinsic
# DIR_SRC_INPUT = '/home/lyf/ws/datasets/IntrinsicImg_dataset/dataset/MIT/MIT-input'
# DIR_SRC_LAYER1 = '/home/lyf/ws/datasets/IntrinsicImg_dataset/dataset/MIT/MIT-reflectance'
# DIR_SRC_LAYER2 = '/home/lyf/ws/datasets/IntrinsicImg_dataset/dataset/MIT/MIT-shading'
# DIR_OUT = '/home/lyf/ws/datasets/IntrinsicImg_dataset/dataset/MIT-wo_gt{}'.format(RANDOM)

# for intrinsic
DIR_SRC_INPUT = '/home/ros/ws/nips19/datasets/reflect_ben/blended'
DIR_SRC_LAYER1 = '/home/ros/ws/nips19/datasets/reflect_ben/transmission'
DIR_SRC_LAYER2 = '/home/ros/ws/nips19/datasets/reflect_ben/reflection'
DIR_OUT = '/home/ros/ws/nips19/datasets/reflect_ben-wo_gt{}'.format(RANDOM)


IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]


def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def check_dir(s_dir):
    if not os.path.exists(s_dir):
        os.makedirs(s_dir)


image_names = os.listdir(DIR_SRC_INPUT)
image_names = [x for x in image_names if is_image_file(x)]
image_names = sorted(image_names)

n_image = len(image_names)

if len(RANDOM) > 0:
    train_images = random.sample(image_names, n_image // 2)
else:
    train_images = image_names[: n_image // 2]
test_images = [x for x in image_names if x not in train_images]

# generate the train set
for item in train_images:
    dir_out_in = os.path.join(DIR_OUT, 'trainA')
    check_dir(dir_out_in)
    pwd_src = os.path.join(DIR_SRC_INPUT, item)
    pwd_dst = os.path.join(dir_out_in, item)
    os.symlink(pwd_src, pwd_dst)

# generate the train set
for item in test_images:
    dir_out_train_l1 = os.path.join(DIR_OUT, 'trainB')
    dir_out_train_l2 = os.path.join(DIR_OUT, 'trainC')
    dir_out_test_in = os.path.join(DIR_OUT, 'testA')
    dir_out_test_l1 = os.path.join(DIR_OUT, 'testB')
    dir_out_test_l2 = os.path.join(DIR_OUT, 'testC')
    check_dir(dir_out_train_l1)
    check_dir(dir_out_train_l2)
    check_dir(dir_out_test_in)
    check_dir(dir_out_test_l1)
    check_dir(dir_out_test_l2)

    # generate test input
    pwd_src = os.path.join(DIR_SRC_INPUT, item)
    pwd_dst = os.path.join(dir_out_test_in, item)
    os.symlink(pwd_src, pwd_dst)
    # generate l1
    pwd_src = os.path.join(DIR_SRC_LAYER1, item)
    pwd_dst = os.path.join(dir_out_test_l1, item)
    os.symlink(pwd_src, pwd_dst)
    pwd_src = os.path.join(DIR_SRC_LAYER1, item)
    pwd_dst = os.path.join(dir_out_train_l1, item)
    os.symlink(pwd_src, pwd_dst)
    # generate l2
    pwd_src = os.path.join(DIR_SRC_LAYER2, item)
    pwd_dst = os.path.join(dir_out_test_l2, item)
    os.symlink(pwd_src, pwd_dst)
    pwd_src = os.path.join(DIR_SRC_LAYER2, item)
    pwd_dst = os.path.join(dir_out_train_l2, item)
    os.symlink(pwd_src, pwd_dst)

print('Done.')


