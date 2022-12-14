import os 
import shutil
import glob
import multiprocessing
import time
from tqdm import tqdm
import random
from random import shuffle
from math import ceil

import pandas as pd

from deepcare.utils.msa import nuc_to_index

def generate_dataset(folder_paths, result_folder_path):
    examples_path = os.path.join(result_folder_path, "examples")
    #workers = 40

    bases = "ACGT"
    counter = {b : 0 for b in bases}

    if not os.path.exists(result_folder_path):
        os.makedirs(result_folder_path)
    if not os.path.exists(examples_path):
        os.makedirs(examples_path)

    names = []
    labels = []

    for folder in folder_paths:
        
        print(f"Now reading folder {folder}")
        start = time.time()
        images = glob.glob(os.path.join(folder, '*.png'))

        for image in tqdm(images):

            elements = os.path.basename(image).split("_")
            label = elements[0]
            if len(elements) == 4:
                annotation = f"{elements[1]}_{elements[2]}"
            else:
                annotation = elements[1]
            new_name = f"{label}_{annotation}_{counter[label]}.png"
            new_path = os.path.join(examples_path, new_name)
            shutil.copyfile(image, new_path)

            counter[label] += 1
            names.append(new_name)
            labels.append(nuc_to_index[label])

        #shutil.rmtree(folder)

        end = time.time()
        duration = end - start
        print(f"Done reading folder. Reading took {duration} seconds.")

    train_df = pd.DataFrame(columns=["img_name","label"])

    train_df["img_name"] = names
    train_df["label"] = labels

    train_df.to_csv(os.path.join(result_folder_path, "train_labels.csv"), index = False, header=True)

    print("Done creating the index file.")


def generate_binary_dataset(folder_paths, result_folder_path):
    examples_path = os.path.join(result_folder_path, "examples")
    #workers = 40

    bases = "ACGT"
    counter = {b : 0 for b in bases}
    case_to_index = {"cons" : 1, "ncons" : 0}

    if not os.path.exists(result_folder_path):
        os.makedirs(result_folder_path)
    if not os.path.exists(examples_path):
        os.makedirs(examples_path)

    names = []
    labels = []

    for folder in folder_paths:
        
        print(f"Now reading folder {folder}")
        start = time.time()
        images = glob.glob(os.path.join(folder, '*.png'))

        for image in tqdm(images):

            elements = os.path.basename(image).split("_")
            base = elements[0]
            label = elements[1]
            if len(elements) == 4:
                annotation = f"{elements[1]}_{elements[2]}"
            else:
                annotation = elements[1]
            new_name = f"{base}_{annotation}_{counter[base]}.png"
            new_path = os.path.join(examples_path, new_name)
            shutil.copyfile(image, new_path)

            counter[base] += 1
            names.append(new_name)
            labels.append(case_to_index[label])

        #shutil.rmtree(folder)

        end = time.time()
        duration = end - start
        print(f"Done reading folder. Reading took {duration} seconds.")

    train_df = pd.DataFrame(columns=["img_name","label"])

    train_df["img_name"] = names
    train_df["label"] = labels

    train_df.to_csv(os.path.join(result_folder_path, "train_labels.csv"), index = False, header=True)

    print("Done creating the index file.")


if __name__ == "__main__":

    global_start = time.time()

    random.seed(1)
    folder_paths = (
          glob.glob("/home/mnowak/data/fresh_start/binary_quality_balanced_datasets/w1_h151/humanchr1430cov_2_parts_0_39/*")
        + glob.glob("/home/mnowak/data/fresh_start/binary_quality_balanced_datasets/w1_h151/humanchr1430cov_3_parts_0_39/*") 
        + glob.glob("/home/mnowak/data/fresh_start/binary_quality_balanced_datasets/w1_h151/humanchr1430cov_4_parts_0_39/*") 
        + glob.glob("/home/mnowak/data/fresh_start/binary_quality_balanced_datasets/w1_h151/humanchr1430cov_5_parts_0_39/*") 
    )
    folder_paths = sorted(folder_paths)
    print(folder_paths)
    shuffle(folder_paths)
    split_part = 0.8
    trainin_parts = ceil(len(folder_paths)*0.8)
    traning_folder_paths = folder_paths[:trainin_parts]
    validation_folder_paths = folder_paths[trainin_parts:]

    result_training_folder_path = "/home/mnowak/data/fresh_start/binary_quality_balanced_datasets/w1_h151/artmiseqv3humanchr1430covMSATraining_2_5"
    result_validation_folder_path = "/home/mnowak/data/fresh_start/binary_quality_balanced_datasets/w1_h151/artmiseqv3humanchr1430covMSAValidation_2_5"
    generate_binary_dataset(traning_folder_paths, result_training_folder_path)
    generate_binary_dataset(validation_folder_paths, result_validation_folder_path)

    print(f"Everything took {time.time() - global_start}")
