from particle_simulator import *

sim = Simulation(width=850, height=800, title="Simulation", gridres=(50, 50),
                 temperature=0, g=0, air_res=0.05, ground_friction=0)

# Random particle-positions
for i in range(50):
    s = 10
    Particle(sim, random.normalvariate(sim.width / 2, sim.width / 5),
             random.normalvariate(sim.height / 2, sim.height / 5), radius=s,
             color=np.random.randint(0, 255, 3).tolist(),
             mass=1, bounciness=0.7, velocity=np.zeros(2), collisions=False,
             attract_r=-1, repel_r=10, attraction_strength=0.25, repulsion_strength=1)

sim.simulate()



