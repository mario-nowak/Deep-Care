import os

from deepcare.data import generate_center_base_train_images_parallel

if __name__ == "__main__":

    parts = [i for i in range(32, 36)]

    for part in parts:
        msa_data_path = "/home/mnowak/care/artmiseqv3humanchr1430covMSA"
        msa_file_name = f"part__{part}"
        msa_file = os.path.join(msa_data_path, msa_file_name)

        fastq_file_path = "/share/errorcorrection/datasets/artmiseqv3humanchr14"
        fastq_file_name = "humanchr1430cov_errFree.fq.gz"
        fastq_file = os.path.join(fastq_file_path, fastq_file_name)

        folder_name = f"datasets/w51_h100/balance_test_4_artmiseqv3humanchr1430covMSA/part_{part}"

        generate_center_base_train_images_parallel(
            msa_file_path=msa_file,
            ref_fastq_file_path=fastq_file,
            image_height= 100,
            image_width=51,
            out_dir=folder_name,
            max_num_examples=None,
            workers=5,
            human_readable=True,
            verbose=True
        )