---
title: Robot Simulation with Gazebo and Unity
sidebar_position: 1
description: Physics simulation and environment building
---

# Week 6: Gazebo Simulation Concepts

## Introduction

Gazebo serves as a critical simulation environment for developing and testing humanoid robots in a safe, controlled, and cost-effective manner. This week explores the fundamental concepts of physics simulation, environment modeling, and sensor simulation that enable effective robot development before real-world deployment. Gazebo's realistic physics engine and comprehensive sensor models make it an invaluable tool for Sim2Real transfer, where skills learned in simulation can be applied to real robots.

## Physics Simulation Fundamentals

Gazebo's physics engine forms the foundation for realistic robot simulation, modeling the complex interactions between robots, objects, and environments that occur in the physical world.

### Physics Engine Architecture

Gazebo supports multiple physics engines, with each offering different trade-offs between accuracy and performance:

- **ODE (Open Dynamics Engine)**: Fast, stable for most robotics applications
- **Bullet**: More accurate collision detection and response
- **DART**: Advanced kinematic and dynamic modeling capabilities
- **Simbody**: High-fidelity multibody dynamics

```
Pseudocode: Physics Simulation Core
class PhysicsEngine:
    def __init__(self, engine_type='ode'):
        self.engine = self.initialize_engine(engine_type)
        self.world = World()
        self.contact_manager = ContactManager()
        self.integrator = Integrator(method='runge_kutta')

    def simulate_step(self, dt):
        # Update collision detection
        collisions = self.contact_manager.detect_collisions(self.world)

        # Apply contact forces
        for collision in collisions:
            force = self.compute_contact_force(collision)
            collision.body1.apply_force(force)
            collision.body2.apply_force(-force)

        # Update body states (position, velocity, acceleration)
        for body in self.world.bodies:
            # Apply gravity
            body.apply_force(body.mass * self.gravity)

            # Apply user-defined forces
            for force in body.external_forces:
                body.apply_force(force)

            # Integrate equations of motion
            body.integrate(self.integrator, dt)

        # Update world state
        self.world.update(dt)

    def compute_contact_force(self, collision):
        # Compute normal and friction forces based on collision properties
        penetration_depth = collision.penetration_depth
        normal = collision.normal
        relative_velocity = collision.body1.velocity - collision.body2.velocity

        # Normal force (repulsive)
        normal_force_magnitude = self.springs_constant * penetration_depth
        normal_force = normal * normal_force_magnitude

        # Friction force (opposes relative motion)
        tangent_velocity = relative_velocity - (relative_velocity.dot(normal)) * normal
        friction_force = -tangent_velocity.normalize() * min(
            self.friction_coefficient * normal_force_magnitude,
            tangent_velocity.length()
        )

        return normal_force + friction_force
```

### Gravity and Environmental Forces

Realistic simulation of environmental forces is crucial for humanoid robot development:

```
Pseudocode: Environmental Force Simulation
class EnvironmentalForces:
    def __init__(self):
        self.gravity = Vector3(0, 0, -9.81)  # Earth's gravity
        self.wind = Vector3(0, 0, 0)  # Default no wind
        self.magnetic_field = Vector3(0.25, 0, 0.45)  # Approximate magnetic field

    def apply_gravity(self, body):
        # Apply gravitational force to each body
        gravity_force = body.mass * self.gravity
        body.apply_force(gravity_force, body.center_of_mass)

    def apply_wind_force(self, body, wind_speed, drag_coefficient):
        # Compute wind resistance based on body's relative velocity
        relative_velocity = body.velocity - self.wind
        wind_force_magnitude = 0.5 * self.air_density * drag_coefficient * body.frontal_area * (
            relative_velocity.length() ** 2
        )
        wind_force = -relative_velocity.normalize() * wind_force_magnitude
        body.apply_force(wind_force, body.center_of_mass)

    def simulate_atmospheric_effects(self, altitude):
        # Adjust air density based on altitude
        self.air_density = self.sea_level_density * math.exp(-altitude / 8500)  # Scale height approximation
```

### Collision Detection and Response

Accurate collision detection and response are essential for realistic humanoid robot simulation:

- **Broad Phase**: Fast culling of non-colliding pairs using bounding volumes
- **Narrow Phase**: Precise collision detection between potentially colliding objects
- **Contact Resolution**: Computing appropriate forces to prevent penetration

