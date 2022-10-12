from turtle import heading
import pygame as pg


class Vehicle(pg.sprite.Sprite):
    # default image is a li'l white triangle
    image = pg.Surface((10, 10), pg.SRCALPHA)
    pg.draw.polygon(image, pg.Color('white'),
                    [(15, 5), (0, 2), (0, 8)])

    def __init__(self, position, velocity, min_speed, max_speed,
                 max_force, can_wrap):

        super().__init__()

        # set limits
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.max_force = max_force

        # set position
        dimensions = len(position)
        assert (1 < dimensions < 4), "Invalid spawn position dimensions"

        if dimensions == 2:
            self.position = pg.Vector2(position)
            self.acceleration = pg.Vector2(0, 0)
            self.velocity = pg.Vector2(velocity)
        else:
            self.position = pg.Vector3(position)
            self.acceleration = pg.Vector3(0, 0, 0)
            self.velocity = pg.Vector3(velocity)

        self.inclination = 0.0
        self.heading = 0.0

        self.position2D = [self.position[0], self.position[1]]

        self.rect = self.image.get_rect(center=self.position2D)

    def update(self, dt, steering):
        self.acceleration = steering * dt

        # enforce turn limit
        new_velocity = self.velocity + self.acceleration * dt
        speed, inclination, heading = new_velocity.as_spherical()

        self.velocity.from_spherical((speed, inclination, heading))

        # enforce speed limit
        speed, self.inclination, self.heading = self.velocity.as_spherical()
        # if speed < self.min_speed:
        #     self.velocity.scale_to_length(self.min_speed)

        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # move
        self.position += self.velocity * dt

        if self.can_wrap:
            self.wrap()

        # draw
        self.image = pg.transform.rotate(Vehicle.image, -self.heading)

        if self.debug:
            center = pg.Vector2((50, 50))

            velocity = pg.Vector2(self.velocity[0],self.velocity[1])
            speed = velocity.length()
            velocity += center

            acceleration = pg.Vector2(self.acceleration[0],self.acceleration[1])
            acceleration += center

            steering = pg.Vector2(steering)
            steering += center

            overlay = pg.Surface((100, 100), pg.SRCALPHA)
            overlay.blit(self.image, center - (10, 10))

            pg.draw.line(overlay, pg.Color('green'), center, velocity, 3)
            pg.draw.line(overlay, pg.Color('red'), center + (5, 0),
                         acceleration + (5, 0), 3)
            pg.draw.line(overlay, pg.Color('blue'), center - (5, 0),
                         steering - (5, 0), 3)

            self.image = overlay
            self.rect = overlay.get_rect(center=[self.position[0],self.position[1]])
        else:
            self.rect = self.image.get_rect(center=[self.position[0],self.position[1]])

    def avoid_edge(self):
        left = self.edges[0] - self.position.x
        up = self.edges[1] - self.position.y
        right = self.position.x - self.edges[2]
        down = self.position.y - self.edges[3]

        scale = max(left, up, right, down)

        if scale > 0:
            center = (Vehicle.max_x / 2, Vehicle.max_y / 2)
            steering = pg.Vector2(center)
            steering -= self.position
        else:
            steering = pg.Vector2()

        return steering

    def wrap(self):
        if self.position.x < 0:
            self.position.x += Vehicle.max_x
        elif self.position.x > Vehicle.max_x:
            self.position.x -= Vehicle.max_x

        if self.position.y < 0:
            self.position.y += Vehicle.max_y
        elif self.position.y > Vehicle.max_y:
            self.position.y -= Vehicle.max_y
        
        if self.position.z < 0:
            self.position.z += Vehicle.max_z
        elif self.position.z > Vehicle.max_z:
            self.position.z -= Vehicle.max_z

    @staticmethod
    def set_boundary(edge_distance_pct):
        info = pg.display.Info()
        Vehicle.max_x = info.current_w
        Vehicle.max_y = info.current_h
        Vehicle.max_z = info.current_h
        margin_w = Vehicle.max_x * edge_distance_pct / 100
        margin_h = Vehicle.max_y * edge_distance_pct / 100
        Vehicle.edges = [margin_w, margin_h, Vehicle.max_x - margin_w,
                         Vehicle.max_y - margin_h]

    def clamp_force(self, force):
        # if 0 < force.magnitude() > self.max_force:
        #     force.scale_to_length(self.max_force)

        return force
