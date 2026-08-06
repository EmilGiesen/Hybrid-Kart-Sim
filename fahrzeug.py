kart = {
    "dry_weight": 257, # Value in kg, taken from the Doku
    "driver_weight": 80, # Value 5kg lighter than in the Doku, because I weigh 75kg + 5kg Equipment
    "fluid_weight": 12, # Value in kg
    "driving_weight": 349, # Value in kg
    "axel_weight_rear": 0.6, # Value in percent
    "axel_weight_front": 0.4, # Value in percent
    "combustion_output": 160, # Value in kW
    "max_rpm": 14500, 
    "electric_output": 60, # Peak power of the electric motor in kW
    "battery_capacity": 1.0, # Value in kWh
    "rear_wheel_radius": 0.266, # Value in Meter, 225/45 R13
    "friction_coefficient": 1.4, # Value for Semi-Slicks
    "cw_area": 0.8, # Estimated value 
    "air_density": 1.225, # More accurate value then in the Doku
    "rr_coefficient": 0.015,
    "gear_ratios": { # Based on the 2024 version
        "primary": 1.63066,
        "secondary": 2.5,
        "gears": [
            {"gear": 1, "ratio": 2.61534},
            {"gear": 2, "ratio": 2.05835},
            {"gear": 3, "ratio": 1.72231},
            {"gear": 4, "ratio": 1.52332},
            {"gear": 5, "ratio": 1.36330},
            {"gear": 6, "ratio": 1.25839}
        ]
    },
    "torque_curve": [
        {"rpm": 2000, "torque": 42.0}, # Value in Nm asstimated by Ai based on a given few data points 
        {"rpm": 2500, "torque": 48.0},
        {"rpm": 3000, "torque": 57.0},
        {"rpm": 3500, "torque": 61.0},
        {"rpm": 4000, "torque": 66.0},
        {"rpm": 4500, "torque": 69.0},
        {"rpm": 5000, "torque": 71.0},
        {"rpm": 5500, "torque": 73.0},
        {"rpm": 6000, "torque": 76.0},
        {"rpm": 6500, "torque": 79.0},
        {"rpm": 7000, "torque": 83.0},
        {"rpm": 7500, "torque": 88.0},
        {"rpm": 8000, "torque": 96.0},
        {"rpm": 8500, "torque": 100.0},
        {"rpm": 9000, "torque": 104.0},
        {"rpm": 9500, "torque": 107.0},
        {"rpm": 10000, "torque": 109.0},
        {"rpm": 10500, "torque": 111.0},
        {"rpm": 11000, "torque": 112.0},
        {"rpm": 11500, "torque": 112.5},
        {"rpm": 12000, "torque": 112.8},
        {"rpm": 12500, "torque": 113.0},
        {"rpm": 13000, "torque": 111.5},
        {"rpm": 13500, "torque": 109.5},
        {"rpm": 14000, "torque": 108.0},
        {"rpm": 14500, "torque": 106.9}
    ]
}