```
Pseudocode: Collision Detection System
class CollisionDetector:
    def __init__(self):
        self.broad_phase = BoundingVolumeHierarchy()
        self.narrow_phase = GJKAlgorithm()  # Gilbert-Johnson-Keerthi
        self.contact_resolver = SequentialImpulses()

    def detect_collisions(self, bodies):
        # Broad phase: identify potential collisions
        potential_pairs = self.broad_phase.find_collisions(bodies)

        actual_collisions = []
        for body1, body2 in potential_pairs:
            # Narrow phase: precise collision detection
            collision_info = self.narrow_phase.check_collision(body1, body2)

            if collision_info.collides:
                # Compute contact points and normals
                contact_points = self.compute_contact_points(collision_info)
                for point in contact_points:
                    collision = Collision(
                        body1=body1,
                        body2=body2,
                        contact_point=point.position,
                        normal=point.normal,
                        penetration_depth=point.penetration
                    )
                    actual_collisions.append(collision)

        return actual_collisions

    def compute_contact_points(self, collision_info):
        # Compute multiple contact points for stable contact
        contact_points = []
        for i in range(collision_info.num_contact_points):
            point = ContactPoint()
            point.position = collision_info.contact_positions[i]
            point.normal = collision_info.contact_normals[i]
            point.penetration = collision_info.penetrations[i]
            contact_points.append(point)
        return contact_points
```

## Environment Building and World Modeling

Creating realistic simulation environments is crucial for effective humanoid robot training and testing. The environment must accurately represent the physical space where the robot will operate.

### World Description Format (SDF)

SDF (Simulation Description Format) provides a standardized way to describe simulation environments:

```xml
<!-- example_world.sdf -->
<sdf version="1.7">
  <world name="humanoid_world">
    <!-- Physics engine configuration -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- Ground plane -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.7 0.7 0.7 1</ambient>
            <diffuse>0.7 0.7 0.7 1</diffuse>
          </material>
        </visual>
      </link>
    </model>

    <!-- Obstacles and furniture -->
    <model name="table">
      <pose>2 0 0 0 0 0</pose>
      <link name="table_top">
        <collision name="collision">
          <geometry>
            <box>
              <size>1.0 0.8 0.02</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1.0 0.8 0.02</size>
            </box>
          </geometry>
        </visual>
      </link>
      <link name="leg1">
        <pose>0.4 0.35 0.35 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <cylinder>
              <radius>0.02</radius>
              <length>0.7</length>
            </cylinder>
          </geometry>
        </collision>
      </link>
    </model>
  </world>
</sdf>
```

### Terrain and Surface Modeling

Realistic terrain modeling is essential for humanoid locomotion training:

```
Pseudocode: Terrain Generation
class TerrainGenerator:
    def __init__(self):
        self.height_map = HeightMap()
        self.material_properties = {}

    def generate_realistic_terrain(self, size_x, size_y, resolution):
        # Generate height map using Perlin noise for natural terrain
        height_data = self.generate_perlin_noise(size_x, size_y, resolution)

        # Add specific terrain features
        height_data = self.add_hills(height_data, num_hills=5)
        height_data = self.add_obstacles(height_data, obstacle_positions)
        height_data = self.add_ramps(height_data, ramp_positions)

        # Create collision and visual meshes
        collision_mesh = self.create_collision_mesh(height_data)
        visual_mesh = self.create_visual_mesh(height_data)

        return collision_mesh, visual_mesh

    def generate_perlin_noise(self, width, height, scale):
        # Generate Perlin noise for natural terrain variation
        noise_map = []
        for y in range(height):
            row = []
            for x in range(width):
                # Scale coordinates for noise function
                nx = x / width * scale
                ny = y / height * scale
                height_value = self.perlin_noise(nx, ny)
                row.append(height_value)
            noise_map.append(row)
        return noise_map

    def add_hills(self, height_data, num_hills):
        # Add random hills to terrain
        for _ in range(num_hills):
            hill_center_x = random.randint(0, len(height_data[0]) - 1)
            hill_center_y = random.randint(0, len(height_data) - 1)
            hill_radius = random.randint(5, 15)
            hill_height = random.uniform(0.1, 0.5)

            for y in range(len(height_data)):
                for x in range(len(height_data[0])):
                    distance = math.sqrt((x - hill_center_x)**2 + (y - hill_center_y)**2)
                    if distance <= hill_radius:
                        height_contribution = hill_height * (1 - distance / hill_radius)
                        height_data[y][x] += height_contribution

        return height_data

    def assign_surface_properties(self, terrain_mesh):
        # Assign different friction and restitution properties to terrain regions
        surface_properties = {}

        # Walkable surfaces (grass, concrete, etc.)
        surface_properties['grass'] = {
            'friction': 0.7,
            'restitution': 0.1,
            'texture': 'grass_texture.png'
        }

        # Slippery surfaces (ice, wet surfaces)
        surface_properties['ice'] = {
            'friction': 0.1,
            'restitution': 0.8,
            'texture': 'ice_texture.png'
        }

        return surface_properties
```

