from cmath import rect
from pathlib import Path

import numpy as np
import pytest

from stanio.csv import read_csv
from stanio.reshape import *

HERE = Path(__file__).parent
DATA = HERE / "data"


# see file data/rectangles/output.stan
@pytest.fixture(scope="module", params=[True, False], ids=["use_object", "use_dtype"])
def rect_data(request):
    files = [DATA / "rectangles" / f"output_{i}.csv" for i in range(1, 5)]
    header, data = read_csv(files)
    params = parse_header(header)
    yield stan_variables(params, data, object=request.param)


def test_basic_shapes(rect_data):
    assert rect_data["lp__"].shape == (4, 1000)
    assert rect_data["mu"].shape == (4, 1000)

    assert rect_data["v"].shape == (4, 1000, 2)
    assert rect_data["r"].shape == (4, 1000, 3)
    assert rect_data["m"].shape == (4, 1000, 2, 3)
    assert rect_data["threeD"].shape == (4, 1000, 4, 2, 3)

    assert rect_data["z"].shape == (4, 1000)
    assert rect_data["z"].dtype.kind == "c"
    assert rect_data["zv"].shape == (4, 1000, 2)
    assert rect_data["zv"].dtype.kind == "c"
    assert rect_data["zm"].shape == (4, 1000, 2, 3)
    assert rect_data["zm"].dtype.kind == "c"
    assert rect_data["z3D"].shape == (4, 1000, 4, 2, 3)
    assert rect_data["z3D"].dtype.kind == "c"


def check_rectangle(rect_data, chain, draw):
    # in output.stan we define all output variables as
    # multiples of mu, so we can check that the data is
    # reshaped correctly by checking that the multiples
    mu = rect_data["mu"][chain, draw]
    np.testing.assert_almost_equal(rect_data["v"][chain, draw], [mu, 2 * mu])
    np.testing.assert_almost_equal(
        rect_data["r"][chain, draw], [2 * mu, 3 * mu, 4 * mu]
    )
    matrix_expected = np.linspace(5, 11, 6).reshape(2, 3, order="F") * mu

    np.testing.assert_almost_equal(rect_data["m"][chain, draw], matrix_expected)
    threeD_expected = (
        np.linspace(5, 11, 6).reshape(1, 2, 3, order="F")
        * np.arange(1, 5).reshape(4, 1, 1)
        * mu
    )
    np.testing.assert_almost_equal(
        rect_data["threeD"][chain, draw],
        threeD_expected,
    )

    nu = rect_data["nu"][chain, draw]
    np.testing.assert_almost_equal(rect_data["z"][chain, draw], nu + 2j * nu)
    np.testing.assert_almost_equal(
        rect_data["zv"][chain, draw], [3 * nu + 4j * nu, 5 * nu + 6j * nu]
    )
    np.testing.assert_almost_equal(
        rect_data["zm"][chain, draw],
        matrix_expected + 1j * (matrix_expected + 1),
    )
    np.testing.assert_almost_equal(
        rect_data["z3D"][chain, draw],
        threeD_expected + 1j * (threeD_expected + 1),
    )


def test_basic_values(rect_data):
    # hardcoded to make sure we're really reading the chain and draw
    # we think we are
    assert rect_data["mu"][0, 0] == 0.5393776428
    assert rect_data["mu"][1, 0] == -0.8009042915

    check_rectangle(rect_data, 0, 0)
    check_rectangle(rect_data, -1, -1)
    for _ in range(100):
        draw = np.random.randint(1000)
        chain = np.random.randint(4)
        check_rectangle(rect_data, chain, draw)


# see file data/tuples/output.stan
@pytest.fixture(scope="module", params=[True, False], ids=["use_object", "use_dtype"])
def tuple_data(request):
    files = [DATA / "tuples" / f"output_{i}.csv" for i in range(1, 5)]
    header, data = read_csv(files)
    params = parse_header(header)
    yield stan_variables(params, data, object=request.param)


