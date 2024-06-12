import numpy as np
import math

class Particle:
    boltzmann_constant = 1.380649e-23  # in m^2 kg s^-2 K^-1
    g_constant = 6.674e-11  # Gravitational constant in m^3 kg^-1 s^-2
    

    def __init__(self, sim, x, y, radius=0.004, color='random', mass=0.001,  
                 velocity=np.zeros(2), bounciness=0.7, locked=False, collisions=False, attract_r=-1, repel_r=0.01,
                 attraction_strength=0.5, repulsion_strength=1, linked_group_particles=True,
                 link_attr_breaking_force=-1, link_repel_breaking_force=-1,
                 group='group1', separate_group=False, gravity_mode=False):
        self.sim = sim
        self.x = x
        self.y = y
        self.r = radius
        if (color == 'random'):
            self.color = np.random.randint(0, 255, 3).tolist()
        else:
            self.color = color

        self.m = mass
        self.v = np.array(velocity).astype('float32')
        self.a = np.zeros(2)
        self.area = math.pi * (self.r ** 2)
        self.bounciness = bounciness
        self.collision_bool = collisions
        self.locked = locked

        self.attr_r = attract_r
        self.repel_r = repel_r
        self.attr = attraction_strength
        self.repel = repulsion_strength
        self.gravity_mode = gravity_mode

        self.return_all = None
        self.return_none = None
        self.range_ = None
        self.init_constants()

        self.linked = []
        self.link_lengths = {}
        self.linked_group_particles = linked_group_particles
        self.link_attr_breaking_force = link_attr_breaking_force
        self.link_repel_breaking_force = link_repel_breaking_force
        self.separate_group = separate_group

        self.group = group
        try:
            self.sim.groups[self.group].append(self)
        except KeyError:
            self.sim.groups[self.group] = [self]
            self.sim.gui.group_indices.append(int(self.group.replace('group', '')))

        self.collisions = []
        self.forces = []

        self.mouse = False

        self.sim.particles.append(self)

    def init_constants(self):
        self.return_all = self.attr_r < 0 and self.attr != 0
        self.return_none = self.attr == 0 and self.repel == 0 and not self.collision_bool
        if self.attr != 0 and not (self.collision_bool and self.r > self.attr_r):
            self.range_ = self.attr_r
        elif self.attr == 0 and self.repel != 0 and not (
                self.collision_bool and self.r > self.repel_r):
            self.range_ = self.repel_r
        else:
            self.range_ = self.r

    def mouse_p(self, event):
        if np.sqrt((event.x - self.x) ** 2 + (event.y - self.y) ** 2) <= max(int(self.sim.mr), self.r):
            if self.sim.mouse_mode == 'SELECT':
                self.select()
                return True

            self.mouse = True
            if self in self.sim.selection:
                return True

    def mouse_r(self, event):
        self.mouse = False

    def delete(self):
        self.sim.particles.remove(self)
        if self in self.sim.selection:
            self.sim.selection.remove(self)
        for p in self.linked:
            del p.link_lengths[self]
            p.linked.remove(self)
        self.sim.groups[self.group].remove(self)
        del self

    def select(self):
        if not self in self.sim.selection:
            self.sim.selection.append(self)

    def return_dict(self, index_source='all'):
        if index_source == 'all':
            index_source = self.sim.particles

        dictionary = self.__dict__.copy()
        del dictionary['sim']
        del dictionary['collisions']
        del dictionary['forces']

        dictionary['linked'] = [index_source.index(particle) for particle in dictionary['linked'] if
                                particle in index_source]
        dictionary['link_lengths'] = {index_source.index(particle): value
                                      for particle, value in dictionary['link_lengths'].items() if
                                      particle in index_source}

        return dictionary

    def applyForce(self, force):  # force in newtons (N)
        self.a = self.a + force / abs(self.m)  # acceleration = force/mass

    def calc_attraction_force(self, distance, direction, repel_r, attr, repel, rest_distance,
                              is_in_group, is_linked, link_attr_breaking_force, link_repel_breaking_force,
                              gravity, part):
        magnitude = 0
        attract = True
        if distance < repel_r:
            magnitude = -repel * rest_distance / 10
            attract = False
        elif is_in_group or is_linked:
            if gravity:
                magnitude = attr * self.m * part.m / distance**2 * 10 #newtons law of universal gravitation
            else:
                magnitude = attr * rest_distance / 3000

        if is_linked:
            max_force = link_attr_breaking_force if attract else link_repel_breaking_force
            if self.sim.stress_visualization:
                if max_force > 0:
                    percentage = round(abs(magnitude) / max_force, 2)
                else:
                    percentage = 1 if max_force == 0 else 0

                self.sim.link_colors.append([self, part, min(percentage, 1)])

            if 0 <= max_force <= abs(magnitude):
                self.sim.unlink([self, part])

        return direction * magnitude

    def update(self, grid):
        if not self.sim.paused:
            # Reset acceleration
            self.a = np.zeros(2)
            
            # Calculate gravitational force
            gravitational_force = self.m * self.sim.g_vector  # F = m * g
            self.applyForce(gravitational_force)  # Apply gravitational force
            
            # Apply wind force
            self.applyForce(self.sim.wind_force * self.r)

            for force in self.forces:
                self.applyForce(force)

            if self.y + self.r >= self.sim.height:  # Assuming the ground is at y = sim.height
                friction_force = self.sim.ground_friction * self.m * self.sim.g_vector
                self.applyForce(friction_force)
                print(friction_force)

            if self.sim.use_grid:
                near_particles = grid.return_particles(self)
            else:
                near_particles = self.sim.particles

            if not self.locked:
                for p in near_particles:
                    is_in_group = not self.separate_group and p in self.sim.groups[self.group]
                    is_linked = p in self.linked
                    if p == self or (not self.linked_group_particles and not is_linked and is_in_group) or \
                            p in self.collisions:
                        continue

                    # Attract / repel
                    repel_r = None
                    if is_linked and self.link_lengths[p] != 'repel':
                        repel_r = self.link_lengths[p]

                    direction = np.array([p.x, p.y]) - np.array([self.x, self.y])
                    distance = np.linalg.norm(direction)
                    if distance != 0:
                        direction = direction / distance
                    conditions = [
                        (p.attr != 0 or p.repel != 0) and (p.attr_r < 0 or p.attr_r < 0 or distance < p.attr_r),
                        (self.attr != 0 or self.repel != 0) and
                        (self.attr_r < 0 or self.attr_r < 0 or distance < self.attr_r)
                        ]
                    if conditions[0] or conditions[1]:
                        if distance == 0:
                            if self.gravity_mode or p.gravity_mode:
                                force = np.zeros(2)
                            else:
                                force = np.random.uniform(-10, 10, 2)
                                force = force / np.linalg.norm(force) * -self.repel
                        else:
                            if self.sim.calculate_radii_diff:
                                force = 0
                                inputs = []

                                for i, particle in enumerate([p, self]):
                                    if conditions[i]:
                                        repel_r_ = particle.repel_r if repel_r is None else repel_r

                                        rest_distance = abs(distance - repel_r_)
                                        new_inputs = [distance, direction, repel_r_, particle.attr, particle.repel,
                                                    rest_distance, is_in_group, is_linked,
                                                    particle.link_attr_breaking_force,
                                                    particle.link_repel_breaking_force,
                                                    particle.gravity_mode]

                                        if i == 1 and new_inputs == inputs:
                                            force *= 2
                                        else:
                                            force += self.calc_attraction_force(*new_inputs, particle)
                                            inputs = new_inputs.copy()
                            else:
                                repel_r_ = max(self.repel_r, p.repel_r) if repel_r is None else repel_r

                                force = self.calc_attraction_force(distance, direction, repel_r_, (p.attr + self.attr),
                                                                (p.repel + self.repel), abs(distance - repel_r_),
                                                                is_in_group, is_linked,
                                                                p.link_attr_breaking_force,
                                                                p.link_repel_breaking_force,
                                                                self.gravity_mode or p.gravity_mode, p)

                        self.applyForce(force)
                        p.forces.append(-force)
                        p.collisions.append(self)

                    if self.collision_bool and distance < self.r + p.r: #elastic collision 
                        temp = self.v[0]
                        self.v[0] = (self.m - p.m) / (self.m + p.m) * self.v[0] + 2 * p.m / (self.m + p.m) * p.v[0]
                        p.v[0] = 2 * self.m / (self.m + p.m) * temp + (p.m - self.m) / (self.m + p.m) * temp
                        temp = self.v[1]
                        self.v[1] = (self.m - p.m) / (self.m + p.m) * self.v[1] + 2 * p.m / (self.m + p.m) * p.v[1]
                        p.v[1] = 2 * self.m / (self.m + p.m) * temp + (p.m - self.m) / (self.m + p.m) * temp

                        # Visual overlap fix
                        translate_vector = -direction * (self.r + p.r) - -direction * distance
                        if not self.mouse:
                            self.x += translate_vector[0] * (self.m / (self.m + p.m))
                            self.y += translate_vector[1] * (self.m / (self.m + p.m))
                        if not p.mouse and not p.locked:
                            p.x -= translate_vector[0] * (p.m / (self.m + p.m))
                            p.y -= translate_vector[1] * (p.m / (self.m + p.m))

            # velocity handler
            if not self.mouse and not self.locked:
                self.v += np.clip(self.a, -2, 2) * self.sim.speed  # adding acceleration

                # Calculate velocity based on temperature using Boltzmann distribution
                scaling_factor = 1e11  # Adjust this factor as needed
                velocity_mag = np.sqrt((3 * Particle.boltzmann_constant * self.sim.temperature) / self.m) * scaling_factor

                # Generate random direction vectors for velocity
                velocity_dir = np.random.uniform(-1, 1, 2)
                velocity_norm = np.linalg.norm(velocity_dir)
            
                if velocity_norm != 0:
                    velocity_dir /= velocity_norm  # Normalize the direction
                # Scale direction vectors by magnitude of velocity
                thermal_velocity = velocity_dir * velocity_mag
            
                self.v += thermal_velocity  # Apply thermal velocity to particle velocity

                self.v += self.sim.air_res_calc * -self.v

                self.x += self.v[0] * self.sim.speed  # velocity + accel * sim speed
                self.y += self.v[1] * self.sim.speed  # velocity + accel * sim speed


        if self.mouse:
            self.x += self.sim.mx - self.sim.prev_mx
            self.y += self.sim.my - self.sim.prev_my
            if not self.sim.paused:
                self.v = np.array([self.sim.mx - self.sim.prev_mx, self.sim.my - self.sim.prev_my], dtype='float64') / \
                        self.sim.speed

        if self.sim.right and self.x + self.r >= self.sim.width:
            self.v[0] *= -self.bounciness
            self.v[1] *= 1 - self.sim.ground_friction
            self.x = self.sim.width - self.r
        if self.sim.left and self.x - self.r <= 0:
            self.v[0] *= -self.bounciness
            self.v[1] *= 1 - self.sim.ground_friction
            self.x = self.r
        if self.sim.bottom and self.y + self.r >= self.sim.height:
            self.v[1] *= -self.bounciness
            self.v[0] *= 1 - self.sim.ground_friction
            self.y = self.sim.height - self.r
        if self.sim.top and self.y - self.r <= 0:
            self.v[1] *= -self.bounciness
            self.v[0] *= 1 - self.sim.ground_friction
            self.y = self.r

        if self.sim.void_edges and (self.x - self.r >= self.sim.width or self.x + self.r <= 0 or
                                    self.y - self.r >= self.sim.height or self.y + self.r <= 0):
            self.delete()
            return

        self.collisions = []
        self.forces = []