### Dynamic Environment Elements

Simulating dynamic environments with moving objects and changing conditions:

```
Pseudocode: Dynamic Environment System
class DynamicEnvironment:
    def __init__(self):
        self.moving_objects = []
        self.environment_states = {}
        self.event_scheduler = EventScheduler()

    def add_moving_object(self, object_model, trajectory):
        moving_obj = MovingObject()
        moving_obj.model = object_model
        moving_obj.trajectory = trajectory
        moving_obj.current_time = 0.0
        self.moving_objects.append(moving_obj)

    def update_dynamic_elements(self, sim_time):
        for obj in self.moving_objects:
            # Update position based on trajectory
            new_pose = obj.trajectory.interpolate(sim_time)
            obj.model.set_pose(new_pose)

            # Trigger events at specific times
            if obj.current_time < sim_time and obj.has_events():
                self.trigger_environment_event(obj.get_next_event())

        # Update environment states (weather, lighting, etc.)
        self.update_environment_states(sim_time)

    def trigger_environment_event(self, event):
        # Handle various environmental events
        if event.type == 'door_open':
            self.open_door(event.target)
        elif event.type == 'light_change':
            self.change_lighting(event.parameters)
        elif event.type == 'obstacle_appear':
            self.add_obstacle(event.position)
```

## Sensor Simulation Concepts

Accurate sensor simulation is crucial for developing robust perception and control systems that can transfer from simulation to reality.

### LiDAR Simulation

LiDAR sensors in simulation must accurately model the physical properties of laser ranging:

```
Pseudocode: LiDAR Simulation
class LiDARSimulator:
    def __init__(self, num_beams, max_range, min_range, resolution):
        self.num_beams = num_beams
        self.max_range = max_range
        self.min_range = min_range
        self.fov = 2 * math.pi  # 360-degree scan
        self.angle_increment = self.fov / num_beams
        self.resolution = resolution
        self.noise_model = GaussianNoise(std_dev=0.01)

    def simulate_scan(self, robot_pose, world_geometry):
        scan_data = []

        for i in range(self.num_beams):
            angle = robot_pose.rotation + i * self.angle_increment

            # Ray casting to find intersection
            ray_origin = robot_pose.position
            ray_direction = Vector2(
                math.cos(angle),
                math.sin(angle)
            )

            # Find closest intersection
            min_distance = self.max_range
            for geometry in world_geometry:
                distance = self.ray_intersect(ray_origin, ray_direction, geometry)
                if distance and distance < min_distance:
                    min_distance = distance

            # Apply noise and range limits
            if min_distance < self.max_range:
                noisy_distance = min_distance + self.noise_model.sample()
                scan_data.append(max(self.min_range, noisy_distance))
            else:
                scan_data.append(float('inf'))  # No obstacle detected

        return scan_data

    def ray_intersect(self, origin, direction, geometry):
        # Implement ray-geometry intersection tests
        if geometry.type == 'box':
            return self.ray_box_intersection(origin, direction, geometry)
        elif geometry.type == 'sphere':
            return self.ray_sphere_intersection(origin, direction, geometry)
        elif geometry.type == 'mesh':
            return self.ray_mesh_intersection(origin, direction, geometry)
        return None
```

### Camera Simulation

Camera sensors must model optical properties, distortion, and image formation:

