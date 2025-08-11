import math 
import pygame 
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Small Body Gravity Clusters")
clock = pygame.time.Clock()
running = True
dt = 0
G = 5000  # Scaled gravitational constant

class CelestialBody: 
    def __init__(self, name, pos, mass, radius, velocity=None, color="white"):
        self.name = name
        self.pos = pygame.Vector2(pos)
        self.mass = mass
        self.radius = radius 
        self.velocity = velocity if velocity is not None else pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
        self.color = color
        self.trail = []
        self.max_trail = 80

    def calculate_gravitational_force(self, other_body): 
        directional_vector = other_body.pos - self.pos
        dist = directional_vector.length()

        # Prevent extreme forces
        min_dist = max(self.radius + other_body.radius, 5)
        if dist < min_dist:
            dist = min_dist
        
        force_magnitude = (G * self.mass * other_body.mass) / (dist ** 2)

        if dist > 0: 
            force_direction = directional_vector / dist
            force_vector = force_direction * force_magnitude
            accel_gravity = force_vector / self.mass
            self.acceleration += accel_gravity
    
    def reset_acceleration(self):
        self.acceleration = pygame.Vector2(0,0)

    def update_position(self, dt): 
        self.velocity += self.acceleration * dt 
        self.pos += self.velocity * dt

        # Add to trail
        self.trail.append(self.pos.copy())
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)

    def draw(self, screen): 
        # Draw trail
        if len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                alpha = i / len(self.trail)
                trail_radius = max(1, int(self.radius * alpha * 0.3))
                
                # Fade the color
                color = pygame.Color(self.color)
                faded_color = (int(color.r * alpha * 0.6), 
                              int(color.g * alpha * 0.6), 
                              int(color.b * alpha * 0.6))
                pygame.draw.circle(screen, faded_color, self.trail[i], trail_radius)
        
        # Draw main body
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        
        # Draw name if radius is large enough
        if self.radius > 8:
            font = pygame.font.Font(None, 16)
            text = font.render(self.name, True, self.color)
            text_rect = text.get_rect(center=(self.pos.x, self.pos.y + self.radius + 12))
            screen.blit(text, text_rect)

def create_asteroid_cluster():
    """Create a cluster of main belt asteroids"""
    center = pygame.Vector2(640, 360)
    bodies = []
    
    # Ceres - largest, at center
    bodies.append(CelestialBody("Ceres", center, 8000, 20, pygame.Vector2(0, 0), "lightblue"))
    
    # Other asteroids in orbit around the cluster center
    asteroids = [
        ("Vesta", 3500, 12, "orange"),
        ("Pallas", 3200, 11, "gray"),
        ("Hygiea", 2800, 10, "darkgray"),
        ("Interamnia", 2200, 8, "brown"),
        ("Davida", 1800, 7, "tan"),
        ("Sylvia", 1600, 6, "lightgray"),
        ("Cybele", 1400, 6, "darkblue")
    ]
    
    for i, (name, mass, radius, color) in enumerate(asteroids):
        angle = (i / len(asteroids)) * 2 * math.pi
        distance = 120 + random.randint(-30, 50)
        
        pos = center + pygame.Vector2(
            math.cos(angle) * distance,
            math.sin(angle) * distance
        )
        
        # Orbital velocity perpendicular to radius
        orbital_speed = math.sqrt(G * 8000 / distance) * 0.8  # Slightly elliptical
        velocity = pygame.Vector2(-math.sin(angle), math.cos(angle)) * orbital_speed
        velocity += pygame.Vector2(random.randint(-20, 20), random.randint(-20, 20))  # Add some chaos
        
        bodies.append(CelestialBody(name, pos, mass, radius, velocity, color))
    
    return bodies

def create_kuiper_belt_cluster():
    """Create a cluster of Kuiper Belt Objects"""
    bodies = []
    center = pygame.Vector2(640, 360)
    
    # Pluto-Charon system at center
    pluto_pos = center + pygame.Vector2(-15, 0)
    charon_pos = center + pygame.Vector2(15, 0)
    
    bodies.append(CelestialBody("Pluto", pluto_pos, 6000, 15, pygame.Vector2(0, -30), "brown"))
    bodies.append(CelestialBody("Charon", charon_pos, 2000, 8, pygame.Vector2(0, 90), "gray"))
    
    # Other KBOs
    kbos = [
        ("Eris", 5800, 14, "white"),
        ("Makemake", 3500, 11, "red"),
        ("Haumea", 4200, 12, "yellow"),
        ("Orcus", 2800, 9, "purple"),
        ("Quaoar", 3200, 10, "lightblue"),
        ("Sedna", 2600, 8, "orange")
    ]
    
    for i, (name, mass, radius, color) in enumerate(kbos):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.randint(150, 280)
        
        pos = center + pygame.Vector2(
            math.cos(angle) * distance,
            math.sin(angle) * distance
        )
        
        # Random orbital velocity
        speed = random.randint(40, 80)
        velocity = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ).normalize() * speed
        
        bodies.append(CelestialBody(name, pos, mass, radius, velocity, color))
    
    return bodies

