# pip install julia
# python -m julia.sysimage
# python -m julia.install

from julia import Julia
jl = Julia(compiled_modules=False)

from julia import Main

# Define a Julia function
Main.eval("""
function add_two_numbers(x, y)
    return x + y
end
""")

# Call it from Python
result = Main.add_two_numbers(3, 5)
print(result)   # 8


# Calling julia packages from python:
from julia import Pkg
Pkg.add("Statistics")

from julia import Statistics

print(Statistics.mean([1, 2, 3, 4]))


# pass objects to julia:
# from julia import Main

Main.eval("f(x) = sum(x)")

print(Main.f([10, 20, 30]))   # 60


# call julia script:

# use subprocess:
import subprocess

result = subprocess.run(
    ["julia", "myscript.jl"],
    capture_output=True,
    text=True
)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)

data = json.loads(result.stdout)
print(data)


# load and execute a julia script using pyjulia:
from julia import Julia
jl = Julia(compiled_modules=False)

from julia import Main

Main.include("myscript.jl")
print(Main.greet("Bob"))

Main.include("myscript.jl")
result = Main.compute_stats([1,2,3,4,5])
print(result)
