from typing import Any

import open_clip
import pytest
import torch

from datachain.lib.feature import Feature
from datachain.lib.text import TextFile, TextReader, convert_text


@pytest.mark.parametrize("tokenizer_model", ["ViT-B-32", "hf-hub:timm/ViT-B-16-SigLIP"])
def test_convert_text(tmp_path, tokenizer_model):
    text = "thisismytext"
    tokenizer = open_clip.get_tokenizer(tokenizer_model)
    converted_text = convert_text(text, tokenizer=tokenizer)
    assert isinstance(converted_text, torch.Tensor)

    tokenizer_kwargs = {"context_length": 100}
    converted_text = convert_text(
        text, tokenizer=tokenizer, tokenizer_kwargs=tokenizer_kwargs
    )
    assert converted_text.size() == (100,)
    converted_text = convert_text(
        text, tokenizer=tokenizer, tokenizer_kwargs=tokenizer_kwargs
    )

    model, _, _ = open_clip.create_model_and_transforms(tokenizer_model)
    converted_text = convert_text(text, tokenizer=tokenizer, open_clip_model=model)
    assert converted_text.dtype == torch.float32


def test_text_reader_column(mocker):
    class _TextFeature(Feature):
        text: str

        def get_value(self, *args: Any, **kwargs: Any) -> Any:
            return text

    text = "mytext"
    text_feature = _TextFeature(text=text)

    mock_tokenizer = mocker.Mock()
    kwargs = {
        "tokenizer": mock_tokenizer,
        "tokenizer_kwargs": {"some": "arg"},
        "open_clip_model": None,
    }
    reader = TextReader("text", **kwargs)

    convert_text = mocker.patch("datachain.lib.text.convert_text")
    reader(text_feature.get_value())
    convert_text.assert_called_with(text, **kwargs)


def test_text_reader_file(tmp_path, catalog, mocker):
    file_name = "myfile"
    text = "myText"

    file_path = tmp_path / file_name
    with open(file_path, "w") as fd:
        fd.write(text)

    mock_tokenizer = mocker.Mock()
    kwargs = {
        "tokenizer": mock_tokenizer,
        "tokenizer_kwargs": {"some": "arg"},
        "open_clip_model": None,
    }
    reader = TextReader(**kwargs)
    file = TextFile(name=file_name, source=f"file://{tmp_path}")

    convert_text = mocker.patch("datachain.lib.text.convert_text")
    with open(file_path) as fd:
        file._set_stream(catalog, fd, caching_enabled=False)
        reader(file.get_value())
        convert_text.assert_called_with(text, **kwargs)


def test_text_file_mapper(tmp_path, catalog):
    file_name = "myfile"
    text = "myText"

    file_path = tmp_path / file_name
    with open(file_path, "w") as fd:
        fd.write(text)

    file = TextFile(name=file_name, source=f"file://{tmp_path}")

    with open(file_path) as fd:
        file._set_stream(catalog, fd, caching_enabled=False)
        res = file.get_value()
        assert res == text
