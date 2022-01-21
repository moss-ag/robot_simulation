def get_plane_model(md_name,lk_name,vs_name,xc, yc, w,l):
    
    plane_str = """
    <model name='{}'>
      <static>1</static>
      <link name='{}'>
        <visual name='{}'>
          <pose>{:.5f} {:.5f} 0 0 0</pose>
          <cast_shadows>0</cast_shadows>
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>{:.5f} {:.5f}</size>
            </plane>
          </geometry>
          <material>
            <script>
              <uri>file://media/materials/scripts/gazebo.material</uri>
              <name>Gazebo/WoodFloor</name>
            </script>
          </material>
        </visual>
      </link>
    </model>""".format(
        md_name,lk_name,vs_name, xc, yc, w,l
    )

    return plane_str
