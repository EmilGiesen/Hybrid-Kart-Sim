import numpy as np
import matplotlib.pyplot as plt
import fahrzeug
from fahrzeug import kart


def sim_breaking(kart, velocity, mode, F_traction_max_front, F_traction_max_rear,  x_new, v_new, dt, battery_level, current_capacity):
    electric_torque = kart["electric_torque"]
    battery_capacity = kart["battery_capacity"]
    rear_wheel_radius = kart["rear_wheel_radius"]
    front_wheel_radius = kart["front_wheel_radius"]
    
    F_regen = 0
    
    if current_capacity < battery_capacity and mode != 3: 
        T_regen_max = electric_torque
        F_regen = min(T_regen_max / front_wheel_radius, 50 * battery_capacity)
        F_regen = min(F_regen, F_traction_max_front)
    
        energy_regen = F_regen * (x_new - x_new + v_new * dt)
        total_regen = min(energy_regen * 0.1, 5 * battery_capacity)
        battery_level = battery_level + total_regen
        
    F_mech_max = F_traction_max_rear + (F_traction_max_front - F_regen)
    F_combined = 0 - F_mech_max
    
    return battery_level, F_combined


def sim_acceleration(kart, velocity=100.0, current_torque=2000, goal_velocity=0/3.6, total_ratio = None, mode = 2, breaking = True):
    driving_weight = kart["driving_weight"]
    cw_area = kart["cw_area"]
    axel_weight_rear = kart["axel_weight_rear"]
    axel_weight_front = kart["axel_weight_front"]
    air_density = kart["air_density"]
    traction_coefficient = kart["friction_coefficient"]
    rr_coefficent = kart["rr_coefficient"]
    gearbox = kart["gear_ratios"]
    rear_wheel_radius = kart["rear_wheel_radius"]
    front_wheel_radius = kart["front_wheel_radius"]
    electric_torque = kart["electric_torque"]
    electric_output = kart["electric_output"]
    battery_capacity = kart["battery_capacity"]

    primary_gear_ratio = gearbox["primary"]
    secondary_gear_ratio = gearbox["secondary"]
    gear_ratios = gearbox["gears"]



    rpm_value = [punkt["rpm"] for punkt in kart["torque_curve"]]
    torque_value = [punkt["torque"] for punkt in kart["torque_curve"]]

    v_new = 100.0
    t_new = 0.0
    x_new = 0.0

    time = 0.0
    position = 0.0
    dt = 0.0001
    power_cut = 15
    current_gear = 0
    battery_level = battery_capacity * 3600000 * 0.5
    N_rear = driving_weight * 9.81 * axel_weight_rear
    N_front = driving_weight * 9.81 * axel_weight_front
    F_roll = rr_coefficent * driving_weight * 9.81
    F_traction_max_rear = traction_coefficient * N_rear
    F_traction_max_front = traction_coefficient * N_front
    rear_wheel_size = 2 * np.pi * rear_wheel_radius
    times = []
    velocities = []
    added_energy_combustion = []
    lost_energy_combustion = []
    current_capacities = []

        
    accelerating = velocity < goal_velocity
    

    while  (velocity < goal_velocity) if accelerating else (velocity > goal_velocity):
        set_rpm = 2000
        F_front = 0
        current_capacity = battery_level / 3600000
        v_old = v_new
        t_old = t_new
        x_old = x_new
        new_gear = current_gear
            
        if total_ratio == 0:
            total_ratio = 0
        else:
            total_ratio = primary_gear_ratio * gear_ratios[current_gear]["ratio"] * secondary_gear_ratio

        F_drag = 0.5 * air_density * cw_area * velocity ** 2

        rear_wheel_rotations = velocity / rear_wheel_size * 60
        calculated_rpm = rear_wheel_rotations * total_ratio

        engine_rpm = max([set_rpm, calculated_rpm])
        current_torque = np.interp(engine_rpm, rpm_value, torque_value)
        engine_output = current_torque * engine_rpm / 9549.3
        

        if power_cut != 15:
            current_torque = 0
            power_cut = power_cut + 1
            if battery_capacity*0.2 < current_capacity:
                F_front = electric_torque / front_wheel_radius
                F_front = min([F_front, F_traction_max_front])
            
        F_rear = current_torque * total_ratio / rear_wheel_radius
        F_rear = min([F_rear, F_traction_max_rear])
        
        if mode == 1 and battery_capacity*0.2 < current_capacity: # Full Electric power
            F_front = electric_torque / front_wheel_radius
            F_front = min([F_front, F_traction_max_front])
            
        if mode == 2 and battery_capacity*0.2 < current_capacity and current_torque < 105: # Hybrid Electric power only if rpm under 9
            F_front = electric_torque / front_wheel_radius
            F_front = min([F_front, F_traction_max_front])
                
        if mode == 3: # Combustion only
            vroom = "vroom"
            F_front = 0
                
        F_combined = F_rear + F_front
        
        if breaking == True:
            
            battery_level, F_combined = sim_breaking(kart, velocity, mode, F_traction_max_front, F_traction_max_rear,  x_new, v_new, dt, battery_level, current_capacity)
            F_combined = F_combined
            
        
        
        F_total = F_combined - F_drag - F_roll
        a = F_total / driving_weight
        
        if engine_rpm > 14450:
            new_gear = current_gear + 1
            
        if new_gear > 5:
            new_gear = 5

        if new_gear != current_gear:
            power_cut = 0
        else:
            power_cut = 15
         
         
        current_gear = new_gear
        v_new = v_old + a * dt
        t_new = t_old + dt
        x_new = x_old + v_old * dt

        time = t_new
        velocity = v_new
        position = x_new
        times.append(time)
        velocities.append(velocity)
        added_energy_combustion.append(F_combined * v_old * dt)
        lost_energy_combustion.append((F_drag + F_roll) * v_old * dt)
        current_capacities.append(current_capacity)
        
        if mode == 1 or mode == 2:   
            produced_energy = F_front * (x_new - x_old)
            used_energy = produced_energy / 0.88
    
            battery_level = battery_level - used_energy        
            
        if velocity < 0:
            break
        if v_new == v_old:
            break

    return time, velocity, times, velocities, engine_rpm, current_torque, added_energy_combustion, lost_energy_combustion, current_gear, current_capacities


if __name__ == "__main__":
    time, velocity, times, velocities, engine_rpm, current_torque, added_energy_combustion, lost_energy_combustion, current_gear, current_capacities = sim_acceleration(kart, velocity=100.0, current_torque=2000, goal_velocity=0/3.6, total_ratio = None, mode = 2, breaking = True)

    print(time)
    print(velocity)
    print(current_gear)

    plt.plot(times, velocities)
    plt.xlabel("Zeit [s]")
    plt.ylabel("Geschwindigkeit [m/s]")
    plt.title("Geradeausbeschleunigung 0-100 km/h")
    plt.show()
    
    plt.plot(times, current_capacities)
    plt.xlabel("Zeit [s]")
    plt.ylabel("Akkukapazizäz [kwH]")
    plt.title("Akku Test")
    plt.show()
