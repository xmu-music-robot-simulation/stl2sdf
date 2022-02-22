def generate_model_sdf(directory, object_name, center_of_mass, centroids, inertia_tensor, mass, links, model_stl_path, scale_factor):

    # http://sdformat.org/spec?ver=1.6&elem=visual

    object_is_static = 0
    max_contacts = 20 # maximum numnber of contact points on the object, when detecting collisions

    # Object mass format: scalar
    # Center of Mass format: [x,y,z]
    # Inertia tensor format:
    # | ixx ixy ixz |
    # | ixy iyy iyz |
    # | ixz iyz izz |
    ixx = []
    ixy = []
    ixz = []
    iyy = []
    iyz = []
    izz = []
    i = 0
    while i < links:
        ixx.append(round(inertia_tensor[i][0][0], 5))
        ixy.append(round(inertia_tensor[i][0][1], 5))
        ixz.append(round(inertia_tensor[i][0][2], 5))
        iyy.append(round(inertia_tensor[i][1][1], 5))
        iyz.append(round(inertia_tensor[i][1][2], 5))
        izz.append(round(inertia_tensor[i][2][2], 5))
        i += 1

    scale_factor = str(round(scale_factor,3))

    sdf_model_file_text = "<?xml version='1.0'?>\n"
    sdf_model_file_text += \
    '<sdf version="1.6"> \n \n \
        <model name="' + 'mesh' + '"> \n \
            <static>' + str(object_is_static) + '</static> \n \
            <self_collide>0</self_collide> \n \
            <allow_auto_disable>1</allow_auto_disable> \n \n \
            <frame name="object_frame"> \n \
                <pose frame="/world">0 0 0 0 -0 0 </pose> \n \
            </frame> \n \n \
            <pose frame="/world">0 0 0 0 -0 0</pose> \n \n'
    i = 0
    while i < links:
        sdf_model_file_text +=\
        '        <link name="' + object_name[i] + '"> \n \n \
                    <gravity>1</gravity> \n \
                    <self_collide>0</self_collide> \n \
                    <kinematic>0</kinematic> \n \n \
                    <frame name="link_frame"> \n \
                        <pose frame="object_frame">0 0 0 0 -0 0</pose> \n \
                    </frame> \n \n \
                    <!-- red green blue offsets: model pivot point --> \n \
                    <!-- 32 is just half of the voxelgrid dimension (64)--> \n \
                    <pose name="link_frame"> ' + str(centroids[i][0])+ ' ' + str(centroids[i][1]) + ' ' + str(centroids[i][2]) + ' 0 -0 0</pose> \n \n \
                    <inertial> \n \
                        <mass>' + str(round(mass[i], 2)) + '</mass> \n \
                        <inertia> \n \
                            <!-- http://gazebosim.org/tutorials?tut=inertia&cat=build_robot --> \n \
                            <ixx>' + str(ixx[i]) + '</ixx> \n \
                            <ixy>' + str(ixy[i]) + '</ixy> \n \
                            <ixz>' + str(ixz[i]) + '</ixz> \n \
                            <iyy>' + str(iyy[i]) + '</iyy> \n \
                            <iyz>' + str(iyz[i]) + '</iyz> \n \
                            <izz>' + str(izz[i]) + '</izz> \n \
                        </inertia> \n \n \
                        <frame name="link_inertia_frame"> \n \
                            <pose frame="link_frame">0 0 0 0 -0 0</pose> \n \
                        </frame> \n \n \
                        <!-- \n \
                        This is the pose of the inertial reference frame, relative to the specified reference frame. \n \
                        The origin of the inertial reference frame needs to be at the center of gravity. \n \
                        The axes of the inertial reference frame do not need to be aligned with the principal axes of the inertia. \n \
                        --> \n \
                        <pose frame="link_inertia_frame">' + \
                            str(round(center_of_mass[i][0],2)) + ' ' + \
                            str(round(center_of_mass[i][1],2)) + ' ' + \
                            str(round(center_of_mass[i][2],2)) + ' 0 0 0 \
                        </pose> \n \
                    </inertial> \n \
                    \n \
                    <collision name="collision"> \n \
                        <!-- \n \
                            Maximum number of contacts allowed between two entities. \n \
                            This value overrides the max_contacts element defined in physics. \n \
                        --> \n \
                        <max_contacts>' + str(max_contacts) + '</max_contacts> \n \n \
                        <!-- A frame of reference to which a pose is relative. --> \n \
                        <frame name="collision_frame"> \n \
                            <pose frame="link_frame">0 0 0 0 -0 0</pose> \n \
                        </frame> \n \
                        <!-- A position(x,y,z) and orientation(roll, pitch yaw) with respect to the specified frame. --> \n \
                        <pose frame="collision_frame">0 0 0 0 -0 0</pose> \n \n \
                        <geometry> \n \
                            <mesh> \n \
                                <uri>' + model_stl_path[i] + '</uri> \n \
                                <!-- <uri>model://mymodel/meshes/model.stl</uri> --> \n \
                                <!-- Scaling factor applied to the mesh --> \n \
                                <scale>' + scale_factor + ' ' + scale_factor + ' ' + scale_factor + '</scale> \n \
                            </mesh> \n \
                        </geometry> \n \
                        <!-- http://sdformat.org/spec?ver=1.6&elem=collision#surface_soft_contact --> \n \
                        <surface></surface> \n \
                    </collision> \n \
                    \n \
                    <visual name="visual"> \n \
                        <cast_shadows>1</cast_shadows>\n \
                        <transparency>0</transparency>\n \n \
                        <frame name="visual_frame"> \n \
                            <pose frame="link_frame">0 0 0 0 -0 0</pose>\n \
                        </frame> \n \
                        <pose frame="visual_frame">0 0 0 0 -0 0</pose> \n \n \
                        <material> \n \n \
                            <script> \n \
                                <uri>file://media/materials/scripts/gazebo.material</uri>\n \
                                <!-- <name>Gazebo/TurquoiseGlowOutline</name> -->\n \
                                <name>Gazebo/Green</name>\n \
                            </script>\n \
                            <shader type="vertex">\n \
                              <normal_map>__default__</normal_map>\n \
                            </shader>\n \n \
                            <lighting>1</lighting> \n \
                            <ambient>0.15 0.75 0.35 1</ambient> \n \
                            <diffuse>0.1 0.95 0.25 1</diffuse> \n \
                            <specular>0.01 0.01 0.01 1</specular> \n \
                            <emissive>0 0 0 1</emissive> \n \
                        </material>\n \n \
                        <geometry> \n \
                            <mesh> \n \
                                <uri>' + model_stl_path[i] + '</uri> \n \
                                <!-- <uri>model://mymodel/meshes/model.stl</uri> --> \n \
                                <!-- Scaling factor applied to the mesh --> \n \
                                <scale>' + scale_factor + ' ' + scale_factor + ' ' + scale_factor + '</scale> \n \
                            </mesh> \n \
                        </geometry> \n \
                    </visual> \n \
                </link> \n'
        i += 1

    sdf_model_file_text +=\
    '    </model> \n \
    </sdf>'

    # Create the file
    f = open(directory + "/" + 'mesh' + ".sdf", "w")
    # Write the content to file
    f.write(sdf_model_file_text)
    # Close the file
    f.close()