def test_tuple_shapes(tuple_data):
    assert len(tuple_data["pair"][0, 0]) == 2

    assert len(tuple_data["nested"][0, 0]) == 2
    assert len(tuple_data["nested"][0, 0][1]) == 2

    assert tuple_data["arr_pair"].shape == (4, 1000, 2)

    assert tuple_data["arr_very_nested"].shape == (4, 1000, 3)

    assert tuple_data["arr_2d_pair"].shape == (4, 1000, 3, 2)

    assert tuple_data["ultimate"].shape == (4, 1000, 2, 3)
    assert tuple_data["ultimate"][0, 0, 0, 0][0].shape == (2,)
    assert tuple_data["ultimate"][0, 0, 0, 0][0][0][1].shape == (2,)
    assert tuple_data["ultimate"][0, 0, 0, 0][1].shape == (4, 5)


def check_tuple_shapes_objects(tuple_data):
    assert isinstance(tuple_data["pair"][0, 0], tuple)

    assert isinstance(tuple_data["nested"][0, 0], tuple)
    assert isinstance(tuple_data["nested"][0, 0][1], tuple)

    assert isinstance(tuple_data["arr_pair"][0, 0, 0], tuple)

    assert isinstance(tuple_data["arr_very_nested"][0, 0, 0], tuple)
    assert isinstance(tuple_data["arr_very_nested"][0, 0, 0][0], tuple)
    assert isinstance(tuple_data["arr_very_nested"][0, 0, 0][0][1], tuple)

    assert isinstance(tuple_data["arr_2d_pair"][0, 0, 0, 0], tuple)

    assert isinstance(tuple_data["ultimate"][0, 0, 0, 0], tuple)
    assert isinstance(tuple_data["ultimate"][0, 0, 0, 0][0][0], tuple)


def check_tuple_shapes_custom_dtypes(tuple_data):
    for value in tuple_data.values():
        assert not value.dtype.hasobject

    pair_dtype = np.dtype([("1", "f8"), ("2", "f8")])
    assert tuple_data["pair"].dtype == pair_dtype

    nested_dtype = np.dtype([("1", "f8"), ("2", [("1", "f8"), ("2", "c16")])])
    assert tuple_data["nested"].dtype == nested_dtype
    assert tuple_data["nested"][0, 0][1].dtype == nested_dtype[1]

    assert tuple_data["arr_pair"].dtype == pair_dtype

    very_nested_dtype = np.dtype(
        [
            ("1", nested_dtype),
            ("2", "f8"),
        ]
    )
    assert tuple_data["arr_very_nested"].dtype == very_nested_dtype
    assert tuple_data["arr_very_nested"][0, 0, 0][0].dtype == nested_dtype
    assert tuple_data["arr_very_nested"][0, 0, 0][0][1].dtype == nested_dtype[1]

    ultimate_dtype = np.dtype(
        [
            ("1", ([("1", "f8"), ("2", "(2,)f8")], (2,))),
            ("2", "(4,5)f8"),
        ]
    )
    assert tuple_data["ultimate"].dtype == ultimate_dtype


def test_tuple_dtypes(tuple_data):
    if isinstance(tuple_data["pair"][0, 0], tuple):
        check_tuple_shapes_objects(tuple_data)
    else:
        check_tuple_shapes_custom_dtypes(tuple_data)


def assert_tuple_equal(t1, t2):
    if hasattr(t1, "dtype") and t1.dtype.kind == "V":
        t1 = t1.tolist()

    assert len(t1) == len(t2)
    for x, y in zip(t1, t2):
        if isinstance(x, tuple):
            assert_tuple_equal(x, y)
        else:
            np.testing.assert_almost_equal(x, y)


