from openlift.control import PIDConfig, PIDController


def test_pid_obeys_output_and_ramp_limits():
    controller = PIDController(PIDConfig(1, 1, 0, 35, 60, 0.25), 50)
    output = controller.step(70, 100, 1)
    assert output == 50.25
    for _ in range(100):
        output = controller.step(70, 100, 1)
    assert 35 <= output <= 60

