r""" Dataloader builder for few-shot semantic segmentation dataset  """
from torch.utils.data import DataLoader
from torchvision import transforms

from data.pascal import DatasetPASCAL
from data.coco import DatasetCOCO
from data.deepglobe import DatasetDeepglobe
from data.isic import DatasetISIC
from data.lung import DatasetLung
from data.fss import DatasetFSS
from data.kvasir import DatasetKvasir
from data.wbc import DatasetWBC
from data.tcia import DatasetTCIA


class FSSDataset:

    @classmethod
    def initialize(cls, img_size, datapath):

        cls.datasets = {
            'pascal': DatasetPASCAL,
            'coco': DatasetCOCO,
            'fss': DatasetFSS,
            'deepglobe': DatasetDeepglobe,
            'isic': DatasetISIC,
            'lung': DatasetLung,
            'kvasir':DatasetKvasir,
            'wbc':DatasetWBC,
            'tcia':DatasetTCIA
        }

        cls.img_mean = [0.485, 0.456, 0.406]
        cls.img_std = [0.229, 0.224, 0.225]
        cls.datapath = datapath

        cls.transform = transforms.Compose([transforms.Resize(size=(img_size, img_size)),
                                            transforms.ToTensor(),
                                            transforms.Normalize(cls.img_mean, cls.img_std)])

    @classmethod
    def build_dataloader(cls, benchmark, bsz, nworker, fold, split, shot=1):
        nworker = nworker if split == 'trn' else 0

        dataset = cls.datasets[benchmark](cls.datapath, fold=fold,
                                          transform=cls.transform,
                                          split=split, shot=shot)
        dataloader = DataLoader(dataset, batch_size=bsz, shuffle=split=='trn', num_workers=nworker,
                                pin_memory=True)

        return dataloader
