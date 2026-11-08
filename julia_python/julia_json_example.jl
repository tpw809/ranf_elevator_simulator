# to install JSON:
# import Pkg; Pkg.add("JSON")

using JSON

# Create a sample Julia data structure (Dictionary)
data = Dict(
    "name" => "Alice",
    "age" => 30,
    "skills" => ["Julia", "Python", "Data Science"],
    "active" => true,
    "account_balance" => 19.97
)

# Open a file in write mode ("w") and print the data directly into it
open("example_output_data_dict.json", "w") do f
    JSON.print(f, data)
end


# example save json:
data = Dict(
    "project" => "JSON.jl", 
    "status" => "complete"
)

# Convert the data structure into a JSON string
json_string = JSON.json(data)

# Save the string to a file
open("output_string.json", "w") do f
    write(f, json_string)
end


# data dictionary:
data = Dict("name" => "Bob", "roles" => ["Admin", "User"])

# Generate a formatted, indented JSON string and save it
open("pretty_output.json", "w") do f
    write(f, JSON.json(data, pretty=true))
end
