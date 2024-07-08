import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from datasets import load_dataset, DatasetDict
from PIL import Image
from io import BytesIO

# ------------ Data -----------------
IN_MEAN = np.array([0.485, 0.456, 0.406])
IN_STD = np.array([0.229, 0.224, 0.225])

DS_PATH_IMAGENET = "imagenet"
DS_PATH_IMAGENET1K = "imagenet-1k"
DS_PATH_IMAGENETTE = "frgfm/imagenette"
DS_PATH_OPENIMAGES = "dalle-mini/open-images"
DS_PATH_COCO30K = "UCSC-VLAA/Recap-COCO-30K"
DS_PATH_COCOPERSON = "Hamdy20002/COCO_Person"
DS_PATH_COCOCAP2017 = "lmms-lab/COCO-Caption2017"
DS_PATH_STDDOGS = "amaye15/stanford-dogs"
DS_PATH_OCRVQA = "howard-hou/OCR-VQA"
DS_PATH_OCRINVREC = "mychen76/invoices-and-receipts_ocr_v1"
DS_PATH_FASHION4 = "detection-datasets/fashionpedia_4_categories"
DS_PATH_CELEBA = "goodfellowliu/CelebA"
DS_PATH_COCO122 = "detection-datasets/coco"


class ImageLabelDataSet(Dataset):
    def __init__(self, dataset, transform=None, return_type='dict', split='train', image_size=224, convert_rgb=True):
        if isinstance(dataset, DatasetDict) and (split is None or split in dataset):
            split = split or "train"
            self.dataset = dataset[split]
        else:
            self.dataset = dataset
        self.transform = transform
        self.return_type = return_type
        self.image_size = image_size
        self.img_key = 'image' if 'image' in self.dataset.column_names else 'img'
        self.label_key = 'label' if 'label' in self.dataset.column_names else 'lbl'
        self.convert_rgb = convert_rgb
        if self.label_key not in self.dataset.column_names:
            self.label_key = None
        if transform is None:
            if isinstance(self.image_size, int):
                self.resize_transform = transforms.Resize((image_size, image_size))
            self.to_tensor_transform = transforms.ToTensor()
            self.normalize_transform = transforms.Normalize(mean=IN_MEAN, std=IN_STD)
        else:
            # Check if self.transform contains a resize operation
            contains_resize = False
            if self.transform:
                for t in self.transform.transforms:
                    if isinstance(t, transforms.Resize):
                        contains_resize = True
                        break
            if not contains_resize and image_size is not None:
                # Check the size of the first image in the dataset
                first_image = self.dataset[self.img_key][0]
                if isinstance(first_image, torch.Tensor):
                    first_image = transforms.ToPILImage()(first_image)
                first_image_size = first_image.size  # (width, height)

                # Add a resize transform if image size does not match
                if first_image_size != (self.image_size, self.image_size):
                    resize_transform = transforms.Resize((self.image_size, self.image_size))
                    if self.transform:
                        # Insert the resize transform at the beginning
                        self.transform.transforms.append(resize_transform)
                    else:
                        self.resize_transform = transforms.Resize((image_size, image_size))

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]
        img = item[self.img_key]
        if self.convert_rgb and img.mode != 'RGB':
            img = img.convert('RGB')
        with BytesIO() as output:
            img.save(output, format='JPEG')
            img_bytes = output.getvalue()
        img = Image.open(BytesIO(img_bytes))
        if self.transform is None:
            if isinstance(self.image_size, int):
                img = self.resize_transform(img)
            img = self.to_tensor_transform(img)
            img = self.normalize_transform(img)
        else:
            img = self.transform(img)

        if self.return_type == 'image_only':
            return img
        elif self.return_type == 'pair':
            return img, item[self.label_key] if self.label_key else ''
        else:
            item['image'] = img
            return item


