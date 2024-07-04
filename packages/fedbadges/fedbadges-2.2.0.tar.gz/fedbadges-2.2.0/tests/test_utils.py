from fedbadges.utils import single_argument_lambda


def test_lambda_factory():
    expression = "value + 2"
    target = 4
    actual = single_argument_lambda(expression, 2)
    assert actual == target