```
Pseudocode: Camera Simulation
class CameraSimulator:
    def __init__(self, width, height, fov, distortion_params):
        self.width = width
        self.height = height
        self.fov = fov
        self.fx = width / (2 * math.tan(fov / 2))  # Focal length x
        self.fy = height / (2 * math.tan(fov / 2))  # Focal length y
        self.cx = width / 2  # Principal point x
        self.cy = height / 2  # Principal point y
        self.distortion = distortion_params  # [k1, k2, p1, p2, k3]

    def simulate_image(self, camera_pose, scene_objects):
        # Create empty image buffer
        image = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        for y in range(self.height):
            for x in range(self.width):
                # Convert pixel coordinates to camera coordinates
                x_norm = (x - self.cx) / self.fx
                y_norm = (y - self.cy) / self.fy

                # Apply distortion correction
                x_distorted, y_distorted = self.apply_distortion(x_norm, y_norm)

                # Ray direction in camera space
                ray_direction = Vector3(x_distorted, y_distorted, 1.0)

                # Transform to world space
                world_ray = camera_pose.transform_vector(ray_direction)

                # Find intersection with scene
                color = self.ray_trace_intersection(world_ray, scene_objects)
                image[y, x] = color

        # Add noise and artifacts
        image = self.add_sensor_noise(image)
        image = self.add_motion_blur(image, camera_pose.velocity)

        return image

    def apply_distortion(self, x, y):
        # Apply radial and tangential distortion
        r_squared = x*x + y*y
        radial_distortion = 1 + self.distortion[0]*r_squared + self.distortion[1]*r_squared*r_squared + self.distortion[4]*r_squared*r_squared*r_squared
        tangential_x = 2*self.distortion[2]*x*y + self.distortion[3]*(r_squared + 2*x*x)
        tangential_y = self.distortion[2]*(r_squared + 2*y*y) + 2*self.distortion[3]*x*y

        x_corrected = x*radial_distortion + tangential_x
        y_corrected = y*radial_distortion + tangential_y

        return x_corrected, y_corrected
```

### IMU Simulation

IMU sensors in simulation must model the physics of acceleration and rotation measurement:

```
Pseudocode: IMU Simulation
class IMUSimulator:
    def __init__(self):
        self.accel_noise = GaussianNoise(std_dev=0.01)
        self.gyro_noise = GaussianNoise(std_dev=0.001)
        self.mag_noise = GaussianNoise(std_dev=0.0001)

        self.accel_bias = Vector3(0, 0, 0)
        self.gyro_bias = Vector3(0, 0, 0)
        self.mag_bias = Vector3(0, 0, 0)

    def simulate_imu_data(self, robot_state, dt):
        # Get true acceleration from robot dynamics
        true_acceleration = robot_state.linear_acceleration
        true_angular_velocity = robot_state.angular_velocity

        # Add gravity to acceleration (IMU measures proper acceleration + gravity)
        gravity_vector = Vector3(0, 0, 9.81)
        measured_accel = true_acceleration + robot_state.orientation.rotate(gravity_vector)

        # Add sensor noise and bias
        noisy_accel = measured_accel + self.accel_bias + self.accel_noise.sample_vector3()
        noisy_gyro = true_angular_velocity + self.gyro_bias + self.gyro_noise.sample_vector3()
        noisy_mag = self.get_magnetic_field() + self.mag_bias + self.mag_noise.sample_vector3()

        # Update bias over time (drift)
        self.update_bias_drift(dt)

        return {
            'linear_acceleration': noisy_accel,
            'angular_velocity': noisy_gyro,
            'magnetic_field': noisy_mag,
            'orientation': self.integrate_orientation(noisy_gyro, dt)
        }

    def integrate_orientation(self, angular_velocity, dt):
        # Integrate angular velocity to get orientation (simplified)
        delta_quaternion = self.angular_velocity_to_quaternion(angular_velocity, dt)
        current_orientation = self.current_orientation * delta_quaternion
        return current_orientation.normalize()
```

## Learning Outcomes

By the end of this week, students should be able to:

1. **Configure physics simulation environments** - Set up realistic physics parameters, gravity, and environmental forces for humanoid robot simulation.

2. **Build complex simulation worlds** - Create detailed environments using SDF format with appropriate terrain, obstacles, and dynamic elements.

3. **Simulate realistic sensor data** - Implement accurate models for LiDAR, camera, and IMU sensors that reflect real-world behavior and limitations.

4. **Model contact forces and collisions** - Understand and implement collision detection and response systems that accurately simulate physical interactions.

5. **Design transferable simulation scenarios** - Create simulation environments and tasks that enable effective Sim2Real transfer for humanoid robot applications.

---

# Week 7: Unity Visualization Concepts

## Introduction

Unity provides a powerful platform for high-fidelity visualization and human-robot interaction in digital twin environments. While Gazebo excels at physics simulation, Unity offers superior rendering capabilities, realistic lighting, and immersive visualization that are essential for human-robot interaction design, teleoperation interfaces, and advanced visualization of robot behaviors. This week explores how Unity integrates with robotic systems to create compelling visual experiences and user interfaces for humanoid robotics applications.

## Unity Architecture for Robotics

Unity's architecture provides a flexible framework for creating realistic 3D environments that can be synchronized with robotic simulation and real-world data.

### Unity Scene Structure

Unity organizes 3D content using a hierarchical scene structure:

