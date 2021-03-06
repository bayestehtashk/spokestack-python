"""
This module contains tests for Voice Activity Detection
"""
from unittest.mock import patch

import numpy as np

from spokestack.context import SpeechContext
from spokestack.vad.webrtc import VoiceActivityDetector, VoiceActivityTrigger


@patch("webrtcvad.Vad.is_speech", return_value=True)
def test_vad_is_triggered(mock_class):
    context = SpeechContext()
    detector = VoiceActivityDetector(
        sample_rate=16000, frame_width=10, vad_rise_delay=0, vad_fall_delay=0
    )
    frame = np.zeros(160, np.int16)
    detector(context, frame)
    assert context.is_speech
    detector.close()


@patch("webrtcvad.Vad.is_speech", return_value=True)
def test_vad_rise_delay(mock_class):
    context = SpeechContext()
    detector = VoiceActivityDetector(
        sample_rate=16000, frame_width=10, vad_rise_delay=30, vad_fall_delay=0
    )
    for i in range(3):
        frame = np.zeros(160, np.int16)
        detector(context, frame)
        if i < 2:
            assert not context.is_speech
        else:
            assert context.is_speech
    detector.close()


def test_vad_fall_triggered():
    context = SpeechContext()
    detector = VoiceActivityDetector(
        sample_rate=16000, frame_width=10, vad_rise_delay=0, vad_fall_delay=20
    )
    with patch("webrtcvad.Vad.is_speech", return_value=True):
        frame = np.zeros(160, np.int16)
        detector(context, frame)
        assert context.is_speech

    with patch("webrtcvad.Vad.is_speech", return_value=False):
        frame = np.zeros(160, np.int16)
        detector(context, frame)
        assert context.is_speech

    with patch("webrtcvad.Vad.is_speech", return_value=True):
        frame = np.zeros(160, np.int16)
        detector(context, frame)
        assert context.is_speech
    detector.close()


def test_vad_fall_untriggered():
    context = SpeechContext()
    detector = VoiceActivityDetector(
        sample_rate=16000, frame_width=10, vad_rise_delay=0, vad_fall_delay=20
    )
    with patch("webrtcvad.Vad.is_speech", return_value=True):
        frame = np.zeros(160, np.int16)
        detector(context, frame)
        assert context.is_speech

    with patch("webrtcvad.Vad.is_speech", return_value=False):
        frame = np.zeros(160, np.int16)
        detector(context, frame)
        assert context.is_speech

    with patch("webrtcvad.Vad.is_speech", return_value=False):
        frame = np.zeros(160, np.int16)
        detector(context, frame)
        assert not context.is_speech
    detector.close()


def test_voice_activity_trigger():
    context = SpeechContext()
    trigger = VoiceActivityTrigger()

    frame = np.zeros(160, np.int16)

    trigger(context, frame)
    assert not context.is_active

    context.is_speech = True
    trigger(context, frame)
    assert context.is_active

    trigger.close()
