import pytest

def test_import():
    import auto_struct

def test_parse_uints():
    from auto_struct import uint8_t, uint16_t, uint32_t, uint64_t, IntegerOutOfBounds
    for i in range(0, 256):
        uint8_t(i)
        uint16_t(i)
        uint32_t(i)
        uint64_t(i)
    with pytest.raises(IntegerOutOfBounds):
        uint8_t(256)
    with pytest.raises(IntegerOutOfBounds):
        uint64_t(1<<64)