- **GameObjects**: The fundamental objects in a Unity scene
- **Components**: Attachable behaviors and properties (Transform, Mesh, Scripts)
- **Scenes**: Collections of GameObjects forming complete environments
- **Prefabs**: Reusable object templates for consistent robot models

```
Pseudocode: Unity Robot Model Structure
class RobotModel:
    def __init__(self):
        self.root_object = GameObject("Robot")
        self.joints = {}
        self.links = {}
        self.sensors = {}
        self.controllers = {}

    def create_link(self, name, mass, inertia, visual_mesh):
        link_object = GameObject(name)
        link_object.AddComponent(Rigidbody)
        link_object.GetComponent(Rigidbody).mass = mass
        link_object.GetComponent(Rigidbody).inertia = inertia
        link_object.AddComponent(MeshRenderer).mesh = visual_mesh
        link_object.AddComponent(MeshCollider).sharedMesh = visual_mesh

        return link_object

    def create_joint(self, name, joint_type, parent_link, child_link, limits):
        joint_object = GameObject(name)
        joint_object.transform.parent = parent_link.transform

        if joint_type == "revolute":
            joint_component = joint_object.AddComponent(HingeJoint)
            joint_component.axis = limits.axis
            joint_component.limits = JointLimits(
                min=limits.min_angle,
                max=limits.max_angle,
                bounciness=limits.bounce
            )
        elif joint_type == "prismatic":
            joint_component = joint_object.AddComponent(ConfigurableJoint)
            # Configure prismatic joint parameters

        return joint_object
```

### Coordinate Systems and Transformations

Unity uses a left-handed coordinate system that must be carefully converted when integrating with ROS and other robotics frameworks:

- **Unity**: X-right, Y-up, Z-forward (left-handed)
- **ROS**: X-forward, Y-left, Z-up (right-handed)

```
Pseudocode: Coordinate System Conversion
class CoordinateConverter:
    def __init__(self):
        # Transformation matrix from ROS to Unity
        self.ros_to_unity = Matrix4x4([
            [0, 0, 1, 0],
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]
        ])

    def ros_to_unity_position(self, ros_position):
        # Convert ROS position (x, y, z) to Unity position
        ros_vec = Vector4(ros_position.x, ros_position.y, ros_position.z, 1)
        unity_vec = self.ros_to_unity * ros_vec
        return Vector3(unity_vec.x, unity_vec.y, unity_vec.z)

    def ros_to_unity_orientation(self, ros_quaternion):
        # Convert ROS quaternion to Unity quaternion
        # Apply coordinate system transformation
        unity_quat = Quaternion(
            w=ros_quaternion.w,
            x=-ros_quaternion.z,
            y=ros_quaternion.x,
            z=ros_quaternion.y
        )
        return unity_quat.normalize()

    def unity_to_ros_transform(self, unity_transform):
        # Convert Unity transform to ROS transform
        ros_position = self.unity_to_ros_position(unity_transform.position)
        ros_orientation = self.unity_to_ros_orientation(unity_transform.rotation)
        return ROS_Transform(ros_position, ros_orientation)
```

## High-Fidelity Rendering and Materials

Unity's rendering pipeline enables photorealistic visualization that's crucial for human-robot interaction and teleoperation scenarios.

### Physically-Based Rendering (PBR)

PBR materials provide realistic surface properties that respond appropriately to lighting:

```
Pseudocode: PBR Material System
class PBRMaterialSystem:
    def __init__(self):
        self.material_library = {}
        self.shader_properties = {}

    def create_robot_material(self, material_type):
        if material_type == "metal":
            material = Material(StandardShader)
            material.SetTexture("_MainTex", self.load_texture("robot_metal_albedo.png"))
            material.SetTexture("_BumpMap", self.load_texture("robot_metal_normal.png"))
            material.SetTexture("_MetallicGlossMap", self.load_texture("robot_metal_metallic.png"))
            material.SetFloat("_Metallic", 0.9)  # High metallic value
            material.SetFloat("_Smoothness", 0.8)  # High smoothness
            material.SetColor("_Color", Color(0.7, 0.7, 0.8))  # Metallic blue-gray

        elif material_type == "plastic":
            material = Material(StandardShader)
            material.SetTexture("_MainTex", self.load_texture("robot_plastic_albedo.png"))
            material.SetFloat("_Metallic", 0.1)  # Low metallic value
            material.SetFloat("_Smoothness", 0.3)  # Medium smoothness
            material.SetColor("_Color", Color(0.3, 0.6, 0.9))  # Plastic blue

        return material

    def apply_material_properties(self, game_object, material_properties):
        # Apply wear patterns, scratches, and aging effects
        material = game_object.GetComponent(MeshRenderer).material
        material.SetTexture("_DetailMask", self.create_wear_pattern(material_properties))
        material.SetFloat("_OcclusionStrength", material_properties.occlusion_strength)
        material.SetFloat("_Parallax", material_properties.parallax_scale)
```

