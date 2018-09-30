## Bounce Visualization
A collection of python utilities for visibility-based decomposition of 
polygons, and strategy generation for mobile "bouncing" robots.

## Installation and Setup for macOS
1. Clone this repository into $bounce_viz:

   ```bash
   export bounce_viz=/desired/absolute/path/to/bounce_viz/ # set absolute path as desired, no space around "="
   git clone --recurse-submodules git@github.com:alexandroid000/bounce_viz.git $bounce_viz
   ```

2. Install Python 3.6
   ```bash
   brew install python
   ```
3. Install all other python libraries specified above
   ```bash
   pip3 install -r requirements.txt
   ```
   (requirements.txt is a file in the root directory of this project.)
## Quick Start
   ```bash
   cd $bounce_viz
   cd test
   ./run_sim.py
   ```
## Generate Documentations
   ```bash
   cd $bounce_viz
   cd docs
   make apidoc
   # to view the documentation
   open ./build/html/bounce_viz.html
   ```
