from unittest.mock import patch

import pytest
from fedora_messaging.message import Message

import fedbadges.rules

from .utils import example_real_bodhi_message, MockedDatanommerMessage


class MockQuery:
    def __init__(self, returned_count):
        self.returned_count = returned_count

    def count(self):
        return self.returned_count


def test_malformed_counter(cache_configured):
    """Test that an error is raised when nonsense is provided."""
    with pytest.raises(ValueError):
        fedbadges.rules.DatanommerCounter(
            dict(
                watwat="does not exist",
            )
        )


def test_underspecified_counter(cache_configured):
    """Test that an error is raised when filter is missing."""
    with pytest.raises(ValueError):
        fedbadges.rules.DatanommerCounter(
            {
                "operation": "count",
            }
        )


def test_malformed_filter(cache_configured):
    """Test that an error is raised for malformed filters"""
    with pytest.raises(ValueError):
        fedbadges.rules.DatanommerCounter(
            {
                "filter": {"wat": "baz"},
                "operation": "count",
            }
        )


def test_basic_datanommer(cache_configured):
    counter = fedbadges.rules.DatanommerCounter(
        {
            "filter": {
                "topics": ["message.topic"],
            },
            "operation": "count",
        }
    )
    message = Message(
        topic="org.fedoraproject.dev.something.sometopic",
    )
    with patch("datanommer.models.Message.grep") as grep:
        grep.return_value = 42, 1, MockQuery(42)
        result = counter.count(message, "dummy-user")
        assert result == 42
        grep.assert_called_once_with(
            topics=["org.fedoraproject.dev.something.sometopic"], defer=True, rows_per_page=0
        )


def test_datanommer_with_lambda_operation(cache_configured):
    counter = fedbadges.rules.DatanommerCounter(
        {
            "filter": {
                "topics": ["message.topic"],
            },
            "operation": {
                "lambda": (
                    "sum(1 for msg in results "
                    "if msg.msg['some_value'] == message.body['some_value'])"
                ),
            },
        }
    )

    def _make_fake_message(value):
        return Message(
            topic="org.fedoraproject.dev.something.sometopic",
            body=dict(
                some_value=value,
            ),
        )

    with (
        patch("datanommer.models.Message.grep") as grep,
        patch("datanommer.models.session.scalars") as scalars,
    ):
        scalars.return_value.all.return_value = [
            MockedDatanommerMessage(_make_fake_message(test_value)) for test_value in (4, 5, 6)
        ]
        grep.return_value = (3, 1, "unused because of the scalars mock")
        result = counter.count(_make_fake_message(5), "dummy-user")
        assert result == 1


def test_datanommer_with_lambda_filter(cache_configured):
    counter = fedbadges.rules.DatanommerCounter(
        {
            "filter": {"users": "[u for u in message.usernames if not u in ['bodhi', 'hadess']]"},
            "operation": "count",
        }
    )

    message = example_real_bodhi_message
    returned_count = 0

    with patch("datanommer.models.Message.grep") as grep:
        grep.return_value = returned_count, 1, MockQuery(returned_count)
        result = counter.count(message, "dummy-user")
        assert result == returned_count
        grep.assert_called_once_with(users=["lmacken"], defer=True, rows_per_page=0)
