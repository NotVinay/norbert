import numpy as np
import pytest
import norbert.scale as scale


@pytest.fixture(params=[10, 100])
def nb_frames(request, rate):
    return int(request.param)


@pytest.fixture(params=[1024, 777])
def nb_bins(request):
    return request.param


@pytest.fixture(params=[1, 2])
def nb_channels(request):
    return request.param


@pytest.fixture(params=[8000, 16000, 44100])
def rate(request):
    return request.param


@pytest.fixture(params=[np.float, np.complex])
def dtype(request):
    return request.param


@pytest.fixture
def X(request, nb_frames, nb_bins, nb_channels, dtype):
    np.random.seed(0)
    return np.random.random((nb_frames, nb_bins, nb_channels)).astype(dtype)


def test_upscale(X, rate):
    bw = scale.LogScaler()
    Xs = bw.scale(X)
    # test shape
    assert Xs.shape == X.shape


def test_reconstruction(X, rate):
    bw = scale.LogScaler()
    Xs = bw.scale(X)
    Y = bw.unscale(Xs)
    assert Y.shape == X.shape
    assert np.sqrt(((X - Y) ** 2).mean()) < 1e-06


def test_max(X, rate):
    bw = scale.LogScaler()
    Xs = bw.scale(X)

    bw2 = scale.LogScaler()
    bw2.scale(X*2, max=bw.max)
    Y = bw2.unscale(Xs, max=bw.max)
    assert Y.shape == X.shape
    assert np.sqrt(((X - Y) ** 2).mean()) < 1e-06