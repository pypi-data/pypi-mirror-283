"""Tests for the BlockSet class"""

import pytest

from blocksets.classes.block import Block
from blocksets.classes.blockset import BlockSet, OperationType
from blocksets.classes.exceptions import DimensionMismatchError, InvalidDimensionsError


def test_construction():
    bs = BlockSet()
    assert bs.dimensions is None
    assert bs.normalised == True

    with pytest.raises(InvalidDimensionsError):
        bs = BlockSet("1")

    with pytest.raises(InvalidDimensionsError):
        bs = BlockSet(0)

    bs = BlockSet(2)
    assert bs.dimensions == 2
    assert set(bs.blocks()) == set()
    assert bs.normalised == True


def test_dimensions():
    bs = BlockSet()
    assert bs.dimensions is None
    blk = Block((1, 1))
    bs.add(blk)
    assert bs.dimensions == 2
    bs.clear()
    assert bs.dimensions is None


def test_empty():
    bs = BlockSet()
    assert bs.empty
    blk = Block((1, 1))
    bs.add(blk)
    assert not bs.empty
    assert bs
    bs.toggle(blk)
    assert bs.empty

    bs.add(blk)
    bs.add(blk)
    bs.remove(blk)
    assert bs.empty
    assert not bs


def test_add():
    bs = BlockSet()
    blk = Block(1)
    bs.add(blk)
    assert bs._operation_stack[0] == (OperationType.ADD, blk)
    assert bs.normalised == False

    blk_2 = Block((1, 1))
    with pytest.raises(DimensionMismatchError):
        bs.add(blk_2)

    blk_2 = Block(3)
    bs.add(blk_2)
    assert bs._operation_stack[1] == (OperationType.ADD, blk_2)
    assert len(bs._operation_stack) == 2
    assert bs.normalised == False


def test_clear():
    bs = BlockSet()
    bs.add(Block(1))
    bs.add(Block(2))
    assert len(bs._operation_stack) == 2
    assert bs.normalised == False
    bs.clear()
    assert len(bs._operation_stack) == 0
    assert bs.normalised == True


def test_remove():
    bs = BlockSet()
    blk = Block(1)
    bs.remove(blk)
    assert bs._operation_stack[0] == (OperationType.REMOVE, blk)
    assert bs.normalised == False

    blk_2 = Block((1, 1))
    with pytest.raises(DimensionMismatchError):
        bs.remove(blk_2)

    blk_2 = Block(3)
    bs.remove(blk_2)
    assert bs._operation_stack[1] == (OperationType.REMOVE, blk_2)
    assert len(bs._operation_stack) == 2
    assert bs.normalised == False


def test_toggle():
    bs = BlockSet()
    blk = Block(1)
    bs.toggle(blk)
    assert bs._operation_stack[0] == (OperationType.TOGGLE, blk)
    assert bs.normalised == False

    blk_2 = Block((1, 1))
    with pytest.raises(DimensionMismatchError):
        bs.toggle(blk_2)

    blk_2 = Block(3)
    bs.toggle(blk_2)
    assert bs._operation_stack[1] == (OperationType.TOGGLE, blk_2)
    assert len(bs._operation_stack) == 2
    assert bs.normalised == False


def test_generators():
    bs = BlockSet()
    assert bs.normalised == True
    blk = Block(1)
    blk_2 = Block(3)
    bs.add(blk)
    bs.add(blk_2)
    assert bs.normalised == False
    assert set(bs.blocks()) == {blk, blk_2}
    assert set(bs.block_tuples()) == {blk.norm, blk_2.norm}
    assert bs.normalised == True
