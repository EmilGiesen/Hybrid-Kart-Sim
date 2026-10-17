import numpy as np
import matplotlib.pyplot as plt
import fahrzeug

driving_weight = fahrzeug.kart["driving_weight"]
combustion_output = fahrzeug.kart["combustion_output"]
cw_area = fahrzeug.kart["cw_area"]
axle_weight_rear = fahrzeug.kart["axle_weight_rear"]
air_density = fahrzeug.kart["air_density"]
traction_coefficient = fahrzeug.kart["friction_coefficient"]
rr_coefficient = fahrzeug.kart["rr_coefficient"]
torque_curve = fahrzeug.kart["torque_curve"]
gearbox = fahrzeug.kart["gear_ratios"]

primary_gear_ratio = gearbox["primary"]
secondary_gear_ratio = gearbox["secondary"]

gear_ratios = gearbox["gears"]   # list of gear dicts

gear_1_ratio = gear_ratios[0]["ratio"]
gear_2_ratio = gear_ratios[1]["ratio"]
gear_3_ratio = gear_ratios[2]["ratio"]
gear_4_ratio = gear_ratios[3]["ratio"]
gear_5_ratio = gear_ratios[4]["ratio"]
gear_6_ratio = gear_ratios[5]["ratio"]

rear_wheel_radius = fahrzeug.kart["rear_wheel_radius"]

rpm_value = [punkt["rpm"] for punkt in fahrzeug.kart["torque_curve"]]
torque_value = [punkt["torque"] for punkt in fahrzeug.kart["torque_curve"]]

v_new = 0.0
t_new = 0.0
x_new = 0.0

total_ratio = primary_gear_ratio * gear_1_ratio * secondary_gear_ratio # Hard coded gear until Smart transmission 

time = 0.0
velocity = 0.0
position = 0.0
dt = 0.0001

times = []
velocities = []

goal_velocity = 100 / 3.6 # m/s

while velocity < goal_velocity: 
    set_rpm = 2000
    v_old = v_new 
    t_old = t_new
    x_old = x_new
    N = driving_weight * 9.81 * axle_weight_rear

    F_drag = 0.5 * air_density * cw_area * velocity**2
    F_roll = rr_coefficient * driving_weight * 9.81
    F_traction_max = traction_coefficient * N
     
    rear_wheel_size = 2 * np.pi * rear_wheel_radius
    
    rear_wheel_rotations = velocity/ rear_wheel_size * 60
    
    calculated_rpm = rear_wheel_rotations * total_ratio # Hard coded gear until Smart transmission 
    
    engine_rpm = max([set_rpm, calculated_rpm])
    
    current_torque = np.interp(engine_rpm, rpm_value, torque_value)
    
    engine_output = current_torque * engine_rpm / 9549.3

    F = current_torque * total_ratio / rear_wheel_radius
    
    F = min([F, F_traction_max])
    F_total = F - F_drag - F_roll 
    a = F_total / driving_weight 
    
    v_new = v_old + a * dt
    t_new = t_old + dt
    x_new = x_old + v_old * dt
    
    time = t_new
    velocity = v_new
    position = x_new
    times.append(time)
    velocities.append(velocity)
    
    
print (time)
print(velocity)
print(engine_rpm)
print(current_torque)
#

plt.plot(times, velocities)
plt.xlabel("Zeit [s]")
plt.ylabel("Geschwindigkeit [m/s]")
plt.title("Geradeausbeschleunigung 0-100 km/h")
plt.show()