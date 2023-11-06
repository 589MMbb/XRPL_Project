def calculate_air_rights_value(baseline, factors, max_buildable_sqft, existing_sqft):
    print(f"Received baseline: {baseline}, type: {type(baseline)}")  # Debugging line
    print(f"Received factors: {factors}, type: {type(factors)}")  # Debugging line
    print(f"First factor value: {factors[0]}, type: {type(factors[0])}")  # Debugging line
    
    total_developable_space = max_buildable_sqft - existing_sqft
    v = baseline
    for factor in factors:
        v *= factor
    return v * total_developable_space