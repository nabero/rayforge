import pytest
from rayforge.models.ops import MoveToCommand, \
                                LineToCommand, \
                                ArcToCommand, \
                                SetPowerCommand, \
                                DisableAirAssistCommand
from rayforge.opstransformer.arcwelder.arcwelder import split_into_segments


def test_split_empty_commands():
    assert split_into_segments([]) == []

def test_split_single_move():
    commands = [MoveToCommand((0, 0))]
    assert split_into_segments(commands) == [[MoveToCommand((0, 0))]]

def test_split_move_and_line():
    commands = [
        MoveToCommand((0, 0)),
        LineToCommand((1, 0))
    ]
    assert split_into_segments(commands) == [
        [MoveToCommand((0, 0)), LineToCommand((1, 0))]
    ]

def test_split_move_and_arc():
    commands = [
        MoveToCommand((0, 0)),
        ArcToCommand((1, 0, 1, 1, False)),
        LineToCommand((2, 0)),
        LineToCommand((3, 0)),
    ]
    assert split_into_segments(commands) == [
        [MoveToCommand((0, 0)), ArcToCommand((1, 0, 1, 1, False))],
        [MoveToCommand((1, 0)), LineToCommand((2, 0)), LineToCommand((3, 0))],
    ]

def test_split_state_commands():
    commands = [
        SetPowerCommand('set_power', (1000,)),
        MoveToCommand((0, 0)),
        LineToCommand((1, 0)),
        DisableAirAssistCommand('disable_air_assist', ())
    ]
    assert split_into_segments(commands) == [
        [SetPowerCommand('set_power', (1000,))],
        [MoveToCommand((0, 0)), LineToCommand((1, 0))],
        [DisableAirAssistCommand('disable_air_assist', ())]
    ]

def test_split_long_mixed_segment():
    commands = [
        MoveToCommand((0, 0)),
        LineToCommand((1, 0)),
        LineToCommand((2, 0)),
        MoveToCommand((3, 0)),
        LineToCommand((4, 0)),
        ArcToCommand((5, 0, 1, 1, False)),
        LineToCommand((6, 0)),
        MoveToCommand((7, 0)),
        ArcToCommand((8, 0, 1, 1, False)),
        MoveToCommand((7, 0)),
        ArcToCommand((8, 0, 1, 1, False)),
    ]
    assert split_into_segments(commands) == [
        [MoveToCommand((0, 0)), LineToCommand((1, 0)), LineToCommand((2, 0))],
        [MoveToCommand((3, 0)), LineToCommand((4, 0))],
        [ArcToCommand((5, 0, 1, 1, False))],
        [MoveToCommand((5, 0)), LineToCommand((6, 0))],
        [MoveToCommand((7, 0)), ArcToCommand((8, 0, 1, 1, False))],
        [MoveToCommand((7, 0)), ArcToCommand((8, 0, 1, 1, False))],
    ]
