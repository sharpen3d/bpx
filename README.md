# bpx
Blender 'Pixel Perfect' Extensions and Asset Library created by Luke Stilson (sharpen3d)

This repo holds primarily python tools related to art creation in Blender
It is recommended to use these scripts and associated files with the most recent stable version of Blender

Latest stable version Blender 3.1.2 - https://www.blender.org/download/

# Tools and Scripts
This repo includes the following scripts to be ran as modules, extending the functionality, improving ease-of-use, and simplifying workflows

- Word Artist
  Non-destructive font editing, improvement on Blender's default 3D font - using custom node_groups for geometry nodes and shaders

- 2D Tools
  Tools for creating accurate pixel-sized planes and standardized methods and workflow for working with a 2D (orthographic) camera
  Helps to match and preview Blender exports and 3D models to standard Unity 2D templates

Quick Actions
  Panel of useful tools to reduce mouse clicks. Includes tools for quick render exports, world setup

File Manager
  Similar to After Effects 'Collect Files' functionality. Locates, copies, and places external data in to a directory beside the .blend, 
  then reassociates all the external data to a relative path to the new (copied) files.
  For file-sharing and render farm use, where external data should be visible and accessible unlike 'pack resources'

Geo Emitters
  Experimental tool for creating particle systems entirely with Geometry Nodes. 
  This allows for 'particle lifetime' to be accessible within the EEVEE renderer,
  and allows for unlimited utility expansion for particle behavior

Grid Packer
  Automatically render the current .blend OR any (square power of 2) image sequence to a (square power of 2) sprite sheet
  Acts like the Grid/Strip method in TexturePacker, does not 'pack' by removing transparent space,
  rather this simply places all images of a sequence or rendered output sequentially in a grid

Tools Manager
  UI for managing the scripts included in this repo, acts as a defacto plugin library for these specific scripts
  More transparency and flexibility than creating these tools as plugins
  Allows for automatic appending of necessary node_groups, shaders, etc
  
# Resources and Assets
This repo includes an asset library of custom shaders, geometry node_groups

- Shaders/Materials
  Procedural Gradients
    Linear and Radial gradient templates (simple, masked, holdout)
    Object gradients (over global X, Y, Z of object)
    True-color gold gradients (gold master, 8 unique gold gradient node_groups)
  Image Shaders
    True-color image shader (Unlit)
    True-color image shader with alpha (Unlit with Alpha)
  Animated Shaders
    Procedural looping and clamped positional texture coordinate mapping (Scrolling UV's, Rotating UV's)
  Fake Lighting Shaders
    Applies gradients in regard to Normal direction without the use of 'lights' in scene (Toon Lighting, True-Color Lighting)

- Meshes/Geometry Nodes
  Animation Geometry Nodes
    Examples and node_groups for simple linear animation with Geometry Nodes
  Shadow Plane
    Geometry node_group for shadow plane setup in EEVEE

# Comments
Raising comments, suggestions, and bug reports on scripts and associated files is encouraged.
When reporting an issue please adhere to the following guidelines to ensure clear communication:
 - Simple explanation of the issue
 - Steps to reproduce the issue
 - Screenshot or link to a file experiencing the issue if applicable

# Current Efforts:
This repo is continuously changing, expanding, and improving. Ongoing and upcoming changes listed below
- adding tooltips and descriptions to current tools code
- adding 'help' functionality pointing to documentation of code functionality
- documenting illustrative support for tools and implementation
- creating a breadth of template .blend files utilizing specific aspects of tools
- adding more 'Quick Tools' functionality
- improving workflow and best practices in current tools
- improved workflow for practical use of custom node_groups

# Future Efforts:
As this repo expands, this is the intended direction for future functionality
- tools for Unity workflow integration with Blender (rendered output and 3D integration)
- standardized template workflows for Cycles and EEVEE renders
- Software utility integration (i.e. workflow improvement Illustrator>Blender, PS>Blender, Blender>AE)
- Unity art tools integration
- Blender to Unity (GLSL) shader integration
