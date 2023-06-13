"""
MIT License

Copyright (c) 2023 Daniel Virgen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""



bl_info = {
    "name": "CSV Material Swapper",
    "author": "Daniel Virgen",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tool Shelf > CSV Material Swapper",
    "description": "Swaps the materials of all selected objects according to the information on a csv file and a blend file with all the materials.",
    "warning": "",
    "wiki_url": "",
    "category": "External Data"}


import bpy
import csv
from io import StringIO
from bpy.props import StringProperty
from bpy.types import Operator, Panel


# Function to read the CSV file and populate the dropdown list
def read_csv_file(self, context):
    csv_path = bpy.path.abspath(bpy.context.scene.my_csv_path)
    dropdown_items = []
    main_delimiter = ","
    alternate_delimiters = [";", "|"]  # List of alternate delimiters

    with open(csv_path, 'r') as file:
        content = csv.reader(file)
        content = file.read()
    
    # Replace alternate delimiters with the main delimiter
    for delimiter in alternate_delimiters:
        content = content.replace(delimiter, main_delimiter)

    # Create a StringIO object to mimic a file for the csv.reader
    csvfile = StringIO(content)

    # Create the csv.reader with the main delimiter
    rdr = csv.reader(csvfile, delimiter=main_delimiter)

    data = list(rdr)

    first_row = data[0]
    dropdown_items = first_row

    bpy.types.Scene.my_dropdown_items = bpy.props.EnumProperty(
        name="Items",
        items=[(item, item, '') for item in dropdown_items]
    )

    return {'FINISHED'}


# Function to swap the original materials for its corresponding materials on the csv file.
def Swap_Materials(self, context):
    selected_item = bpy.context.scene.my_dropdown_items

    csv_path = bpy.path.abspath(bpy.context.scene.my_csv_path)
    blend_File_Path = bpy.context.scene.my_blend_path
    dropdown_items = []
    main_delimiter = ","
    alternate_delimiters = [";", "|"]  # List of alternate delimiters

    with open(csv_path, 'r') as file:
        content = csv.reader(file)
        content = file.read()
    
    # Replace alternate delimiters with the main delimiter
    for delimiter in alternate_delimiters:
        content = content.replace(delimiter, main_delimiter)

    # Create a StringIO object to mimic a file for the csv.reader
    csvfile = StringIO(content)

    # Create the csv.reader with the main delimiter
    rdr = csv.reader(csvfile, delimiter=main_delimiter)

    data = list(rdr)     
    first_row = data[0]
    second_row = data[1]

    selected_index = first_row.index(selected_item)

    print("Selected item:", selected_item)
    print("Second row:", second_row)
    print("Selected index:", selected_index)
    print("data: ", data)

    if bpy.context.selected_objects != []:
        for obj in bpy.context.selected_objects:              
            if obj.type == 'MESH':                
                for slot in obj.material_slots:
                    for identfier in data[1]:
                        if identfier in slot.material.name:
                            print("material found")
                            print("identifier: ", identfier)
                            print("identifier index", data[1].index(identfier))
                            column_index = data[1].index(identfier)
                            if column_index == selected_index:
                                break  
                            column_values = [row[column_index] for row in data]
                            print("column ", column_values)
                            for item in column_values:
                                if slot.material.name == item:
                                    print("material found In column")
                                    row_index = column_values.index(slot.material.name)
                                    print("Row index ", row_index)
                                    if data[row_index][selected_index]:
                                        print("new material name: ", data[row_index][selected_index])
                                        new_material_name = data[row_index][selected_index]
                                        material_path = bpy.path.abspath(blend_File_Path) + "\\Material\\"
                                        bpy.ops.wm.append(filename=new_material_name, directory=material_path)
                                        slot.material = bpy.data.materials[new_material_name]   
        bpy.ops.outliner.orphans_purge()
        print("Removed Orphan Data")                                                             

    return {'FINISHED'}


# UI Panel
class CSVPanel(Panel):
    bl_label = "CSV Panel"
    bl_idname = "OBJECT_PT_csv_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Material Swapper'
    bl_label = "Material Swapper"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        layout.prop(scene, "my_csv_path")
        layout.operator("object.read_csv", text="Read CSV")
        layout.prop(scene, "my_blend_path")

        if hasattr(scene, "my_dropdown_items"):
            layout.prop(scene, "my_dropdown_items")
            layout.operator("object.swap_materials", text="Swap Materials")


# Operator to read the CSV file
class ReadCSVOperator(Operator):
    bl_idname = "object.read_csv"
    bl_label = "Read CSV"

    def execute(self, context):
        return read_csv_file(self, context)


# Operator to print the selected item
class SwapMaterialsOperator(Operator):
    bl_idname = "object.swap_materials"
    bl_label = "Swap Materials"

    def execute(self, context):
        return Swap_Materials(self, context)


classes = (
    CSVPanel,
    ReadCSVOperator,
    SwapMaterialsOperator
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_csv_path = StringProperty(
        name="CSV Path",
        subtype='FILE_PATH',
        default=""
    )
    bpy.types.Scene.my_blend_path = StringProperty(
        name="Blend File Path",
        subtype='FILE_PATH',
        default=""
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_csv_path
    del bpy.types.Scene.my_blend_path


if __name__ == "__main__":
    register()
