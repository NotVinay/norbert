import numpy as np
import pytest
import norbert


@pytest.fixture(params=[8, 11, 33])
def nb_frames(request):
    return int(request.param)


@pytest.fixture(params=[8, 11, 33])
def nb_bins(request):
    return request.param


@pytest.fixture(params=[1, 2, 3])
def nb_channels(request):
    return request.param


@pytest.fixture(params=[1, 2, 4])
def nb_sources(request):
    return request.param


@pytest.fixture(params=[True, False])
def no_channels(request):
    return request.param


@pytest.fixture
def X(request, nb_frames, nb_bins, nb_channels):
    return np.random.random(
        (nb_frames, nb_bins, nb_channels)
    ) + np.random.random(
        (nb_frames, nb_bins, nb_channels)
    ) * 1j


@pytest.fixture
def V(request, nb_frames, nb_bins, nb_channels, nb_sources, no_channels):
    if no_channels:
        return np.random.random((nb_frames, nb_bins, nb_sources))
    else:
        return np.random.random((nb_frames, nb_bins, nb_channels, nb_sources))


def test_shapes(X, V):
    Y = norbert.wiener(V, X)

    assert X.shape == Y.shape[:-1]

    Y = norbert.softmask(V, X)

    assert X.shape == Y.shape[:-1]


def test_wiener_copy(X, V):
    X0 = np.copy(X)
    V0 = np.copy(V)

    _ = norbert.wiener(V, X)

    assert np.allclose(X0, X)
    assert np.allclose(V0, V)


def test_softmask_copy(X, V):
    X0 = np.copy(X)
    V0 = np.copy(V)

    _ = norbert.softmask(V, X)

    assert np.allclose(X0, X)
    assert np.allclose(V0, V)