### Advanced Lighting Systems

Realistic lighting is crucial for creating immersive robot environments:

```
Pseudocode: Lighting System
class AdvancedLighting:
    def __init__(self):
        self.light_probes = []
        self.reflection_probes = []
        self.global_illumination = GlobalIllumination()

    def setup_environment_lighting(self, environment_type):
        if environment_type == "indoor_office":
            # Setup directional light (simulating windows/overhead lights)
            sun_light = GameObject("SunLight")
            sun_light.AddComponent(Light)
            sun_light.GetComponent(Light).type = LightType.Directional
            sun_light.GetComponent(Light).color = Color(0.98, 0.92, 0.85)  # Warm white
            sun_light.GetComponent(Light).intensity = 1.2
            sun_light.transform.rotation = Quaternion.Euler(50, -30, 0)

            # Add ambient lighting
            RenderSettings.ambientMode = UnityEngine.Rendering.AmbientMode.Trilight
            RenderSettings.ambientSkyColor = Color(0.4, 0.5, 0.7)
            RenderSettings.ambientEquatorColor = Color(0.2, 0.3, 0.5)
            RenderSettings.ambientGroundColor = Color(0.1, 0.15, 0.25)

            # Setup reflection probes for metallic surfaces
            self.create_reflection_probes_for_environment()

        elif environment_type == "outdoor":
            # More intense directional light (sun)
            sun_light = GameObject("Sun")
            sun_light.AddComponent(Light)
            sun_light.GetComponent(Light).type = LightType.Directional
            sun_light.GetComponent(Light).color = Color(1.0, 0.95, 0.8)
            sun_light.GetComponent(Light).intensity = 1.5
            sun_light.transform.rotation = Quaternion.Euler(60, 120, 0)

            # Skybox for realistic background
            RenderSettings.skybox = self.load_skybox_material("outdoor_skybox")

    def create_light_probes(self, positions):
        # Create light probe volumes for accurate lighting on moving objects
        for pos in positions:
            probe = GameObject("LightProbe")
            probe.transform.position = pos
            probe.AddComponent(LightProbeGroup)
            self.light_probes.append(probe)

    def setup_global_illumination(self, environment_bounds):
        # Configure baked lighting for static objects
        self.global_illumination.bake_static_objects = True
        self.global_illumination.lightmap_resolution = 64  # texels per unit
        self.global_illumination.indirect_intensity = 1.5
        self.global_illumination.environment_lighting = True
```

## Human-Robot Interaction Design

Unity's interface capabilities make it ideal for designing human-robot interaction systems, including teleoperation interfaces and augmented reality applications.

### User Interface Systems

Creating intuitive interfaces for robot control and monitoring:

```
Pseudocode: HRI Interface System
class HumanRobotInterface:
    def __init__(self):
        self.canvas = Canvas()
        self.robot_status_panel = self.create_robot_status_panel()
        self.control_interface = self.create_control_interface()
        self.camera_system = self.create_camera_system()

    def create_robot_status_panel(self):
        # Create status panel showing robot vitals
        status_panel = GameObject("RobotStatusPanel")
        status_panel.AddComponent(RectTransform)

        # Battery indicator
        battery_bar = self.create_progress_bar("Battery", Color.green, Color.red)
        battery_text = self.create_text_element("Battery: 85%", 16)

        # Joint status display
        joint_status_container = GameObject("JointStatusContainer")
        for joint_name in self.robot_joints:
            joint_display = self.create_joint_status_display(joint_name)
            joint_status_container.AddChild(joint_display)

        return status_panel

    def create_control_interface(self):
        # Create teleoperation controls
        control_panel = GameObject("ControlPanel")

        # Movement controls
        movement_controls = self.create_movement_joystick()

        # Action buttons
        action_buttons = []
        for action in ["walk", "grasp", "speak", "emergency_stop"]:
            button = self.create_action_button(action)
            action_buttons.append(button)

        # Gesture recognition interface
        gesture_recognition = self.create_gesture_interface()

        return control_panel

    def create_camera_system(self):
        # Multiple camera views for comprehensive robot monitoring
        cameras = {}

        # Main view - third person follow
        main_camera = self.create_follow_camera("MainCamera", offset=Vector3(-3, 2, 0))
        cameras["main"] = main_camera

        # First person view from robot perspective
        fpv_camera = self.create_robot_camera("FPVCamera", mount_point="head")
        cameras["fpv"] = fpv_camera

        # Sensor view cameras (LiDAR, depth camera simulation)
        sensor_cameras = self.create_sensor_cameras()
        cameras.update(sensor_cameras)

        return cameras
```

