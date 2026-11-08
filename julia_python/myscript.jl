println("Hello from Julia!")
println(2 + 3)

function greet(name)
    println("Hello, $name from Julia!")
    return "done"
end

function compute_stats(x)
    return (mean = mean(x), std = std(x))
end

using JSON

data = Dict("a" => 1, "b" => [1,2,3])
println(JSON.json(data))