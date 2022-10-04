# Import standard modules.
import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
# Import non-standard modules.
import pygame as pg
from pygame.locals import *

# Import local modules
from particle import Particle

geometry_size = 1000
grid_size=10
grid_length=int(geometry_size/grid_size)
default_geometry = str(geometry_size) + "x" + str(geometry_size)
frames = 1000

numLoops=1

def update(dt, particles):

    # Go through events that are passed to the script by the window.
    # for event in pg.event.get():
    #     if event.type == QUIT:
    #         pg.quit()
    #         sys.exit(0)
    #     elif event.type == KEYDOWN:
    #         mods = pg.key.get_mods()
    #         if event.key == pg.K_q:
    #             # quit
    #             pg.quit()
    #             sys.exit(0)
    #         elif event.key == pg.K_UP:
    #             # add particles
    #             if mods & pg.KMOD_SHIFT:
    #                 add_particles(particles, 100)
    #             else:
    #                 add_particles(particles, 10)
    #         elif event.key == pg.K_DOWN:
    #             # remove particles
    #             if mods & pg.KMOD_SHIFT:
    #                 particles.remove(particles.sprites()[:100])
    #             else:
    #                 particles.remove(particles.sprites()[:10])
    #         elif event.key == pg.K_1:
    #             for particle in particles:
    #                 particle.max_force /= 2
    #             print("max force {}".format(particles.sprites()[0].max_force))
    #         elif event.key == pg.K_2:
    #             for particle in particles:
    #                 particle.max_force *= 2
    #             print("max force {}".format(particles.sprites()[0].max_force))
    #         elif event.key == pg.K_3:
    #             for particle in particles:
    #                 particle.perception *= .8
    #             print("perception {}".format(particles.sprites()[0].perception))
    #         elif event.key == pg.K_4:
    #             for particle in particles:
    #                 particle.perception *= 1.2
    #             print("perception {}".format(particles.sprites()[0].perception))
    #         elif event.key == pg.K_5:
    #             for particle in particles:
    #                 particle.crowding *= 0.8
    #             print("crowding {}".format(particles.sprites()[0].crowding))
    #         elif event.key == pg.K_6:
    #             for particle in particles:
    #                 particle.crowding *= 1.2
    #             print("crowding {}".format(particles.sprites()[0].crowding))
    #         elif event.key == pg.K_d:
    #             # toggle debug
    #             for particle in particles:
    #                 particle.debug = not particle.debug
    #         elif event.key == pg.K_r:
    #             # reset
    #             num_particles = len(particles)
    #             particles.empty()
    #             add_particles(particles, num_particles)

    for b in particles:
        b.update(dt)


def draw(screen, background, particles):
    """
    Draw things to the window. Called once per frame.
    """

    # Redraw screen here
    particles.clear(screen, background)
    dirty = particles.draw(screen)

    # Flip the display so that the things we drew actually show up.
    pg.display.update(dirty)


def main(args, loop):
    # Initialise pg.
    pg.init()

    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

    # Set up the clock to maintain a relatively constant framerate.
    fps = 60.0
    fpsClock = pg.time.Clock()

    # Set up the window.
    pg.display.set_caption("Particles!")
    window_width, window_height = [int(x) for x in args.geometry.split("x")]
    flags = DOUBLEBUF

    screen = pg.display.set_mode((window_width, window_height), flags)
    screen.set_alpha(None)
    background = pg.Surface(screen.get_size()).convert()
    background.fill(pg.Color('black'))

    particles = pg.sprite.RenderUpdates()

    add_particles(particles)

    # Main game loop.
    dt = 1/fps  # dt is the time since last frame.

    # Loop forever!
    i=0

    mean_dispersion = []
    particle_diffusion = []
    std_devs = []
    times = []
    start_time = time.time()
    for i in range(frames):
        update(dt, particles)
        draw(screen, background, particles)
        dt = fpsClock.tick(fps)
        mean_dispersion.append(getMeanDispersionStatistics(particles))
        particle_diffusion.append(getParticleDiffusivity(particles))
        # std_devs.append(getGridStatistics(particles))
        current_time = time.time() - start_time
        times.append(current_time)

    
    writeParticles(particles, loop)
    # getGridStatistics(particles)
    plt.figure(1)
    plt.plot(times, particle_diffusion)

    plt.figure(2)
    plt.xlabel("Time")
    plt.ylabel("Mean Squared Dispersion")
    plt.plot(times, mean_dispersion)

    plt.figure(3)
    plt.xlabel("Time")
    plt.ylabel("Standard Deviation")
    plt.plot(times, std_devs)

    plt.show()


def add_particles(particles):
    field_pos_x = grid_length
    while field_pos_x <= pg.display.Info().current_w:
        field_pos_y = grid_length
        while field_pos_y <= pg.display.Info().current_h:
            particles.add(Particle(
                pg.math.Vector2(
                field_pos_x,field_pos_y),
                pg.math.Vector2(
                10, 0)))
            field_pos_y += grid_length
        field_pos_x += grid_length
    args.num_particles = len(particles)

def writeParticles(particles, loopNum):
        
    filePositions = open("C:\\Users\\pasam\\Documents\\CCL\\Flocking\\data\\positions\\loop" + str(loopNum) + ".dat", "w")
    fileVelocities = open("C:\\Users\\pasam\\Documents\\CCL\\Flocking\\data\\velocities\\loop" + str(loopNum) + ".dat", "w")

    for particle in particles:
        filePositions.write(str(particle.position))
        filePositions.write("\n")

        fileVelocities.write(str(particle.velocity))
        fileVelocities.write("\n")

    filePositions.close()
    fileVelocities.close()

def getGridStatistics(particles):
    grid = np.zeros((grid_size, grid_size), dtype=int)

    mean = args.num_particles/(grid_size * grid_size)
    
    for particle in particles:

        particle_grid_x = int(particle.position[0]/grid_length)
        particle_grid_y = int(particle.position[1]/grid_length) 

        if (particle_grid_x >= 10):
            particle_grid_x = 9
        if (particle_grid_y >= 10):
            particle_grid_y = 9
        grid[particle_grid_x][particle_grid_y] += 1

    std_dev = 0
    nums_cells=0
    for i in range(0, grid_size):
        for j in range(0, grid_size):

            std_dev += pow((grid[i][j] - mean), 2)
            nums_cells+=1

    # print()
    # print(grid)
    return std_dev




def getMeanDispersionStatistics(particles):
    
    sum_dispersion = 0

    for particle in particles:
        dispersion  = 2 * np.hypot(particle.position[0] - particle.start_position[0], particle.position[1] - particle.start_position[1]) * np.linalg.norm(particle.velocity)
        sum_dispersion += dispersion

    mean_dispersion = sum_dispersion / len(particles)
    
    return mean_dispersion/2

def getParticleDiffusivity(particles):
    
    sum_diffusivity = 0

    for particle in particles:
        diffusivity = pow(np.hypot(particle.velocity[0] - particle.start_velocity[0], particle.velocity[1] - particle.start_velocity[1]),2)
        sum_diffusivity += diffusivity

    mean_diffusivity= sum_diffusivity / len(particles)
    
    return mean_diffusivity

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Emergent flocking.')
    parser.add_argument('--geometry', metavar='WxH', type=str,
                        default=default_geometry, help='geometry of window')
    parser.add_argument('--number', dest='num_particles', default=0,
                        help='number of particles to generate')
    args = parser.parse_args()

    # for loop
    loop=0
    for loop in range(numLoops):
        main(args, loop)
