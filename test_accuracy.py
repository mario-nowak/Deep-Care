import os

import torch
from torch.utils.data import DataLoader
import torchvision.transforms as transforms

from deepcare.utils.accuracy import check_accuracy_on_classes, check_accuracy
from deepcare.data import MSADataset
from deepcare.models.conv_net import \
    conv_net_w51_h100_v1, \
    conv_net_w51_h100_v2, \
    conv_net_w51_h100_v3, \
    conv_net_w51_h100_v4, \
    conv_net_w51_h100_v5, \
    conv_net_w51_h100_v6, \
    conv_net_w51_h100_v7, \
    conv_net_w51_h100_v8, \
    conv_net_w51_h100_v9, \
    conv_net_w51_h100_v10, \
    conv_net_w51_h100_v11, \
    conv_net_w250_h50_v1


if __name__ == "__main__":

    device = ("cuda" if torch.cuda.is_available() else "cpu")
    
    dataset_folder = "datasets/w51_h100/"
    dataset_name = "artmiseqv3humanchr1430covMSA_defragmented"

    model_path = "trained_models"
    model_name = "conv_net_v11_w51_h100/BalancedHmnChr14DSet/conv_net_v11_state_dict"
    model = conv_net_w51_h100_v11()

    shuffle = False
    batch_size = 2048
    pin_memory = True
    num_workers = 40
    
    transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5, 0.5), (0.5, 0.5, 0.5, 0.5)),
            ]
        )

    dataset = MSADataset(
        root_dir=os.path.join(dataset_folder, dataset_name),
        annotation_file=os.path.join(dataset_folder, dataset_name, "train_labels.csv"),
        transform=transform
        )

    loader = DataLoader(dataset=dataset, shuffle=shuffle, batch_size=batch_size,num_workers=num_workers,pin_memory=pin_memory)
    
    state_dict = torch.load(os.path.join(model_path, model_name))
    model.load_state_dict(state_dict)
    model.to(device)

    check_accuracy(loader=loader, model=model, device=device)