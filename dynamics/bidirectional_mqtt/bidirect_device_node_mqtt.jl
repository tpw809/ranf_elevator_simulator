# MQTT: Message Queuing Telemetry Transport
# using Pkg
# Pkg.add("MQTTClient")
# Pkg.add("JSON3")
# check install:
# using MQTTClient

using MQTTClient
using JSON3
using Random
using Dates
# using LinearAlgebra

const CMD_TOPIC = "demo/node1/cmd"
const TLM_TOPIC = "demo/node1/tlm"

# Device state
const node_state = Dict(
    "enabled" => false,
    "setpoint" => 50.0
)

# mutable struct NodeState
# 
#     enabled::Bool
#     setpoint::Float64
#     process_value::Float64
#     temperature::Float64
# 
# end

####################################################
# MQTT Connection
####################################################

client = Client(
    "localhost",
    1883
)

connect(client)

println("Connected to broker")

#####################################################
# Command Handler
#####################################################

function handle_command(payload)

    cmd = JSON3.read(payload)

    println("Received command:")
    println(cmd)

    if haskey(cmd, :command)

        if cmd.command == "ENABLE"
            node_state["enabled"] = true

        elseif cmd.command == "DISABLE"
            node_state["enabled"] = false

        elseif cmd.command == "SETPOINT"
            node_state["setpoint"] = Float64(cmd.value)

        end
    end
    println("Current state = ", node_state)
end


# Subscribe to commands
subscribe(client, CMD_TOPIC)

#########################################
# Telemetry Task
#########################################

@async begin

    while true

        process_value =
            node_state["enabled"] ?
            node_state["setpoint"] + rand(-2.0:0.1:2.0) :
            0.0

        telemetry = Dict(
            "enabled" => node_state["enabled"],
            "setpoint" => node_state["setpoint"],
            "process_value" => round(process_value, digits=2),
            "temperature" => round(
                25 + rand()*10 - 5,
                digits=2
            ),
            "timestamp" => now()
        )

        publish(
            client,
            TLM_TOPIC,
            JSON3.write(telemetry)
        )

        sleep(1)
    end
end

############################################
# Main MQTT Loop
############################################

while true

    msg = receive(client)

    if msg !== nothing
        topic = msg.topic
        payload = String(msg.payload)

        if topic == CMD_TOPIC
            handle_command(payload)

        end
    end
end

# state = NodeState(
#     false,
#     50.0,
#     0.0,
#     25.0
# )
#