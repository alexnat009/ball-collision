import numpy as np
import random

# Constants
WIDTH, HEIGHT = 640, 480
BALL_RADIUS = 15
GRAVITY = 0.5
DAMPING = 0.9
FRICTION = 0.98
COEFFICIENT_OF_RESTITUTION = 0.8


class BallSystem:
	def __init__(self, num_fixed_balls):
		"""Initialize the ball system with a given number of fixed balls."""
		self.positions = np.zeros((0, 2))
		self.velocities = np.zeros((0, 2))
		self.fixed = np.array([], dtype=bool)

		# Generate fixed balls in the upper half of the screen
		fixed_positions = np.array([
			[random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS),
			 random.randint(BALL_RADIUS, HEIGHT // 2)]
			for _ in range(num_fixed_balls)
		])
		fixed_velocities = np.zeros((num_fixed_balls, 2))
		fixed_states = np.ones(num_fixed_balls, dtype=bool)

		self.add_balls(fixed_positions, fixed_velocities, fixed_states)

	def add_balls(self, positions, velocities, fixed):
		"""Adds new balls to the system."""
		self.positions = np.vstack((self.positions, positions))
		self.velocities = np.vstack((self.velocities, velocities))
		self.fixed = np.concatenate((self.fixed, fixed))

	def move_balls(self):
		"""Applies physics: gravity, friction, and boundary collisions."""
		self.velocities[~self.fixed, 1] += GRAVITY
		self.velocities[~self.fixed] *= FRICTION
		self.positions[~self.fixed] += self.velocities[~self.fixed]

		# Collision with walls
		mask_left = self.positions[:, 0] - BALL_RADIUS < 0
		self.positions[mask_left, 0] = BALL_RADIUS
		self.velocities[mask_left, 0] *= -DAMPING

		mask_right = self.positions[:, 0] + BALL_RADIUS > WIDTH
		self.positions[mask_right, 0] = WIDTH - BALL_RADIUS
		self.velocities[mask_right, 0] *= -DAMPING

		mask_top = self.positions[:, 1] - BALL_RADIUS < 0
		self.positions[mask_top, 1] = BALL_RADIUS
		self.velocities[mask_top, 1] *= -DAMPING

		mask_bottom = self.positions[:, 1] + BALL_RADIUS > HEIGHT
		self.positions[mask_bottom, 1] = HEIGHT - BALL_RADIUS
		self.velocities[mask_bottom, 1] *= -DAMPING

	def resolve_collisions(self):
		"""Detects and resolves ball collisions."""
		diffs = self.positions[:, np.newaxis, :] - self.positions[np.newaxis, :, :]
		distances = np.linalg.norm(diffs, axis=-1)
		collision_mask = (distances < 2 * BALL_RADIUS) & (distances > 0)

		for i in range(self.positions.shape[0]):
			colliders = np.where(collision_mask[i])[0]
			for j in colliders:
				if self.fixed[i] and self.fixed[j]:
					continue  # Skip fixed balls

				dx, dy = diffs[i, j]
				distance = distances[i, j]
				nx, ny = dx / distance, dy / distance

				rel_vx, rel_vy = self.velocities[i] - self.velocities[j]
				rel_dot = rel_vx * nx + rel_vy * ny

				if rel_dot > 0:
					continue  # Ignore separating balls

				impulse = (2 * rel_dot) / (1 + (0 if self.fixed[j] else 1))
				impulse *= COEFFICIENT_OF_RESTITUTION

				if not self.fixed[i]:
					self.velocities[i] -= impulse * np.array([nx, ny])
				if not self.fixed[j]:
					self.velocities[j] += impulse * np.array([nx, ny])

				overlap = 2 * BALL_RADIUS - distance
				if not self.fixed[i]:
					self.positions[i] += 0.5 * overlap * np.array([nx, ny])
				if not self.fixed[j]:
					self.positions[j] -= 0.5 * overlap * np.array([nx, ny])
