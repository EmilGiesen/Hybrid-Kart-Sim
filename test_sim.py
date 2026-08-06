import pytest
import fahrzeug
import matplotlib.pyplot as plt
import numpy as np
from sim import sim_acceleration


def test_grenzfall_ohne_widerstaende():
    test_kart = fahrzeug.kart.copy()
    test_kart["cw_area"] = 0
    test_kart["rr_coefficient"] = 0
    test_kart["friction_coefficient"] = 100

    time, velocity, times, velocities, engine_rpm, current_torque, added_energy, lost_energy= sim_acceleration(test_kart)

    # HIER: dein erwarteter Wert, den du von Hand ausgerechnet hast
    erwartete_geschwindigkeit_nach_einem_schritt = 0.0004823628

    assert velocities[0] == pytest.approx(erwartete_geschwindigkeit_nach_einem_schritt, rel=0.01)
    
def test_ausrollen():
    test_kart = fahrzeug.kart.copy()

    time, velocity, times, velocities, engine_rpm, current_torque, added_energy, lost_energy = sim_acceleration(
        kart=test_kart,
        velocity=27.8,
        current_torque=0,
        total_ratio=0,
        goal_velocity=0,
    )
    ist_monoton_fallend = all(velocities[i] >= velocities[i+1] for i in range(len(velocities) - 1))
    assert ist_monoton_fallend
    assert velocity > -0.01
    
def test_energiebilanz():
    test_kart = fahrzeug.kart.copy()
    driving_weight = test_kart["driving_weight"]
    
    time, velocity, times, velocities, engine_rpm, current_torque, added_energy, lost_energy = sim_acceleration(test_kart)
    
    total_added_energy = sum(added_energy)
    total_lost_energy = sum(lost_energy)
    kin_energy = 0.5 * driving_weight * velocity**2
    
    total_energy = total_added_energy - total_lost_energy
    
    assert total_energy == pytest.approx(kin_energy, rel=0.01)
