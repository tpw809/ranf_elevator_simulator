function adams_style_velocity_adjusted_mu(
    velocity::Float64,
    mu_static::Float64,
    mu_dynamic::Float64,
    vel_trans_static::Float64,
    vel_trans_dynamic::Float64
)::Float64

    @assert mu_static ≥ 0.0 "mu_static ≤ 0.0"
    @assert mu_dynamic ≥ 0.0 "mu_dynamic ≤ 0.0"
    @assert mu_dynamic ≤ mu_static "mu_static ≤ mu_dynamic"
    @assert vel_trans_static > 0.0 "vel_trans_static ≤ 0.0"
    @assert vel_trans_dynamic > vel_trans_static "vel_trans_dynamic ≤ vel_trans_static"

    ω_static  = π / (2.0 * vel_trans_static)
    ω_dynamic = π / (vel_trans_dynamic - vel_trans_static)

    vabs = abs(velocity)
    sgn  = sign(velocity)

    if vabs ≥ vel_trans_dynamic
        return -mu_dynamic * sgn

    elseif vabs < vel_trans_static
        return -mu_static * sin(ω_static * velocity)

    else
        μ = mu_dynamic +
            ((mu_static - mu_dynamic) / 2.0) *
            (1.0 + cos(ω_dynamic * (velocity - vel_trans_static)))

        return -μ * sgn
    end
end
