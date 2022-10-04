import pygame as pg
from random import uniform
from vehicle import Vehicle
import argparse
import numpy as np
from numpy import loadtxt

gas_grid_size = 101

arr = np.loadtxt(r"C:\Users\pasam\Documents\CCL\Turbulence Research\Drag\VelocityData100.csv")

gas_particle_velocity_field = arr.reshape(gas_grid_size, gas_grid_size, 3)

class Particle(Vehicle):

    # CONFIG
    debug = False
    min_speed = .01
    max_speed = .2
    max_force = 1
    max_turn = 5
    perception = 60
    crowding = 15
    can_wrap = True
    edge_distance_pct = 5
    timescale = 100
    ###############

    def __init__(self, start_position, start_velocity):
        Particle.set_boundary(Particle.edge_distance_pct)

        self.max_x = Particle.max_x
        self.max_y = Particle.max_y

        #starting position and velocity
        self.start_position = start_position
        self.start_velocity = start_velocity
        
        super().__init__(start_position, start_velocity,
                         Particle.min_speed, Particle.max_speed,
                         Particle.max_force, Particle.can_wrap)

        self.rect = self.image.get_rect(center=self.position)

        self.debug = Particle.debug

    def drag(self):

        gas_particle_velocity = gas_particle_velocity_field[int(self.position[0]/10.1)][int(self.position[1]/10.1)]
        gas_particle_velocity_vector = pg.Vector2(gas_particle_velocity[0], gas_particle_velocity[1])
        steering = (self.velocity - gas_particle_velocity_vector)/self.timescale
        return steering

    def update(self, dt):
        steering = pg.Vector2()

        if not self.can_wrap:
            steering += self.avoid_edge()

        drag = self.drag()

            # DEBUG
            # separation *= 0
            # alignment *= 0
            # cohesion *= 0

        steering += drag

        # steering = self.clamp_force(steering)
        print(self.position)
        super().update(dt, steering)

            