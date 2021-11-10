from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error
from compas_fofin.rhino import select_vertices


__commandname__ = "FFcablemesh_move_nodes"


@FF_error()
@FF_undo
def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    cablemesh = scene.get("cablemesh")[0]
    if not cablemesh:
        print("There is no CableMesh in the scene.")
        return

    options = ["free", "x", "y", "z", "xy", "yz", "zx"]
    option = compas_rhino.rs.GetString("Set Direction.", strings=options)
    if not option:
        return

    direction = option

    options1 = ["ByContinuousEdges", "Manual"]
    option1 = compas_rhino.rs.GetString("Selection Type.", strings=options1)
    if not option1:
        return

    if option1 == "ByContinuousEdges":
        temp = cablemesh.select_edges()
        keys = list(set(flatten([cablemesh.datastructure.vertices_on_edge_loop(key) for key in temp])))

    # elif option == "ByConstraints":
    #     guids = pattern.datastructure.vertices_attribute('constraints')
    #     guids = list(set(list(flatten(list(filter(None, guids))))))

    #     if not guids:
    #         print('there are no constraints in this pattern')
    #         return

    #     current = pattern.settings['color.edges']
    #     pattern.settings['color.edges'] = [120, 120, 120]
    #     scene.update()

    #     compas_rhino.rs.ShowObjects(guids)

    #     def custom_filter(rhino_object, geometry, component_index):
    #         if str(rhino_object.Id) in guids:
    #             return True
    #         return False

    #     constraints = compas_rhino.rs.GetObjects('select constraints', custom_filter=custom_filter)

    #     if not constraints:
    #         return

    #     def if_constraints(datastructure, key, guid):
    #         constraints = datastructure.vertex_attribute(key, 'constraints')
    #         if constraints:
    #             if str(guid) in constraints:
    #                 return True
    #         return False

    #     keys = []
    #     for guid in constraints:
    #         for key in pattern.datastructure.vertices():
    #             if if_constraints(pattern.datastructure, key, guid):
    #                 keys.append(key)

    #     keys = list(set(keys))

    #     compas_rhino.rs.HideObjects(guids)
    #     pattern.settings['color.edges'] = current

    elif option1 == "Manual":
        keys = cablemesh.select_vertices()

    if keys:
        compas_rhino.rs.UnselectAllObjects()
        select_vertices(cablemesh, keys)

        if direction == 'free':
            move = cablemesh.move_vertices(keys)
        else:
            move = cablemesh.move_vertices_direction(keys, direction=direction)
        
        if move:
            cablemesh.settings['_is.valid'] = False
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
