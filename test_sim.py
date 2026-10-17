import pytest
import fahrzeug
from sim import sim_acceleration
 
# sim_acceleration hat als Standard inzwischen eine BREMSUNG aus 100 m/s
# (velocity=100, goal_velocity=0, breaking=True).
# Die Beschleunigungs-Tests geben deshalb ihre Startwerte ausdrücklich an.
BESCHLEUNIGEN = dict(velocity=0.0, goal_velocity=150 / 3.6, breaking=False)
 
 
def test_grenzfall_ohne_widerstaende():
    test_kart = fahrzeug.kart.copy()
    test_kart["cw_area"] = 0
    test_kart["rr_coefficient"] = 0
    test_kart["friction_coefficient"] = 100
 
    time, velocity, times, velocities, *_ = sim_acceleration(test_kart, mode=3, **BESCHLEUNIGEN)
 
    # Von Hand: F = M * i / r, a = F / m, v nach dt = a * dt
    erwartete_geschwindigkeit_nach_einem_schritt = 0.0004823628
 
    assert velocities[0] == pytest.approx(erwartete_geschwindigkeit_nach_einem_schritt, rel=0.01)
 
 
def test_ausrollen():
    test_kart = fahrzeug.kart.copy()
 
    time, velocity, times, velocities, *_ = sim_acceleration(
        kart=test_kart,
        velocity=27.8,
        goal_velocity=0,
        total_ratio=0,
        mode=3,
        breaking=False,
    )
    ist_monoton_fallend = all(velocities[i] >= velocities[i + 1] for i in range(len(velocities) - 1))
    assert ist_monoton_fallend
    assert velocity > -0.01
 
 
def test_energiebilanz_beschleunigen():
    test_kart = fahrzeug.kart.copy()
    m = test_kart["driving_weight"]
 
    time, velocity, times, velocities, engine_rpm, current_torque, added, lost, *_ = sim_acceleration(
        test_kart, **BESCHLEUNIGEN
    )
 
    # zugeführte Energie - Verluste = kinetische Energie (Start bei 0 m/s)
    total_energy = sum(added) - sum(lost)
    kin_energy = 0.5 * m * velocity ** 2
 
    assert total_energy == pytest.approx(kin_energy, rel=0.01)
 
 
def test_energiebilanz_bremsen():
    test_kart = fahrzeug.kart.copy()
    m = test_kart["driving_weight"]
    start = 100.0
 
    # Standardaufruf = Bremsung aus 100 m/s
    time, velocity, times, velocities, engine_rpm, current_torque, added, lost, *_ = sim_acceleration(
        test_kart, velocity=start
    )
 
    # Energieänderung = kinetische Energie am Ende - am Anfang (negativ beim Bremsen)
    total_energy = sum(added) - sum(lost)
    delta_kin = 0.5 * m * (velocity ** 2 - start ** 2)
 
    assert total_energy == pytest.approx(delta_kin, rel=0.01)
 
 
def test_electricfasterthencombustion():
    test_kart = fahrzeug.kart.copy()
    time_electric = sim_acceleration(test_kart, mode=1, **BESCHLEUNIGEN)[0]
    time_hybrid = sim_acceleration(test_kart, mode=2, **BESCHLEUNIGEN)[0]
    time_combustion = sim_acceleration(test_kart, mode=3, **BESCHLEUNIGEN)[0]
 
    assert time_electric <= time_hybrid <= time_combustion