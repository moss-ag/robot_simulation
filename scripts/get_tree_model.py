def get_tree_model(name, x, y, z):
    """
    Get the two string sections needed to create an object in a world file.

    Args
    ----
        name (str): the name of this vine
        x (float): x coordinate of the vine
        y (float): y coordinate of the vine
        z (float): z coordinate of the vine

    Returns
    -------
        tree_str (str): the string to include a tree

    """
    tree_str = """
    <include>
      <uri>https://fuel.ignitionrobotics.org/1.0/shrijitsingh99/models/Juniper Tree</uri>
      <name>'{}'</name>
      <pose>{:.5f} {:.5f} {:.5f} 0 0</pose>
    </include>""".format(
        name, x, y, z
    )

    return tree_str
    