def check_tuples(tuple_data, chain, draw):
    base = tuple_data["base"][chain, draw]
    base_i = tuple_data["base_i"][chain, draw]
    pair_exp = (base, 2 * base)
    assert_tuple_equal(tuple_data["pair"][chain, draw], pair_exp)
    nested_exp = (base * 3, (base_i, 4j * base))
    assert_tuple_equal(tuple_data["nested"][chain, draw], nested_exp)

    assert_tuple_equal(tuple_data["arr_pair"][chain, draw, 0], pair_exp)
    assert_tuple_equal(tuple_data["arr_pair"][chain, draw, 1], (base * 5, base * 6))

    assert_tuple_equal(
        tuple_data["arr_very_nested"][chain, draw, 0], (nested_exp, base * 7)
    )
    assert_tuple_equal(
        tuple_data["arr_very_nested"][chain, draw, 1],
        ((base * 8, (base_i * 2, base * 9.0j)), base * 10),
    )
    assert_tuple_equal(
        tuple_data["arr_very_nested"][chain, draw, 2], (nested_exp, base * 11)
    )

    for i in range(3):
        for j in range(2):
            idx = i * 4 + j * 2 + 12
            assert_tuple_equal(
                tuple_data["arr_2d_pair"][chain, draw, i, j],
                (base * idx, base * (idx + 1)),
            )

    for i in range(2):
        for j in range(3):
            idx = i * 3 + j
            base_p = base + idx
            assert_tuple_equal(
                tuple_data["ultimate"][chain, draw, i, j][0][0],
                (base_p, [base_p * 2, base_p * 3]),
            )
            assert_tuple_equal(
                tuple_data["ultimate"][chain, draw, i, j][0][1],
                (base_p * 4, [base_p * 5, base_p * 6]),
            )
            matrix_expected = np.linspace(7, 11, 20).reshape(4, 5, order="F") * base_p

            np.testing.assert_almost_equal(
                tuple_data["ultimate"][chain, draw, i, j][1], matrix_expected
            )


def test_tuple_values(tuple_data):
    # fixed param
    assert (tuple_data["lp__"] == 0).all()

    assert tuple_data["base"][0, 0] == -0.5216157371

    check_tuples(tuple_data, 0, 0)
    check_tuples(tuple_data, -1, -1)
    for _ in range(100):
        draw = np.random.randint(1000)
        chain = np.random.randint(4)
        check_tuples(tuple_data, chain, draw)


def test_single_row():
    header, data = read_csv(DATA / "edges" / "one_row.csv")
    params = parse_header(header)
    variables = stan_variables(params, data.squeeze())
    assert variables["lp__"].shape == ()
    z = variables["z"]
    assert z.shape == (4, 3)
    for i in range(4):
        for j in range(3):
            assert int(z[i, j]) == i + 1


def test_preserve_1d():
    header, data = read_csv(DATA / "edges" / "oned_opt.csv")
    params = parse_header(header)
    A = params["A"]
    dummy = params["dummy"]
    dummy_tuple = params["dummy_tuple"]
    assert A.extract_reshape(data).shape == (1, 2, 1, 3)
    assert dummy.extract_reshape(data).shape == (1, 1, 1, 1)
    assert dummy_tuple.extract_reshape(data).shape == (1, 1)
    assert A.extract_reshape(data.squeeze()).shape == (2, 1, 3)
    assert dummy.extract_reshape(data.squeeze()).shape == (1, 1, 1)
    assert dummy_tuple.extract_reshape(data.squeeze()).shape == (1,)

    assert len(A.columns()) == A.num_elts() == 2 * 1 * 3

    header2, data2 = read_csv(DATA / "edges" / "oned_sample.csv")
    params2 = parse_header(header2)
    A2 = params2["A"]
    dummy2 = params2["dummy"]
    dummy_tuple2 = params2["dummy_tuple"]

    assert A2.extract_reshape(data2).shape == (1, 1000, 2, 1, 3)
    assert dummy2.extract_reshape(data2).shape == (1, 1000, 1, 1, 1)
    assert dummy_tuple2.extract_reshape(data2).shape == (1, 1000, 1)

    A_extracted = A2.extract_reshape(data2.squeeze())
    dummy_extracted = dummy2.extract_reshape(data2.squeeze())
    dummy_tuple_extracted = dummy_tuple2.extract_reshape(data2.squeeze())
    assert A_extracted.shape == (1000, 2, 1, 3)
    assert dummy_extracted.shape == (1000, 1, 1, 1)
    assert dummy_tuple_extracted.shape == (1000, 1)

    base = params2["base"].extract_reshape(data2.squeeze())
    for i in range(1000):
        b = base[i]
        np.testing.assert_almost_equal(
            A_extracted[i], np.array([[[b, b, b * 2]], [[b * 3, b * 4, b * 5]]])
        )
        np.testing.assert_almost_equal(dummy_extracted[i, 0, 0, 0], b * 10)
        assert_tuple_equal(dummy_tuple_extracted[i][0], (b * 11, b * 12))
