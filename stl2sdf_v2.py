import os # to walk through directories, to rename files
import sys

# Libraries
import trimesh # for converting voxel grids to meshes (to import objects into simulators)

# Modules
import tools_sdf_generator
import tools_mesh_splitter

if __name__ == "__main__":

    print("Usage: ")
    print("python {} <FILEPATH> scaling_factor".format(sys.argv[0]))
    print("Example:\npython {} <FILEPATH> 1.0".format(sys.argv[0]))

    filename = sys.argv[1]
    scaling_factor = float(sys.argv[2])
    mass = []
    center_of_mass = []
    moments_of_inertia = []
    stlpath = []
    object_model_name = []

    # Generate a folder to store the images
    print("Generating a folder to save the mesh")
    # Generate a folder with the same name as the input file, without its ".binvox" extension
    currentPathGlobal = os.path.dirname(os.path.abspath(__file__))
    directory = currentPathGlobal + "/" + filename + "_sdf"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filelist = tools_mesh_splitter.detect_and_split_mesh(filename,directory)

    i = 0
    while i < filelist[-1]:
        mesh = trimesh.load(filelist[i] + '.obj')
        object_model_name.append(filelist[i])
        # scaling_factor = 100
        mesh.apply_scale(scaling=scaling_factor)

        mass.append(mesh.volume) # WATER density
        print("\n\nMesh volume: {} (used as mass)".format(mesh.volume))
        print("Mass (equal to volume): {0}".format(mass[i]))
        print("Mesh convex hull volume: {}\n\n".format(mesh.convex_hull.volume))
        print("Mesh bounding box volume: {}".format(mesh.bounding_box.volume))

        print("Merging vertices closer than a pre-set constant...")
        mesh.merge_vertices()
        print("Removing duplicate faces...")
        mesh.remove_duplicate_faces()
        print("Making the mesh watertight...")
        trimesh.repair.fill_holes(mesh)
        # print("Fixing inversion and winding...")
        # trimesh.repair.fix_winding(mesh)
        # trimesh.repair.fix_inversion(mesh)
        trimesh.repair.fix_normals(mesh)

        print("\n\nMesh volume: {}".format(mesh.volume))
        print("Mesh convex hull volume: {}".format(mesh.convex_hull.volume))
        print("Mesh bounding box volume: {}".format(mesh.bounding_box.volume))

        print("Computing the center of mass: ")

        center_of_mass.append(mesh.center_mass)
        print(center_of_mass[i])

        print("Computing moments of inertia: ")

        moments_of_inertia.append(mesh.moment_inertia)
        print(moments_of_inertia[i])  # inertia tensor in meshlab

        print("Generating the STL mesh file")
        trimesh.exchange.export.export_mesh(
            mesh=mesh,
            file_obj=directory + "/" + filelist[i] + ".stl",
            file_type="stl"
        )

        stlpath.append(directory + "/" + filelist[i] + ".stl")
        i += 1

    print("Generating the SDF file...")

    tools_sdf_generator.generate_model_sdf(
        directory=directory,
        object_name=object_model_name,
        center_of_mass=center_of_mass,
        inertia_tensor=moments_of_inertia,
        mass=mass,
        links=filelist[-1],
        model_stl_path=stlpath,
        scale_factor = 1.0) #scale_normalisation_factor)
