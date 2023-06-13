<div align="center">
  
# CSV Material Swapper

Add-on that allows you to swap the materials of selected objects based on information from a CSV file and a reference .blend file containing all the materials. It provides an efficient way to update and manage interchangable sets of Materials.

![](img/Material_Swapper_Demo_01_Full.gif)
</div>

## Features

- Swaps the materials of all selected objects according to the information provided in a CSV file.
- Supports CSV files with different delimiters, including commas, semicolons, and vertical bars.
- Provides a dropdown list populated with the column names from the CSV file, allowing you to select the desired material property for swapping.
- Supports reading and writing CSV files in a user-friendly format.
- Orphaned materials are removed after each usage.


## Installation

1. Download the ["CSV_Material_Swapper.py"](CSV_Material_Swapper.py) file.
2. Launch Blender and go to **Edit > Preferences > Add-ons**.
3. Click on the "Install" button and navigate to the downloaded file.
4. Select the file and click "Install Add-on".
5. Enable the "CSV Material Swapper" add-on by ticking the checkbox.

## Usage 

**addon**
1. Locate the "Material Swaper" section of in the 3D Viewport Tool Shelf.
2. Provide the path to the CSV file containing the material information using the "CSV Path" field.
3. Click the "Read CSV" button to populate the dropdown list with the available material groups.
4. Specify the path to the blend file containing the materials using the "Blend File Path" field.
5. Select the desired material property from the dropdown list.
6. Click the "Swap Materials" button to replace the materials of the selected objects with the ones in the selected material group.
<p align="center">
<img src=img/Material_Swapper_Image.png width="400">
</p>
**csv file**
- The first row of the file should only contain the name of the material groups
- The second row should contain identifier codes for each group
- From the third row on, the file should contain a list of all swappable materials, each column is a material group, and each material with be paired with the other materials in the same row.
- Each material name should contain the identifier of its material group (Column), it doesn't matter if the identifier is a prefix, a sufix or if it is in the middle of the name. 

<p align="center">
<img src=img/Example_CSV_Image.png width="500">
</p>

**Reference .blend File**
- All materials listed in the csv file should be contained in a separate .blend file.
- They should have all the exact same name as in the CSV file
- It doesn't matter in which object the materials are applied.
<p align="center">
<img src=img/Reference_File.png width="500">
</p>


Enjoy using the CSV Material Swapper add-on!

## Compatibility

- Blender 2.80 and above.

## Credits

- **Author**: Daniel Virgen