def get_cv_dataset(path=DS_PATH_IMAGENETTE,
                   name=None,  # "full_size"
                   batch_size=1,
                   image_size=None, # original size
                   split=None,  # 'train'
                   shuffle=True,
                   num_workers=4,
                   transform=None,
                   return_loader=False,
                   return_type='pair',
                   convert_rgb=False,
                   **loader_params):
    if return_type not in ['image_only', 'pair', 'dict']:
        raise ValueError("return_type must be 'image_only' or 'pair' or 'dict'")

    if path == DS_PATH_IMAGENETTE:
        if name is None:
            name = "full_size"
        assert name in ('160px', '320px', 'full_size')
    elif path == DS_PATH_IMAGENET1K:
        name = None
    elif path == DS_PATH_OPENIMAGES:
        name = "default"
    dataset = load_dataset(path, name, trust_remote_code=True, split=split)

    if isinstance(split, str):
        custom_dataset = ImageLabelDataSet(dataset,
                                           transform=transform,
                                           return_type=return_type,
                                           split=split,
                                           image_size=image_size,
                                           convert_rgb=convert_rgb)
        if return_loader:
            return DataLoader(custom_dataset,
                              batch_size=batch_size,
                              shuffle=shuffle,
                              num_workers=num_workers,
                              **loader_params)
        else:
            return custom_dataset
    else:
        custom_datasets = {}
        for split_name in dataset.keys():
            custom_datasets[split_name] = ImageLabelDataSet(dataset,
                                                            transform=transform,
                                                            return_type=return_type,
                                                            split=split_name,
                                                            image_size=image_size,
                                                            convert_rgb=convert_rgb)
        if return_loader:
            for split_name in custom_datasets:
                custom_datasets[split_name] = DataLoader(dataset=custom_datasets[split_name],
                                                         batch_size=batch_size,
                                                         shuffle=shuffle,
                                                         num_workers=num_workers,
                                                         **loader_params)
        return custom_datasets


def _get_datasplit(d, s):
    if isinstance(d, dict):
        if s in ("validation", 'val'):
            if 'val' in d:
                return d['val']
            if 'validation' in d:
                return d['validation']
        if s in d:
            return d[s]
        else:
            raise f"error: no split:{s} in dataset:{d}!"
    return d


try:
    import lightning


    class DataModuleFromConfig(lightning.LightningDataModule):
        def __init__(
                self,
                dataset_name="frgfm/imagenette",
                batch_size=1,
                image_size=None,
                num_workers=1,
                config_name="full_size",
                split=None,
                shuffle=True,
        ):
            super().__init__()
            self.dataset_name = dataset_name
            self.batch_size = batch_size
            self.image_size = image_size
            self.dataset_configs = dict()
            self.num_workers = num_workers
            self.config_name = config_name
            self.split = split
            self.shuffle = shuffle

            self.train_dataloader = self._train_dataloader
            self.val_dataloader = self._val_dataloader

        def setup(self, stage=None):
            self.datasets = get_cv_dataset(
                path=self.dataset_name,
                name=self.config_name,
                image_size=self.image_size,
                split=self.split,
                batch_size=self.batch_size,
                num_workers=self.num_workers,
                return_type="dict",
            )

        def _train_dataloader(self):
            return DataLoader(
                _get_datasplit(self.datasets, "train"),
                batch_size=self.batch_size,
                num_workers=self.num_workers,
                shuffle=self.shuffle,
                collate_fn=custom_collate,
                pin_memory=True,
            )

        def _val_dataloader(self):
            return DataLoader(
                _get_datasplit(self.datasets, "validation"),
                batch_size=self.batch_size,
                num_workers=self.num_workers,
                collate_fn=custom_collate,
                shuffle=False,
                pin_memory=True,
            )

        def _test_dataloader(self):
            return DataLoader(
                _get_datasplit(self.datasets, "test"),
                batch_size=self.batch_size,
                num_workers=self.num_workers,
                collate_fn=custom_collate,
                shuffle=False,
                pin_memory=True,
            )

except:
    pass


def imshow(img):
    from matplotlib import pyplot as plt
    img = img / 2 + 0.5  # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

def verify_datasets(dataset_names=('fashion_mnist',)):  #"cifar10", 'mnist', DS_PATH_CELEBA
    from tqdm import tqdm

    transform = transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    loader_params = dict(
        shuffle=True,
        drop_last=True,
        pin_memory=True,
    )
    for n in dataset_names:
        dataloader = get_cv_dataset(path=n,
                                    image_size=32,
                                    split='train',
                                    batch_size=2,
                                    num_workers=2,
                                    transform=transform,
                                    return_type="pair",
                                    return_loader=True,
                                    **loader_params
                                    )
        with tqdm(dataloader, dynamic_ncols=True, colour="#ff924a") as data:
            for images, label in data:
                print(images.shape)
                if n == 'mnist':
                    assert (images.shape == torch.Size([2, 3, 32, 32]))
                else:
                    assert (images.shape == torch.Size([2, 3, 32, 32]))
                imshow(images[0])
                break


if __name__ == "__main__":
    verify_datasets()
    datasets = get_cv_dataset(path=DS_PATH_IMAGENETTE,
                              image_size=256,
                              split=None,
                              batch_size=2,
                              num_workers=2,
                              return_type="dict")
    validation_dataset = datasets["validation"]
    print(validation_dataset)

    datasets = get_cv_dataset(path=DS_PATH_IMAGENETTE, return_loader=False, name='full_size', split=None)
    validation_dataset = datasets["validation"]
    print(validation_dataset)
