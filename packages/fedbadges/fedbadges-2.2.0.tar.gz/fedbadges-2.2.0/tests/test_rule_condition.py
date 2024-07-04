import pytest

import fedbadges.rules


def test_malformed_condition(cache_configured):
    """Test that an error is raised when nonsense is provided."""
    with pytest.raises(ValueError):
        fedbadges.rules.Condition(
            dict(
                watwat="does not exist",
            )
        )


@pytest.mark.parametrize(
    ["returned_count", "expectation"],
    [
        (499, False),
        (500, True),
        (501, True),
    ],
)
def test_basic_condition(cache_configured, returned_count, expectation):
    condition = fedbadges.rules.Condition(
        {
            "greater than or equal to": 500,
        }
    )
    assert condition(returned_count) is expectation


@pytest.mark.parametrize(
    ["returned_count", "expectation"],
    [
        (499, False),
        (500, True),
        (501, True),
    ],
)
def test_lambda(cache_configured, returned_count, expectation):
    condition = fedbadges.rules.Condition(
        {
            "lambda": "value >= 500",
        }
    )
    assert condition(returned_count) is expectation
