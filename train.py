import os

import torch
from torch.utils.data.sampler import SubsetRandomSampler
import numpy as np

from language import Language
from dataset import KoreanDataset

here = os.path.dirname(os.path.abspath(__file__))
file_path_data = os.path.join(here, 'data', 'toy_data.txt')
file_path_tokens_map = os.path.join(here, 'data', 'tokens_map.json')
file_path_vectors_map = os.path.join(here, 'data', 'vectors_map.txt')

# Data parameters
max_len_sentence = 50
max_len_morpheme = 5
embedding_dim = 300  # dimension of substring embedding

# Training parameters
random_seed = 0
validation_split = .2
shuffle_dataset = True

start_epoch = 0
epochs = 1000
batch_size = 2
encoder_lr = 1e-4  # learning rate for encoder
decoder_lr = 4e-4  # learning rate for decoder
print_freq = 1  # print training status every 100 iterations, print validation status every epoch

def main():
    language = Language(file_path_tokens_map=file_path_tokens_map, file_path_vectors_map=file_path_vectors_map)
    vocab_size = language.get_n_tokens()
    print('total vocab_size:', vocab_size)

    korean_dataset = KoreanDataset(file_path_data=file_path_data, file_path_tokens_map=file_path_tokens_map,
                                   max_len_sentence=50, max_len_morpheme=5, noise=True)

    # Creating data indices for training and validation splits:
    dataset_size = len(korean_dataset)
    indices = list(range(dataset_size))
    split = int(np.floor(validation_split * dataset_size))
    if shuffle_dataset:
        np.random.seed(random_seed)
        np.random.shuffle(indices)
    train_indices, val_indices = indices[split:], indices[:split]

    # Creating data samplers and loaders:
    train_sampler = SubsetRandomSampler(train_indices)
    valid_sampler = SubsetRandomSampler(val_indices)
    train_loader = torch.utils.data.DataLoader(korean_dataset, batch_size=batch_size, sampler=train_sampler,
                                               pin_memory=True, drop_last=True)
    validation_loader = torch.utils.data.DataLoader(korean_dataset, batch_size=batch_size, sampler=valid_sampler,
                                                    pin_memory=True, drop_last=True)

    for i, (plain_words, enc_words, len_inputs) in enumerate(train_loader):


if __name__ == '__main__':
    main()