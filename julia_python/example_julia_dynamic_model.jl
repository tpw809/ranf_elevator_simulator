# using Pkg
# Pkg.add("DataFrames")
# import Pkg;
# Pkg.add("StaticArrays")
using CSV
using Plots
using StaticArrays
using DataFrames
using DifferentialEquations

# include("stepper_driver.jl")
# include("adams_style_velocity_adjusted_mu.jl")

###############################
# Load Parameters
###############################

# load parameters from json here:


###############################
# Run Parameters
###############################

# [sec], initial time:
ti = 0.0

# [sec], initialize current time to initial time:
t = ti

# [sec], final time:
tf = 0.6

# [sec], time step:
dt = 0.000001

# [sec], save time step:
save_dt = 0.0001

# [hz], controller frequency:
control_freq = 10000.0

# [sec], save data time interval:
t_save = ti - dt/2.0

# solver type:

# initialize stop flag to false:
stop_flag = false

# initialize time-history data index:
memory_index = 1

###############################
# System Parameters:
###############################

# Make a struct?

# [N-m/A], motor torque constant:
kt = 2.0 * 0.04

# [N-m], detent torque constant:
k_det = 0.0

# [Ohm], phase resistance:
R = 1.2

# [H], phase inductance:
L = 0.001

# [kg-m^2], motor rotor inertia:
J = 2.0e-5

# [V], supply voltage:
v_supp = 24.0

# [N-m], motor static friction (coulomb) torque:
T_coul = 0.0

# [N-m/rad/sec], motor rotor viscous friction coefficient:
b = 1.0e-3

# [A], max current:
i_max = 20.0

# [#], number of phases:
n_phases = 2

# number of rotor pole pairs:
N_RT = 3

# step angle:
step_angle_rad = 30.0*pi/180.0

# Stiction params:
stiction_params = (
    mu_static = 1.5*T_coul,
    mu_dynamic = T_coul,
    v_dyn = 0.2,
    v_stat = 0.1,)

println(stiction_params.mu_static)
println(stiction_params.mu_dynamic)
println(stiction_params.v_dyn)
println(stiction_params.v_stat)

# like Python's partial:
#f(x, y, z) = x + y + z
#g = x -> f(x, 2, 3) # Partial application: y=2, z=3
#g(1) # Returns 6

stiction_func = velocity -> adams_style_velocity_adjusted_mu(
    velocity,
    stiction_params.mu_static,
    stiction_params.mu_dynamic,
    stiction_params.v_stat,
    stiction_params.v_dyn)


###############################
# controller / intermittent functions:
###############################
control_freq = 1000.0
control_dt = 1.0 / control_freq
t_control = 0.0 - control_dt / 2.0

# controller step frequency parameters:
mutable struct StepControl
    step_freq::Float64  # [hz]
    step_dt::Float64
    next_step_t::Float64
    n::Int
end

step_control = StepControl(40.0, 1.0/40.0, 1.0/40.0, 0)

function control(t::Float64, sc::StepControl)
    # println("running controller")
    if t>= sc.next_step_t
        sc.n += 1
        sc.next_step_t = t + sc.step_dt
    end
end


###############################
# Dynamic Parameters: 
###############################

# mutable struct StepperParams
#     v1::Float64
#     v2::Float64
#     n::Int
# end
# 
# stepper_params = StepperParams(v_supp, v_supp, 0)

###############################
# Stepper Driver Logic:
###############################

# moved to separate file for modularity

###############################
# Allocate Sim Data Memory: 
###############################

# use rounding to convert Float64 to Int:
data_points = ceil(Int, (tf - ti) / save_dt) + 1
println("data_points = ", data_points)

# pre-allocate data memory:
memory = DataFrame(zeros(data_points, 6), [:t, :i1, :i2, :theta, :omega, :n])
# println("empty memory = ", memory)


###############################
# Define the ODE: 
###############################

function f!(du, u, p, t)
    # du = state derivative
    # u = state = [i1, i2, theta_m, omega_m]
    # p = parameters
    # t = time

    # du[1] = -0.5 * u[1]
    # du[2] = u[3]

    # params:
    v1, v2, n = p

    i1 = u[1]
    i2 = u[2]
    theta = u[3]
    omega = u[4]

    theta_e1 = theta * N_RT
    theta_e2 = theta_e1 + pi/2.0

    bemf1 = kt * omega * sin(theta_e1)
    bemf2 = kt * omega * sin(theta_e2)

    # [A/sec], current change:
    di_dt1 = (v1 - R * i1 - bemf1) / L
    di_dt2 = (v2 - R * i2 - bemf2) / L

    # Motor Torque:
    T_ph1 = kt * i1 * sin(theta_e1)
    T_ph2 = kt * i2 * sin(theta_e2)
    T_det = -k_det * sin(4.0*theta_e1)
    T_mot = T_ph1 + T_ph2 + T_det
    T_visc = -b * omega

    du[1] = di_dt1
    du[2] = di_dt2
    du[3] = u[4]
    du[4] = (T_mot + T_visc) / J
end

# Initial conditions:
u0 = [0.0, 0.0, 0.0, 0.0]

# [sec], Time span:
tspan = (ti, ti+dt)

# parameters:
params = (v1=0.0, v2=0.0, n=0)

# Define the ODE problem:
prob = ODEProblem(f!, u0, tspan, params)

###############################
# Run Simulation
###############################

# sol = solve(prob)
# t_now = sol.t[end]
# u_now = sol.u[end]
# println("t_now = ", t_now)
# println("u_now = ", u_now)

# start time:
tic = time()

while t < (tf + dt/2.0)
    # println("t = ", t)
    # println("t_save = ", t_save)

    # Exercise Controllers here:
    if t > t_control
        # println("running controller")
        control(t, step_control)
        global t_control = t + control_dt
    end

    # Run Dynamics here:
    # println("running dynamics")
    new_p = (v1=cardinal_stepper_2phase(v_supp, step_control.n)[1], v2=cardinal_stepper_2phase(v_supp, step_control.n)[2], n=step_control.n)
    # Remake allows changing parameters/initial conditions efficiently
    new_prob = remake(prob, p=new_p, u0=u0)
    sol = solve(new_prob, Tsit5())

    global u0 = sol.u[end]
    # println("u0 = ", u0)

    # Save data to memory here:
    # maybe separate memory compilation to a separate function?
    if t > t_save
        # println("saving data to memory")
        # println(t)
        memory[memory_index, :t] = t
        memory[memory_index, [2,3,4,5]] = u0
        memory[memory_index, :n] = step_control.n
        global t_save += save_dt
        global memory_index += 1
    end

    # save state to json:


    global t += dt
    
    if stop_flag
        break
    end
end


# elapsed time:
toc = time()
println("elapsed time = ", toc - tic, " sec")

###############################
# Save simulation time-history data to csv
###############################

# dir = @__DIR__
# path = joinpath(dir, "model_sim_memory.csv")
# CSV.write(path, memory)
