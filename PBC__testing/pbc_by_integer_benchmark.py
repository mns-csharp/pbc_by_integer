import time
import random

# Assuming Vec3 and PBCByInteger are already defined as in your provided code
from pbc_by_integer import PBCByInteger, Vec3, AxesTypeEnum


def benchmark_wrap_function(pbc, num_iterations=100000):
    # Create random positions within the simulation box
    start_time = time.time()

    for _ in range(num_iterations):
        loc = Vec3(random.uniform(0, pbc.periodic_distance),
                   random.uniform(0, pbc.periodic_distance),
                   random.uniform(0, pbc.periodic_distance))
        pbc.wrap(loc)  # Call wrap function

    end_time = time.time()

    # Calculate elapsed time and report
    elapsed_time = end_time - start_time
    print(f"Time taken for {num_iterations} wrap operations: {elapsed_time:.6f} seconds")
    print(f"Average time per wrap operation: {elapsed_time / num_iterations:.10f} seconds")


# Example usage:
if __name__ == "__main__":
    # Set up a PBC system with a box length of 10.0 and a wrap function using the positive axes type
    pbc_system = PBCByInteger(box_length=10.0, axes_type=AxesTypeEnum.NEGATIVE_POSITIVE)

    # Benchmark the wrap function with 100000 iterations
    benchmark_wrap_function(pbc_system, num_iterations=100000)
