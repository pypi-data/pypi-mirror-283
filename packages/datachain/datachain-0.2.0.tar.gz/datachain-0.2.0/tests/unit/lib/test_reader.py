from datachain.lib.feature import Feature
from datachain.lib.file import TextFile
from datachain.lib.reader import FeatureReader, LabelReader


class NameFeature(Feature):
    name: str

    def get_value(self):
        return self.name


class PrefixReader(FeatureReader):
    def __call__(self, value):
        return "prefix-" + value


class SuffixReader(FeatureReader):
    def __init__(self, fr_class, suffix):
        self.suffix = suffix
        super().__init__(fr_class)

    def __call__(self, value):
        return value + self.suffix


def test_feature_reader():
    reader = PrefixReader(NameFeature)
    feature = NameFeature(name="name")
    assert reader(feature.get_value()) == "prefix-name"


def test_feature_reader_args():
    reader = SuffixReader(NameFeature, suffix="-suffix")
    feature = NameFeature(name="name")
    assert reader(feature.get_value()) == "name-suffix"


def test_feature_reader_file(tmp_path, catalog):
    file_name = "myfile"
    data = "myText"

    file_path = tmp_path / file_name
    with open(file_path, "w") as fd:
        fd.write(data)

    reader = PrefixReader(TextFile)
    file = TextFile(name=file_name, source=f"file://{tmp_path}")

    with open(file_path) as fd:
        file._set_stream(catalog, fd, caching_enabled=False)
        assert reader(file.get_value()) == "prefix-myText"


def test_feature_reader_column():
    reader = PrefixReader("name")
    feature = NameFeature(name="name")
    assert reader(feature.get_value()) == "prefix-name"


def test_label_reader():
    classes = ["my", "name"]
    reader = LabelReader("name", classes=classes)
    feature = NameFeature(name="name")
    assert reader(feature.get_value()) == 1
