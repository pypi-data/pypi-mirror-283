from numpy.testing import assert_almost_equal
import pytest

import sys
sys.path.append('../')

from fastopic import FASTopic
from topmost.data import download_dataset, DynamicDataset
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Union, Mapping, Any, Callable, Iterable


@pytest.fixture
def cache_path():
    return './pytest_cache/'


@pytest.fixture
def num_topics():
    return 10


class DocEmbedModel:
    def __init__(
            self,
            model: str="all-MiniLM-L6-v2",
            device: str='cpu'
        ):

        self.doc_embed_model = SentenceTransformer(model, device=device)

    def encode(self,
               docs:List[str],
               show_progress_bar:bool=False,
               normalize_embeddings: bool=True
            ):

        embeddings = self.doc_embed_model.encode(
            docs,
            show_progress_bar=show_progress_bar,
            normalize_embeddings=normalize_embeddings,
        )
        return embeddings


def test(cache_path, num_topics):
    download_dataset("NYT", cache_path=f"{cache_path}/datasets")
    dataset = DynamicDataset("./datasets/NYT", as_tensor=False)

    custom_model = DocEmbedModel()

    model = FASTopic(num_topics=num_topics, doc_embed_model=custom_model, epochs=1)
    docs = dataset.train_texts
    model.fit_transform(docs)
    beta = model.get_beta()
