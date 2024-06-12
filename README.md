# Particle Simulator 

Group Members:
- Clarissa Audrey Fabiola Kusnadi - 2602118490
- Jeffrey - 2602118484
- Pranav Harish Nathani - 2702293872
- Priscilla Abigail Munthe - 2602109883

This particle simulator is written using Python. 
Using the GUI, you can easily create and edit scenes and play with them in real-time.


## Required modules <a name="Required_modules"></a>
- pynput
- numpy
- cv2 (OpenCV) 
- PIL

To install, paste the following command inside the designated terminal:
```
pip install -r requirements.txt   
```

## Shortcuts and toolbar <a name="Shortcuts_and_toolbar"></a>
At the top of the screen, you can see the toolbar with the different mouse modes and some buttons.

### Mouse-modes <a name="Mouse-modes"></a>
In the toolbar, you can see 3 different mouse-modes, being to select, move and add particles.
By default, move will be selected. <br> Scrolling up or down will change the cursor-size,
which gets represented by a circle around your cursor.
- **Move:** When you’re in the ‘move’ mouse-mode, you can move particles by dragging them around.
            The amount of particles that get moved depends on your cursor-size.
            When multiple particles are select and you move one of the particles from your selection,
            all the particles in the selection will be moved.
- **Select:** When you’re in the ‘select’ mouse-mode, you can select particles by clicking or dragging. 
              To deselect them, you can simply click outside of your selection.
              The amount of particles that get selected depends on your cursor-size.
- **Add:** When you’re in the ‘add’ mouse-mode, you can add particles by clicking, 
           dragging or holding the left-mouse button.
           By default, the size of the particles is set to the cursor-size, 
           but you can simply change this setting in the particle-settings tab (see 'particle-settings').
 
 ### Buttons <a name="Buttons"></a>
- **Pause button:** Starts and stops the simulation
- **Link button:** Links the selected particles (does the same as pressing 'L')


### Shortcuts <a name="Shortcuts"></a>
- **RMB:** erase particles
- **DELETE:** delete selected particles
- **SPACE:** pause / unpause simulation
- **CTRL+A:** select all
- **CTRL+C:** copy selected particles
- **CTRL+V:** paste
- **CTRL+X:** cut selected particles
- **CTRL+L:** lock selected particles
- **CTRL+SHIFT+L:** 'unlock' selected particles
- **R (hold) + scroll:** rotate selected particles (rotation amount depends on the cursor-size)


Note: Most shortcuts won't work when the canvas isn't 'selected' or 'focused'.
To reset the focus, you can click the canvas with one of the mouse-modes selected.

## Simulation-settings <a name="Simulation-settings"></a>
- **Gravity:** Gravity-strength (float)
- **Air Resistance:** Amount of air resistance, a particle's velocity gets multiplied by "1 - air resistance" 
                      (float, values range from 0 to 1)
- **Ground Friction:** Amount of friction between the edges of the canvas and a particle (float, values range from 0 to 1)
- **Temperature:** Strength of random velocity that gets added to a particle's velocity (float)
- **Simulation Speed:** Speed at which the simulation runs. Does not change the fps! 
                        Setting it too high might result in inaccurate simulations and particles might not be able to go 
                        to a stable position. (float)
- **Display FPS:** When set to True, the current fps will be displayed in the top left corner of the screen (bool)
- **Display Particles Amount:** When set to True, the amount of particles in the simulation will be displayed in the 
                           top left corner of the screen (bool)
- **Blocking edges:** 'top', 'bottom', 'left' and 'right' checkboxes determine whether that edge of the canvas 
                       acts like a wall (booleans) 


## Particle-settings <a name="Particle-settings"></a>
In the particles-tab, you can see the settings that particles will have when you spawn them. 
You can also change the settings of existing particles using the ‘set selected’ and ‘set all’ buttons. 
To see the properties of a certain particle, you can simply select it and click on ‘copy from selected’. 
This will display all the settings from that particle in the particle-tab. If you do this with 
multiple particles selected, the fields of the settings that they don’t have in common will be left empty.

- **Radius:** Radius of circle drawn on the screen, only affects physics when 'Check Collisions' is set to True 
              (int or 'scroll' to set it to the current cursor-size)
- **Color:** Color of circle drawn on the screen, no effect on physics 
            (change color by pressing 'preview-square' and selecting a color,
             typing it as a list, eg. [255, 0, 0] for red or setting it to 'random' for a random color)
- **Mass:** Mass of particle (float)
- **Bounciness:** Bounciness of particle, particle-velocity gets multiplied by this value when hitting an edge 
                  (float, values range from 0 to 1)
- **Velocity:** Current velocity of particle (x and y components: floats)
- **Locked:** When set to True, the particle won't move, but will still affect other particle (bool)
- **Check Collisions:** Handles particle-collisions, based on radius, does not work when 'Use Grid' is set to True,
                        !not recommended in simulations with many particles: using repel-radius works better (bool)
- **Attraction-radius\*:** Minimum distance between particles before the attraction force gets applied (float)
- **Attr-strength:** Attraction force coefficient (float)
- **Gravity-Mode:** When set to True, attraction force will be calculated with gravity-equation 
                    instead of spring equation (bool)
- **Repulsion-radius:** Minimum distance between particles before the repulsion force gets applied,
                        attraction force won't be applied when repulsion force gets applied (float)
- **Repel-strength:** Repulsion force coefficient (float)

###### *: When setting this to a negative number, this value gets interpreted as infinity
