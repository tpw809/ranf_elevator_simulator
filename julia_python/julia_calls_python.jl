# calling python from julia:
using PyCall
math = pyimport("math")
math.sin(1.0)
