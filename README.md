# Prison-Architect-to-3d-model-converter
This is a repository for my Prison Architect save file to 3d model converter.<br>
Requirements:
<ul> 
  <li>Python 3</li>
  <li>Voxelfuse library</li>
  <li>Prison architect save file</li>
</ul>
Install:
<ul> 
  <li>Download the python script</li>
  <li>Install voxelfuse</li>
  <li>Place the savefile next to the script and run the script</li>
  <li>Follow the prompts</li>
</ul>
Notes:
<ul> 
  <li>The script will not extract objects as that would require for me to have 3d versions of every object in prison architect</li>
  <li>The script will not extract tile textures as voxelfuse library can't assign textures to models, only simple colours</li>
  <li>The extraction time will vary but generally speaking it will take about an hour (that's a lot of models to process)</li>
</ul>
What can be done with the model?:<br>
Generally speaking whatever you want. Blender can import .stl files so you can just go wild.<br>
How it works:<br>
For each tile the program takes it's location and material. Then based on this data it generates a cuboid with the height varying based on the material.
If the tile has the indoor tag it will generate a cuboid above the previously generated cuboid for the tile.
