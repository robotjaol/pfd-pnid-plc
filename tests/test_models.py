from openlift.models import ESPWellModel, PlantParameters


def parameters() -> PlantParameters:
    return PlantParameters(180, 7.5, 22, 95, 0.0018, 0.0010, 50, 105, 135, 620, 0.70, 0.88, 480, 55)


def test_increased_frequency_increases_flow():
    low = ESPWellModel(parameters())._steady_flow(40, 180, 0)
    high = ESPWellModel(parameters())._steady_flow(55, 180, 0)
    assert high > low >= 0


def test_blockage_reduces_flow():
    model = ESPWellModel(parameters())
    assert model._steady_flow(50, 180, 0.4) < model._steady_flow(50, 180, 0)


def test_power_is_nonnegative():
    result = ESPWellModel(parameters()).step(50, 180, 0, 1)
    assert result.electrical_power_kw >= 0