def create_jovian_moon_system():
    """Create Jupiter's major moons system"""
    bodies = []
    jupiter_pos = pygame.Vector2(640, 360)
    
    # Jupiter at center
    bodies.append(CelestialBody("Jupiter", jupiter_pos, 20000, 35, pygame.Vector2(0, 0), "orange"))
    
    # Galilean moons
    moons = [
        ("Io", 80, 2500, 8, "yellow"),
        ("Europa", 110, 2200, 7, "lightblue"),
        ("Ganymede", 150, 4000, 12, "brown"),
        ("Callisto", 200, 3500, 10, "darkgray")
    ]
    
    for name, distance, mass, radius, color in moons:
        angle = random.uniform(0, 2 * math.pi)
        pos = jupiter_pos + pygame.Vector2(
            math.cos(angle) * distance,
            math.sin(angle) * distance
        )
        
        # Circular orbital velocity
        orbital_speed = math.sqrt(G * 20000 / distance)
        velocity = pygame.Vector2(-math.sin(angle), math.cos(angle)) * orbital_speed
        
        bodies.append(CelestialBody(name, pos, mass, radius, velocity, color))
    
    return bodies

def create_random_small_bodies():
    """Create a random cluster of small bodies"""
    bodies = []
    
    for i in range(12):
        pos = pygame.Vector2(
            random.randint(100, 1180),
            random.randint(100, 620)
        )
        
        mass = random.randint(800, 3000)
        radius = max(4, mass // 200)
        
        velocity = pygame.Vector2(
            random.randint(-60, 60),
            random.randint(-60, 60)
        )
        
        colors = ["white", "gray", "brown", "orange", "yellow", "lightblue", "red", "purple"]
        color = random.choice(colors)
        
        bodies.append(CelestialBody(f"Body{i+1}", pos, mass, radius, velocity, color))
    
    return bodies

# Start with asteroid cluster
current_simulation = 0
simulations = [
    ("Asteroid Belt Cluster", create_asteroid_cluster),
    ("Kuiper Belt Objects", create_kuiper_belt_cluster),
    ("Jovian Moon System", create_jovian_moon_system),
    ("Random Small Bodies", create_random_small_bodies)
]

bodies = simulations[current_simulation][1]()
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                bodies = simulations[current_simulation][1]()
            elif event.key == pygame.K_n:  # Next simulation
                current_simulation = (current_simulation + 1) % len(simulations)
                bodies = simulations[current_simulation][1]()
            elif event.key == pygame.K_p:  # Previous simulation
                current_simulation = (current_simulation - 1) % len(simulations)
                bodies = simulations[current_simulation][1]()
    
    screen.fill("black")
    
    if not paused:
        # Physics calculations
        for body in bodies:
            body.reset_acceleration()
        
        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                bodies[i].calculate_gravitational_force(bodies[j])
                bodies[j].calculate_gravitational_force(bodies[i])
        
        for body in bodies:
            body.update_position(dt)
    
    # Draw everything
    for body in bodies:
        body.draw(screen)
    
    # Draw UI
    font = pygame.font.Font(None, 24)
    title = simulations[current_simulation][0]
    title_text = font.render(title, True, "yellow")
    screen.blit(title_text, (10, 10))
    
    instructions = [
        "SPACE - Pause/Resume",
        "R - Reset current simulation",
        "N - Next simulation",
        "P - Previous simulation",
        f"Bodies: {len(bodies)}",
        f"Status: {'PAUSED' if paused else 'RUNNING'}"
    ]
    
    small_font = pygame.font.Font(None, 20)
    for i, instruction in enumerate(instructions):
        color = "yellow" if "PAUSED" in instruction else "white"
        text = small_font.render(instruction, True, color)
        screen.blit(text, (10, 40 + i * 20))
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000 if not paused else 0

pygame.quit()