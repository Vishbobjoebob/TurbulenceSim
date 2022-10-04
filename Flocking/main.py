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
from boid import Boid

default_boids = 100
geometry_size = 1000
grid_size=10
grid_length=int(geometry_size/grid_size)
default_geometry = str(geometry_size) + "x" + str(geometry_size)
frames = 1000

numLoops=1

def update(dt, boids):

    # Go through events that are passed to the script by the window.
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            mods = pg.key.get_mods()
            if event.key == pg.K_q:
                # quit
                pg.quit()
                sys.exit(0)
            elif event.key == pg.K_UP:
                # add boids
                if mods & pg.KMOD_SHIFT:
                    add_boids(boids, 100)
                else:
                    add_boids(boids, 10)
            elif event.key == pg.K_DOWN:
                # remove boids
                if mods & pg.KMOD_SHIFT:
                    boids.remove(boids.sprites()[:100])
                else:
                    boids.remove(boids.sprites()[:10])
            elif event.key == pg.K_1:
                for boid in boids:
                    boid.max_force /= 2
                print("max force {}".format(boids.sprites()[0].max_force))
            elif event.key == pg.K_2:
                for boid in boids:
                    boid.max_force *= 2
                print("max force {}".format(boids.sprites()[0].max_force))
            elif event.key == pg.K_3:
                for boid in boids:
                    boid.perception *= .8
                print("perception {}".format(boids.sprites()[0].perception))
            elif event.key == pg.K_4:
                for boid in boids:
                    boid.perception *= 1.2
                print("perception {}".format(boids.sprites()[0].perception))
            elif event.key == pg.K_5:
                for boid in boids:
                    boid.crowding *= 0.8
                print("crowding {}".format(boids.sprites()[0].crowding))
            elif event.key == pg.K_6:
                for boid in boids:
                    boid.crowding *= 1.2
                print("crowding {}".format(boids.sprites()[0].crowding))
            elif event.key == pg.K_d:
                # toggle debug
                for boid in boids:
                    boid.debug = not boid.debug
            elif event.key == pg.K_r:
                # reset
                num_boids = len(boids)
                boids.empty()
                add_boids(boids, num_boids)

    for b in boids:
        b.update(dt, boids)


def draw(screen, background, boids):
    """
    Draw things to the window. Called once per frame.
    """

    # Redraw screen here
    boids.clear(screen, background)
    dirty = boids.draw(screen)

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
    pg.display.set_caption("BOIDS!")
    window_width, window_height = [int(x) for x in args.geometry.split("x")]
    flags = DOUBLEBUF

    screen = pg.display.set_mode((window_width, window_height), flags)
    screen.set_alpha(None)
    background = pg.Surface(screen.get_size()).convert()
    background.fill(pg.Color('black'))

    boids = pg.sprite.RenderUpdates()

    add_boids(boids, args.num_boids)

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
        update(dt, boids)
        draw(screen, background, boids)
        dt = fpsClock.tick(fps)
        mean_dispersion.append(getMeanDispersionStatistics(boids))
        particle_diffusion.append(getParticleDiffusivity(boids))
        std_devs.append(getGridStatistics(boids))
        current_time = time.time() - start_time
        times.append(current_time)

    
    writeBoids(boids, loop)
    getGridStatistics(boids)
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


def add_boids(boids, num_boids):
    for _ in range(num_boids):
        boids.add(Boid())

def writeBoids(boids, loopNum):
        
    filePositions = open("C:\\Users\\pasam\\Documents\\CCL\\Flocking\\data\\positions\\loop" + str(loopNum) + ".dat", "w")
    fileVelocities = open("C:\\Users\\pasam\\Documents\\CCL\\Flocking\\data\\velocities\\loop" + str(loopNum) + ".dat", "w")

    for boid in boids:
        filePositions.write(str(boid.position))
        filePositions.write("\n")

        fileVelocities.write(str(boid.velocity))
        fileVelocities.write("\n")

    filePositions.close()
    fileVelocities.close()

def getGridStatistics(boids):
    grid = np.zeros((grid_size, grid_size), dtype=int)

    mean = default_boids/(grid_size * grid_size)
    
    for boid in boids:

        boid_grid_x = int(boid.position[0]/grid_length)
        boid_grid_y = int(boid.position[1]/grid_length) 

        if (boid_grid_x >= 10):
            boid_grid_x = 9
        if (boid_grid_y >= 10):
            boid_grid_y = 9
        grid[boid_grid_x][boid_grid_y] += 1

    std_dev = 0
    nums_cells=0
    for i in range(0, grid_size):
        for j in range(0, grid_size):

            std_dev += pow((grid[i][j] - mean), 2)
            nums_cells+=1

    # print()
    # print(grid)
    return std_dev




def getMeanDispersionStatistics(boids):
    
    sum_dispersion = 0

    for boid in boids:
        dispersion  = 2 * np.hypot(boid.position[0] - boid.start_position[0], boid.position[1] - boid.start_position[1]) * np.linalg.norm(boid.velocity)
        sum_dispersion += dispersion

    mean_dispersion = sum_dispersion / len(boids)
    
    return mean_dispersion/2

def getParticleDiffusivity(boids):
    
    sum_diffusivity = 0

    for boid in boids:
        diffusivity = pow(np.hypot(boid.velocity[0] - boid.start_velocity[0], boid.velocity[1] - boid.start_velocity[1]),2)
        sum_diffusivity += diffusivity

    mean_diffusivity= sum_diffusivity / len(boids)
    
    return mean_diffusivity

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Emergent flocking.')
    parser.add_argument('--geometry', metavar='WxH', type=str,
                        default=default_geometry, help='geometry of window')
    parser.add_argument('--number', dest='num_boids', default=default_boids,
                        help='number of boids to generate')
    args = parser.parse_args()

    # for loop
    loop=0
    for loop in range(numLoops):
        main(args, loop)