### Gesture Recognition and Input Systems

Advanced input systems for natural human-robot interaction:

```
Pseudocode: Gesture Recognition System
class GestureRecognition:
    def __init__(self):
        self.tracked_joints = []
        self.gesture_templates = {}
        self.current_gesture_buffer = []
        self.recognition_threshold = 0.8

    def initialize_gesture_system(self):
        # Setup camera for gesture recognition
        self.camera = GameObject("GestureCamera")
        self.camera.AddComponent(WebCamTexture)
        self.camera.AddComponent(ImageProcessingComponent)

        # Initialize gesture templates
        self.load_gesture_templates()

    def recognize_gesture(self, hand_positions):
        # Process hand tracking data and match to templates
        current_gesture = self.extract_gesture_features(hand_positions)
        self.current_gesture_buffer.append(current_gesture)

        # Keep only recent gesture data
        if len(self.current_gesture_buffer) > 10:
            self.current_gesture_buffer.pop(0)

        # Match against templates
        best_match = None
        best_score = 0

        for template_name, template in self.gesture_templates.items():
            score = self.match_gesture_to_template(
                self.current_gesture_buffer,
                template
            )
            if score > best_score:
                best_score = score
                best_match = template_name

        if best_score > self.recognition_threshold:
            return best_match
        return None

    def extract_gesture_features(self, positions):
        # Extract meaningful features from hand positions
        features = {}

        # Calculate joint angles
        features["finger_angles"] = self.calculate_finger_angles(positions)

        # Calculate hand velocity
        features["hand_velocity"] = self.calculate_velocity(positions)

        # Calculate spatial relationships
        features["finger_distances"] = self.calculate_finger_distances(positions)

        return features
```

## Real-time Simulation Synchronization

Synchronizing Unity visualization with real-time robotic systems requires careful timing and data management.

### ROS Integration

Connecting Unity to ROS systems for real-time data exchange:

```
Pseudocode: ROS Integration System
class UnityROSBridge:
    def __init__(self):
        self.ros_node = None
        self.subscribers = {}
        self.publishers = {}
        self.synchronization_manager = SynchronizationManager()

    def initialize_ros_connection(self):
        # Initialize ROS connection
        self.ros_node = rclpy.create_node('unity_bridge')

        # Create subscribers for robot data
        self.subscribers['joint_states'] = self.ros_node.create_subscription(
            sensor_msgs.msg.JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.subscribers['robot_pose'] = self.ros_node.create_subscription(
            geometry_msgs.msg.PoseStamped,
            '/robot_pose',
            self.robot_pose_callback,
            10
        )

        # Create publishers for Unity commands
        self.publishers['unity_commands'] = self.ros_node.create_publisher(
            std_msgs.msg.String,
            '/unity_commands',
            10
        )

    def joint_state_callback(self, msg):
        # Update Unity robot model with joint states
        for i, joint_name in enumerate(msg.name):
            if joint_name in self.robot_model.joints:
                joint_angle = msg.position[i]
                self.update_joint_in_unity(joint_name, joint_angle)

    def robot_pose_callback(self, msg):
        # Update Unity robot position and orientation
        unity_position = self.ros_to_unity_position(msg.pose.position)
        unity_rotation = self.ros_to_unity_orientation(msg.pose.orientation)

        self.robot_model.root_object.transform.position = unity_position
        self.robot_model.root_object.transform.rotation = unity_rotation

    def synchronize_simulation(self, unity_time, ros_time):
        # Ensure Unity and ROS simulation are synchronized
        time_difference = abs(unity_time - ros_time)

        if time_difference > 0.1:  # 100ms threshold
            # Resynchronize by interpolating between states
            target_time = max(unity_time, ros_time)
            self.interpolate_robot_state(target_time)

        # Maintain consistent frame rate
        self.maintain_frame_rate()
```

### Performance Optimization

Optimizing Unity for real-time robotics applications:

