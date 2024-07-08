import pytest
from torch import Size, Tensor
from torchvision.datasets import FakeData
from torchvision.transforms import v2

from datachain.lib.dc import DataChain
from datachain.lib.pytorch import PytorchDataset


@pytest.fixture
def fake_dataset(tmp_path, catalog):
    # Create fake images in labeled dirs
    data_path = tmp_path / "data" / ""
    for i, (img, label) in enumerate(FakeData()):
        label = str(label)
        (data_path / label).mkdir(parents=True, exist_ok=True)
        img.save(data_path / label / f"{i}.jpg")

    # Create dataset from images
    uri = data_path.as_uri()

    return (
        DataChain.from_storage(uri, type="image")
        .map(label=lambda file: int(file.parent.split("/")[-1]), output=int)
        .save("fake")
    )


def test_pytorch_dataset(fake_dataset):
    transform = v2.Compose([v2.ToTensor(), v2.Resize((64, 64))])
    pt_dataset = PytorchDataset(
        name=fake_dataset.name,
        version=fake_dataset.version,
        transform=transform,
    )
    for img, label in pt_dataset:
        assert isinstance(img, Tensor)
        assert isinstance(label, int)
        assert img.size() == Size([3, 64, 64])


def test_pytorch_dataset_sample(fake_dataset):
    transform = v2.Compose([v2.ToTensor(), v2.Resize((64, 64))])
    pt_dataset = PytorchDataset(
        name=fake_dataset.name,
        version=fake_dataset.version,
        transform=transform,
        num_samples=700,
    )
    assert len(list(pt_dataset)) == 700


def test_to_pytorch(fake_dataset):
    from torch.utils.data import IterableDataset

    transform = v2.Compose([v2.ToTensor(), v2.Resize((64, 64))])
    pt_dataset = fake_dataset.to_pytorch(transform=transform)
    assert isinstance(pt_dataset, IterableDataset)
    for img, label in pt_dataset:
        assert isinstance(img, Tensor)
        assert isinstance(label, int)
        assert img.size() == Size([3, 64, 64])
