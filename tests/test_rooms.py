def calculate_capacity(capacity: int) -> bool:
    return capacity > 100

def test_calculate_capacity():
    result = calculate_capacity(10)

    assert result is True