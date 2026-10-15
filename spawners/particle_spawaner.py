import config
import random

from utilities.particle import Particle


def spawnParticle(game, entity, particlesList):
    rect = entity.get_rect()
    if entity.flip:
        pos = (
            rect.right,
            rect.centery
            + random.randint(
                -config.PARTICLE_OFFSET_Y,
                config.PARTICLE_OFFSET_Y,
            ),
        )
        speed = [
            random.uniform(
                config.PARTICLE_SPEED_MIN,
                config.PARTICLE_SPEED_MAX,
            ),
            random.uniform(
                -config.PARTICLE_VERTICAL_SPEED,
                config.PARTICLE_VERTICAL_SPEED,
            ),
        ]
    else:
        pos = (
            rect.left,
            rect.centery
            + random.randint(
                -config.PARTICLE_OFFSET_Y,
                config.PARTICLE_OFFSET_Y,
            ),
        )
        speed = [
            -random.uniform(
                config.PARTICLE_SPEED_MIN,
                config.PARTICLE_SPEED_MAX,
            ),
            random.uniform(
                -config.PARTICLE_VERTICAL_SPEED,
                config.PARTICLE_VERTICAL_SPEED,
            ),
        ]

    particlesList.append(
        Particle(
            game,
            config.PARTICLE_COLOR,
            random.randint(
                config.PARTICLE_MIN_SIZE,
                config.PARTICLE_MAX_SIZE,
            ),
            pos,
            speed,
        )
    )
