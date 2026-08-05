import fahrzeug

driving_weight = fahrzeug.kart["driving_weight"]
combustion_output = fahrzeug.kart["combustion_output"]
cw_area = fahrzeug.kart["cw_area"]
axel_weight_rear = fahrzeug.kart["axel_weight_rear"]
air_density = fahrzeug.kart["air_density"]
traction_coefficient = fahrzeug.kart["friction_coefficient"]
rr_coefficent = fahrzeug.kart["rr_coefficient"]

v_new = 0.0
t_new = 0.0
x_new = 0.0

time = 0.0
velocity = 0.0
position = 0.0
dt = 0.0001

times = []
velocities = []

goal_velocity = 100 / 3.6 # m/s

while velocity < goal_velocity: 
    v_old = v_new 
    t_old = t_new
    x_old = x_new
    N = driving_weight * 9.81 * axel_weight_rear
    if velocity == 0.0: 
        F = combustion_output * 1000
    else:
        F = combustion_output * 1000 / velocity
            
    
    F_drag = 0.5 * air_density * cw_area * velocity**2
    F_roll = rr_coefficent * driving_weight * 9.81
    F_traction_max = traction_coefficient * N
    
    F = min([F, F_traction_max])
    F_total = F - F_drag - F_roll 
    
    a= F_total / driving_weight 
    
    v_new = v_old + a * dt
    t_new = t_old + dt
    x_new = x_old + v_old * dt
    
    time = t_new
    velocity = v_new
    position = x_new
    
    
print (time)
print(velocity)
    