```
Pseudocode: Performance Optimization System
class PerformanceOptimizer:
    def __init__(self):
        self.lod_system = LODSystem()
        self.occlusion_culling = OcclusionCulling()
        self.object_pooling = ObjectPooling()
        self.rendering_pipeline = RenderingPipeline()

    def optimize_robot_rendering(self, robot_model):
        # Apply Level of Detail (LOD) to robot components
        for component in robot_model.get_components():
            lod_group = component.AddComponent(LODGroup)
            lods = [
                LOD(0.0, [self.get_high_detail_mesh(component)]),  # High detail
                LOD(0.01, [self.get_medium_detail_mesh(component)]),  # Medium detail
                LOD(0.05, [self.get_low_detail_mesh(component)])  # Low detail
            ]
            lod_group.SetLODs(lods)

        # Enable occlusion culling for robot components
        self.occlusion_culling.add_static_objects(robot_model.get_environment_objects())

    def implement_object_pooling(self):
        # Pre-instantiate objects to avoid runtime allocation
        for obj_type in ["laser_points", "particles", "effects"]:
            pool = []
            for i in range(100):  # Pre-allocate 100 objects
                obj = self.instantiate_object(obj_type)
                obj.SetActive(False)  # Inactive in pool
                pool.append(obj)
            self.object_pooling.register_pool(obj_type, pool)

    def optimize_rendering_pipeline(self):
        # Configure rendering for robotics applications
        self.rendering_pipeline.use_forward_rendering = True  # Better for real-time
        self.rendering_pipeline.shadow_distance = 50.0  # Optimize shadow rendering
        self.rendering_pipeline.texture_resolution = 1024  # Balance quality/performance
        self.rendering_pipeline.occlusion_culling = True
        self.rendering_pipeline.dynamic_batching = True
        self.rendering_pipeline.static_batching = True
```

## Augmented Reality Integration

Unity's AR capabilities enable overlaying robot information onto real-world environments:

```
Pseudocode: AR Integration System
class ARIntegration:
    def __init__(self):
        self.ar_session = ARSession()
        self.robot_visualization = RobotARVisualization()
        self.spatial_mapping = SpatialMapping()

    def initialize_ar_session(self):
        # Initialize AR session with camera and plane detection
        self.ar_session.Initialize()

        # Setup plane detection for placing robot visualizations
        self.ar_session.plane_detection = PlaneDetection.Horizontal
        self.ar_session.plane_detection_callback = self.on_plane_detected

        # Setup image tracking for robot markers
        self.ar_session.image_tracking = True
        self.ar_session.tracked_images = self.load_robot_markers()

    def visualize_robot_in_ar(self, robot_pose, robot_state):
        # Create AR visualization of robot at real-world location
        robot_ar_object = self.robot_visualization.create_robot_model()

        # Position robot in AR space
        ar_position = self.transform_ros_to_ar(robot_pose.position)
        ar_rotation = self.transform_ros_to_ar(robot_pose.orientation)

        robot_ar_object.transform.position = ar_position
        robot_ar_object.transform.rotation = ar_rotation

        # Update robot state visualization
        self.update_robot_state_visualization(robot_ar_object, robot_state)

        # Add interaction affordances
        self.add_interaction_handles(robot_ar_object)

    def create_robot_state_visualization(self, robot_object, state):
        # Visualize robot state information in AR
        # Joint angles as overlay indicators
        for joint_name, angle in state.joint_angles.items():
            angle_indicator = self.create_angle_indicator(joint_name, angle)
            self.attach_to_joint(robot_object, joint_name, angle_indicator)

        # Sensor data visualization
        if hasattr(state, 'lidar_data'):
            lidar_visualization = self.create_lidar_visualization(state.lidar_data)
            self.attach_sensor_visualization(robot_object, lidar_visualization)

        # Planning and navigation visualization
        if hasattr(state, 'planned_path'):
            path_visualization = self.create_path_visualization(state.planned_path)
            self.attach_path_visualization(robot_object, path_visualization)
```

## Learning Outcomes

By the end of this week, students should be able to:

1. **Design Unity scenes for robotics** - Create hierarchical robot models with appropriate coordinate system conversions and component structures.

2. **Implement high-fidelity visualization** - Apply physically-based rendering, advanced lighting, and realistic materials to create compelling robot visualizations.

3. **Develop human-robot interaction interfaces** - Create intuitive user interfaces, gesture recognition systems, and teleoperation controls in Unity.

4. **Integrate with real-time systems** - Connect Unity to ROS and other robotic systems for synchronized visualization and control.

5. **Optimize performance for real-time applications** - Apply LOD systems, object pooling, and rendering optimization techniques for smooth robot visualization.

---