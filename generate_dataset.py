import os
import glob

from deepcare.data import generate_center_base_train_images


if __name__ == "__main__":


    msa_data_path = "/home/mnowak/care/care-output2/"
    msa_file_name = "humanchr1430covMSA_1"
    msa_file_name_pattern = os.path.join(msa_data_path, msa_file_name)
    msa_file_paths = glob.glob(msa_file_name_pattern)

    fastq_file_path = "/share/errorcorrection/datasets/artmiseqv3humanchr14"
    fastq_file_name = "humanchr1430cov_errFree.fq.gz"
    fastq_file = os.path.join(fastq_file_path, fastq_file_name)

    folder_name = "datasets/test"

    generate_center_base_train_images(
            msa_file_paths=msa_file_paths,
            ref_fastq_file_path=fastq_file,
            image_height=100,
            image_width=51,
            out_dir=folder_name,
            max_number_examples=800,
            human_readable=True,
            verbose=True
        )
