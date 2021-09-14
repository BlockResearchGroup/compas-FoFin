from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino

from compas_fofin.rhino import get_scene
from compas_fofin.rhino import FF_undo
from compas_fofin.rhino import FF_error


__commandname__ = "FFcablemesh_modify_edges"


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

    options = ["All", "AllBoundaryEdges", "Continuous", "Parallel", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type", strings=options)

    if not option:
        return

    if option == "All":
        keys = keys = list(cablemesh.datastructure.edges())

    elif option == "AllBoundaryEdges":
        keys = cablemesh.datastructure.edges_on_boundary()

    elif option == "Continuous":
        temp = cablemesh.select_edges()
        keys = list(set(flatten([cablemesh.datastructure.edge_loop(key) for key in temp])))

    elif option == "Parallel":
        temp = cablemesh.select_edges()
        keys = list(set(flatten([cablemesh.datastructure.edge_strip(key) for key in temp])))

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
    #         for (u, v) in pattern.datastructure.edges():
    #             if if_constraints(pattern.datastructure, u, guid) and if_constraints(pattern.datastructure, v, guid):
    #                 keys.append((u, v))

    #     compas_rhino.rs.HideObjects(guids)
    #     pattern.settings['color.edges'] = current

    elif option == "Manual":
        keys = cablemesh.select_edges()

    if keys:
        # ModifyAttributesForm.from_sceneNode(pattern, 'edges', keys)
        # scene.update()
        public = [name for name in cablemesh.datastructure.default_edge_attributes.keys() if not name.startswith('_')]
        if cablemesh.update_edges_attributes(keys, names=public):
            cablemesh.settings['_is.valid'] = False
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
