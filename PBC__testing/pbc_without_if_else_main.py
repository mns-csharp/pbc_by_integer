from pbc_without_if_else import PBC3WithoutIfElse, AxesTypeEnum, Vec3

if __name__ == "__main__":
    box_length = 10.0  # Define the physical size of the simulation box
    pbc = PBC3WithoutIfElse(box_length, AxesTypeEnum.NEGATIVE_POSITIVE)

    # Define some test points
    point1 = Vec3(-6.0, 0.0, 25.5)  # Outside the box range
    point2 = Vec3(-5.0, 5.0, 4.99999999)

    # Wrap the points using periodic boundary conditions
    wrapped_point1 = pbc.wrap(point1)
    wrapped_point2 = pbc.wrap(point2)

    print(f"Original Point 1: {point1}, Wrapped: {wrapped_point1}")
    print(f"Original Point 2: {point2}, Wrapped: {wrapped_point2}")

    # Compute the squared minimum image convention (MIC) distance
    dist_sqr = pbc.distance_sqr(wrapped_point1, wrapped_point2)
    dist = pbc.distance(wrapped_point1, wrapped_point2)
    print(f"Squared Distance (MIC): {dist_sqr}")
    print(f"Distance (MIC): {dist}")


