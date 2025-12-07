import trimesh
import sys
import numpy as np

def load_mesh(fileName):
    '''
    Load the mesh file, checking if it is an STL or OBJ file
    Parameter:
    - fileName (stl): Geometry file
    '''
    mesh = trimesh.load(fileName, "stl")
    return mesh

def create_box(box_size=10.0, ruota=False, tol=0.99):
    '''
    Create a box mesh centered at the origin with given dimensions.
    Parameters:
    - box_size (float): The size of the box (length of each side).
    - ruota (bool): If the TPMS is rotated or not
    - tol (float): Sligth tolerance in the cutting geometry dimensions, when rotated

    Returns:
    - box (trimesh.Trimesh): The box mesh.
    '''
    if not ruota:
        # Create a cube
        # box = trimesh.creation.box(extents=[box_size*tol, box_size*tol, box_size*tol])
        box = trimesh.creation.box(extents=[box_size*tol, box_size*tol, box_size*tol])
    else:
        # Create a box with larger size in y,z directions
        # tol is useful to have a bit of tolerance in the cutting and splitting of the geometry
        rad2 = 1.41421*tol
        box = trimesh.creation.box(extents=[box_size, box_size*rad2, box_size*rad2])

    return box

def intersect_mesh_with_box(mesh, box):
    '''
    Intersect a mesh with a box.
    Parameters:
    - mesh (trimesh.Trimesh): The mesh to intersect.
    - box (trimesh.Trimesh): The box to intersect with.

    Returns:
    - list of trimesh.Trimesh: Separated meshes from the intersection.
    '''
    intersection = mesh.intersection(box)
    if intersection.is_empty:
        return []
    return intersection.split()

def find_point_inside_mesh(mesh, max_attempts=10000):
    '''
    Find a point inside the mesh, within a cube of specified size.
    Parameters:
    - mesh (trimesh.Trimesh): The mesh to check.
    - max_attempts (float): Max numbers of attempts to search for a point within the mesh.

    Returns:
    - point (array[3,1]): Point within the mesh.
    '''
    bounds = mesh.bounds
    min_bounds = bounds[0]
    max_bounds = bounds[1]

    for _ in range(max_attempts):          
        point = np.random.uniform(low=min_bounds, high=max_bounds)
        
        # Check if the point is inside the mesh
        if mesh.contains([point])[0]:
            return point

    raise ValueError("Failed to find a point inside the mesh after {} attempts.".format(max_attempts))

def update_snappyHexMeshDict(snappyHexMeshDict_path, points, multiple=False):
    # Read the current snappyHexMeshDict file
    with open(snappyHexMeshDict_path, 'r') as file:
        lines = file.readlines()

    # Prepare the replacement lines
    if not multiple:
        replacement_line = f"    locationInMesh ({points[0][0]} {points[0][1]} {points[0][2]});\n"
    else:
        replacement_lines = "    locationsInMesh\n    (\n"
        for i, point in enumerate(points):
            replacement_lines += f"        (({point[0]} {point[1]} {point[2]}) region{i})\n"
        replacement_lines += "    );\n"

    # Write the updated lines back to the file
    with open(snappyHexMeshDict_path, 'w') as file:
        inside_locations_in_mesh = False
        for line in lines:
            if not multiple and "locationInMesh" in line:
                file.write(replacement_line)
            elif not multiple and "locationsInMesh" in line:
                inside_locations_in_mesh = True
                file.write(replacement_line)
            elif multiple and "locationInMesh" in line:
                file.write(replacement_lines)
            elif multiple and "locationsInMesh" in line:
                inside_locations_in_mesh = True
                file.write(replacement_lines)
            elif inside_locations_in_mesh and line.strip() == ");":
                inside_locations_in_mesh = False
            elif not inside_locations_in_mesh:
                file.write(line)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 findInsidePoint.py <snappyHexMeshDict> <path_to_stl> <ruota>")
        sys.exit(1)

    snappyHexMeshDict_path = sys.argv[1]
    stl_file = sys.argv[2]
    ruota = eval(sys.argv[3])
    ruota = eval(sys.argv[3])
    points = []

    mesh = load_mesh(stl_file)
    box = create_box(ruota=ruota)
    separated_meshes = intersect_mesh_with_box(mesh, box)

    for i, submesh in enumerate(separated_meshes):
        try:
            point_inside = find_point_inside_mesh(submesh)
            print(f"Found a point inside submesh {i}: {point_inside}")
            points.append(point_inside)
        except ValueError as e:
            print(f"Failed to find a point inside submesh {i}: {e}")
    
    if len(separated_meshes) == 1:
        print(f"Found 1 mesh" )
    else:
        print(f"Found {len(separated_meshes)} separated meshes\n") 
    
    if len(separated_meshes) == 1:
        print(f"Found 1 mesh" )
    else:
        print(f"Found {len(separated_meshes)} separated meshes\n") 

    if points:
        update_snappyHexMeshDict(snappyHexMeshDict_path, points, len(separated_meshes)>1)
