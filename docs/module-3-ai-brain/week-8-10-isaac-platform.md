---
title: NVIDIA Isaac Platform
sidebar_position: 1
description: AI-powered perception and manipulation with Isaac SDK
---

# Week 8: NVIDIA Isaac Platform Introduction

## Introduction

The NVIDIA Isaac platform represents a comprehensive ecosystem for developing AI-powered robotic applications, specifically designed to leverage GPU acceleration for perception, navigation, and manipulation tasks. This week introduces the core components of the Isaac platform, including Isaac ROS, Isaac Sim, and Isaac Lab, and explores how these tools enable the development of sophisticated humanoid robots capable of intelligent behavior in complex environments.

## NVIDIA Isaac Platform Architecture

The Isaac platform provides a unified framework that bridges simulation, perception, and real-world deployment through a suite of interconnected tools and libraries.

### Isaac Platform Components

The Isaac ecosystem consists of several key components:

- **Isaac ROS**: GPU-accelerated ROS 2 packages for perception and navigation
- **Isaac Sim**: High-fidelity physics simulation and synthetic data generation
- **Isaac Lab**: Reinforcement learning and imitation learning framework
- **Isaac Apps**: Reference applications and demonstrations
- **Isaac Core**: Foundational libraries and tools

```
Pseudocode: Isaac Platform Architecture
class IsaacPlatform:
    def __init__(self):
        self.isaac_ros = IsaacROS()
        self.isaac_sim = IsaacSim()
        self.isaac_lab = IsaacLab()
        self.isaac_apps = IsaacApps()
        self.isaac_core = IsaacCore()

        self.hardware_abstraction = HardwareAbstractionLayer()
        self.gpu_manager = GPUResourceManager()
        self.data_pipeline = DataPipeline()

    def initialize_platform(self):
        # Initialize core components
        self.isaac_core.initialize()

        # Configure GPU resources
        self.gpu_manager.initialize_gpus()
        self.gpu_manager.allocate_memory_pools()

        # Set up data pipeline
        self.data_pipeline.setup_message_passing()
        self.data_pipeline.configure_compression()

        # Initialize simulation environment
        self.isaac_sim.initialize()

        # Initialize ROS integration
        self.isaac_ros.initialize()

    def create_robot_application(self, robot_description):
        # Create robot-specific application
        robot_app = RobotApplication(robot_description)

        # Configure perception pipeline
        perception_pipeline = self.isaac_ros.create_perception_pipeline()
        perception_pipeline.add_gpu_nodes([
            'isaac_ros_detectnet',      # Object detection
            'isaac_ros_pointcloud',     # 3D point cloud processing
            'isaac_ros_image_proc'      # Image processing
        ])

        # Configure navigation pipeline
        navigation_pipeline = self.isaac_ros.create_navigation_pipeline()
        navigation_pipeline.add_gpu_nodes([
            'isaac_ros_costmap_2d',     # 2D costmap generation
            'isaac_ros_planner',        # Path planning
            'isaac_ros_controller'      # Motion control
        ])

        robot_app.set_perception_pipeline(perception_pipeline)
        robot_app.set_navigation_pipeline(navigation_pipeline)

        return robot_app
```

### GPU Acceleration Framework

Isaac leverages NVIDIA's GPU ecosystem for accelerated computation:

```
Pseudocode: GPU Acceleration System
class GPUAcceleration:
    def __init__(self):
        self.gpu_devices = self.detect_gpu_devices()
        self.memory_manager = GPUMemoryManager()
        self.compute_contexts = {}
        self.tensor_cores = TensorCoreManager()

    def setup_compute_context(self, device_id):
        # Create CUDA context for specific GPU
        context = cuda.Context(device_id)
        self.compute_contexts[device_id] = context

        # Allocate memory pools
        self.memory_manager.allocate_pinned_memory(device_id, size_gb=4)
        self.memory_manager.allocate_unified_memory(device_id, size_gb=8)

        # Initialize Tensor Core operations for mixed precision
        self.tensor_cores.enable_mixed_precision(device_id)

        return context

    def accelerate_perception_task(self, task_type, input_data):
        # Select appropriate GPU based on task requirements
        gpu_id = self.select_optimal_gpu(task_type)
        context = self.compute_contexts[gpu_id]

        with context:
            # Transfer data to GPU memory
            gpu_input = self.memory_manager.copy_to_gpu(input_data, gpu_id)

            if task_type == 'object_detection':
                # Use TensorRT for optimized inference
                result = self.tensorrt_inference(
                    model='detectnet_model',
                    input=gpu_input,
                    precision='fp16'  # Mixed precision
                )

            elif task_type == 'pointcloud_processing':
                # Use CUDA kernels for point cloud operations
                result = self.cuda_pointcloud_process(gpu_input)

            elif task_type == 'image_processing':
                # Use GPU-accelerated image processing
                result = self.gpu_image_process(gpu_input)

            # Transfer result back to CPU memory
            cpu_result = self.memory_manager.copy_to_cpu(result, gpu_id)

        return cpu_result

    def optimize_memory_usage(self):
        # Implement memory optimization strategies
        self.memory_manager.enable_memory_pooling()
        self.memory_manager.setup_memory_caching()
        self.memory_manager.configure_streaming()
```

## Isaac ROS: GPU-Accelerated ROS 2 Packages

Isaac ROS provides GPU-accelerated implementations of common ROS 2 packages, significantly improving performance for perception and navigation tasks.

### Isaac ROS Package Ecosystem

Key Isaac ROS packages include:

- **isaac_ros_detectnet**: Object detection using NVIDIA's DetectNet
- **isaac_ros_pointcloud**: GPU-accelerated point cloud processing
- **isaac_ros_image_proc**: High-performance image processing
- **isaac_ros_visual_slam**: Visual SLAM with GPU acceleration
- **isaac_ros_pose_estimation**: Real-time pose estimation

```
Pseudocode: Isaac ROS Node Implementation
class IsaacROSNode:
    def __init__(self, node_name):
        self.node = rclpy.create_node(node_name)
        self.gpu_pipeline = GPUPipeline()
        self.tensorrt_engine = None
        self.input_queue = queue.Queue(maxsize=10)
        self.output_queue = queue.Queue(maxsize=10)

    def initialize_gpu_pipeline(self, model_path, input_shape):
        # Load TensorRT engine for optimized inference
        self.tensorrt_engine = self.load_tensorrt_engine(model_path)

        # Configure GPU memory allocation
        self.gpu_pipeline.allocate_tensors(
            input_shape=input_shape,
            output_shape=self.get_output_shape(model_path)
        )

        # Set up CUDA streams for asynchronous processing
        self.gpu_pipeline.setup_cuda_streams(num_streams=2)

    def process_gpu_inference(self, input_data):
        # Asynchronous GPU inference
        with self.gpu_pipeline.get_stream() as stream:
            # Copy input to GPU memory
            gpu_input = self.gpu_pipeline.copy_input(input_data, stream)

            # Execute TensorRT inference
            gpu_output = self.tensorrt_engine.execute_async(
                bindings=[gpu_input, self.gpu_pipeline.get_output_buffer()],
                stream_handle=stream.cuda_stream
            )

            # Copy result back to CPU
            output_result = self.gpu_pipeline.copy_output(gpu_output, stream)

        return output_result

    def create_isaac_ros_publisher(self, msg_type, topic_name):
        # Create publisher with GPU-optimized message handling
        publisher = self.node.create_publisher(msg_type, topic_name, 10)

        # Optimize for GPU-accelerated data
        publisher.set_qos_profile(
            rclpy.qos.QoSProfile(
                reliability=rclpy.qos.ReliabilityPolicy.RELIABLE,
                durability=rclpy.qos.DurabilityPolicy.VOLATILE,
                history=rclpy.qos.HistoryPolicy.KEEP_LAST,
                depth=1  # Minimize memory usage for high-frequency data
            )
        )

        return publisher
```

### GPU-Accelerated Perception Pipeline

Building an optimized perception pipeline using Isaac ROS:

```
Pseudocode: Perception Pipeline
class PerceptionPipeline:
    def __init__(self):
        self.image_subscriber = None
        self.detection_publisher = None
        self.pointcloud_subscriber = None
        self.gpu_pipeline = GPUPipeline()
        self.synchronization = MessageSynchronizer()

    def setup_gpu_perception_nodes(self):
        # Initialize Isaac ROS nodes with GPU acceleration
        self.image_subscriber = self.node.create_subscription(
            sensor_msgs.msg.Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        # Object detection node
        self.detection_node = self.create_gpu_detection_node()

        # Depth processing node
        self.depth_node = self.create_gpu_depth_node()

        # Point cloud fusion node
        self.fusion_node = self.create_gpu_fusion_node()

    def image_callback(self, image_msg):
        # Process image using GPU acceleration
        image_tensor = self.convert_image_to_tensor(image_msg)

        # Run object detection on GPU
        detections = self.detection_node.run_inference(image_tensor)

        # Process depth information
        depth_tensor = self.get_depth_tensor(image_msg.header.stamp)
        depth_processed = self.depth_node.process(depth_tensor)

        # Fuse detection and depth data
        fused_result = self.fusion_node.fuse_data(detections, depth_processed)

        # Publish results
        self.publish_detection_results(fused_result, image_msg.header)

    def create_gpu_detection_node(self):
        # Create GPU-optimized detection pipeline
        detection_node = IsaacDetectionNode()

        # Load optimized model
        detection_node.load_model(
            model_path='detectnet_model.plan',  # TensorRT optimized
            input_shape=(3, 512, 512),
            output_shape=(1, 100, 7)  # batch, detections, (class, conf, x, y, w, h, angle)
        )

        # Configure GPU memory
        detection_node.configure_gpu_memory(
            input_buffer_size=512*512*3*4,  # 4 bytes per float
            output_buffer_size=100*7*4,
            max_batch_size=8
        )

        return detection_node
```

## Isaac Sim: Physics Simulation and Synthetic Data Generation

Isaac Sim provides high-fidelity physics simulation and synthetic data generation capabilities essential for training AI models without real-world data collection.

### Simulation Environment Architecture

Isaac Sim builds upon Omniverse technology to provide realistic simulation:

```
Pseudocode: Isaac Sim Environment
class IsaacSimEnvironment:
    def __init__(self):
        self.sim_app = omni.kit.app.get_app()
        self.physics_context = PhysicsContext()
        self.renderer = KitRenderer()
        self.synthetic_data_generator = SyntheticDataGenerator()
        self.domain_randomization = DomainRandomization()

    def create_simulation_world(self, world_config):
        # Create physics scene
        self.physics_context.create_simulation()

        # Set up physics properties
        self.physics_context.set_gravity(world_config.gravity)
        self.physics_context.set_timestep(world_config.timestep)
        self.physics_context.set_solver_iterations(world_config.solver_iterations)

        # Create ground plane
        ground_plane = self.create_ground_plane(
            size=world_config.ground_size,
            friction=world_config.ground_friction,
            restitution=world_config.ground_restitution
        )

        # Create lighting environment
        self.setup_environment_lighting(world_config.lighting_config)

        # Create dynamic objects
        for obj_config in world_config.objects:
            self.create_dynamic_object(obj_config)

    def setup_synthetic_data_generation(self):
        # Configure synthetic data generation pipeline
        self.synthetic_data_generator.set_camera_config(
            resolution=(1920, 1080),
            fov=60.0,
            sensor_noise={'mean': 0.0, 'std': 0.001}
        )

        # Set up annotation generation
        self.synthetic_data_generator.enable_annotations([
            'bounding_box_2d_tight',
            'instance_segmentation',
            'depth',
            'normals',
            'motion_vectors'
        ])

        # Configure domain randomization
        self.domain_randomization.set_randomization_ranges({
            'lighting': {'intensity_range': (0.5, 2.0)},
            'textures': {'roughness_range': (0.1, 0.9)},
            'materials': {'color_range': ('red', 'blue', 'green')}
        })

    def generate_synthetic_dataset(self, num_samples, scenario_configs):
        dataset = []

        for i in range(num_samples):
            # Apply domain randomization
            self.domain_randomization.randomize_scene()

            # Execute scenario
            scenario_config = random.choice(scenario_configs)
            self.execute_scenario(scenario_config)

            # Capture synthetic data
            frame_data = self.synthetic_data_generator.capture_frame()
            annotations = self.synthetic_data_generator.generate_annotations()

            sample = {
                'image': frame_data['rgb'],
                'depth': frame_data['depth'],
                'annotations': annotations,
                'scenario': scenario_config,
                'randomization_params': self.domain_randomization.get_current_params()
            }

            dataset.append(sample)

        return dataset
```

### Physics Simulation Capabilities

Advanced physics simulation for humanoid robot development:

```
Pseudocode: Advanced Physics Simulation
class AdvancedPhysicsSimulation:
    def __init__(self):
        self.material_properties = MaterialProperties()
        self.contact_properties = ContactProperties()
        self.deformable_bodies = DeformableBodySystem()
        self.fluid_simulation = FluidSimulation()

    def setup_material_properties(self):
        # Configure realistic material properties
        self.material_properties.set_defaults({
            'robot_metal': {
                'density': 7800,  # kg/m^3
                'youngs_modulus': 200e9,  # Pa
                'poissons_ratio': 0.3,
                'static_friction': 0.5,
                'dynamic_friction': 0.4,
                'restitution': 0.2
            },
            'rubber_foot': {
                'density': 1200,
                'youngs_modulus': 1e6,
                'poissons_ratio': 0.49,
                'static_friction': 0.8,
                'dynamic_friction': 0.7,
                'restitution': 0.1
            }
        })

    def simulate_robot_environment_interaction(self, robot, environment):
        # Simulate complex interactions between robot and environment
        for link in robot.links:
            for contact_point in self.detect_contacts(link, environment):
                # Calculate contact forces
                contact_force = self.calculate_contact_force(
                    contact_point,
                    link.material,
                    environment.material
                )

                # Apply forces to robot dynamics
                link.apply_force(contact_force, contact_point.position)

                # Handle friction and sliding
                if self.is_sliding(contact_point):
                    friction_force = self.calculate_friction_force(contact_point)
                    link.apply_force(friction_force, contact_point.position)

    def simulate_deformable_contacts(self, robot, soft_objects):
        # Handle interactions with deformable objects
        for soft_obj in soft_objects:
            deformation = self.calculate_deformation(robot, soft_obj)
            soft_obj.apply_deformation(deformation)

            # Update collision geometry based on deformation
            soft_obj.update_collision_mesh(deformation)
```

## Isaac Lab: Reinforcement Learning Framework

Isaac Lab provides a comprehensive framework for training robotic policies using reinforcement learning and imitation learning.

### Reinforcement Learning Environment

```
Pseudocode: Isaac Lab RL Environment
class IsaacLabEnvironment:
    def __init__(self, task_config):
        self.task_config = task_config
        self.simulation = IsaacSimEnvironment()
        self.observation_space = self.define_observation_space()
        self.action_space = self.define_action_space()
        self.reward_function = self.define_reward_function()
        self.termination_conditions = self.define_termination_conditions()

    def define_observation_space(self):
        # Define observation space for RL agent
        observation_spec = {
            'joint_positions': {
                'shape': (self.robot.num_joints,),
                'dtype': np.float32,
                'low': -np.pi,
                'high': np.pi
            },
            'joint_velocities': {
                'shape': (self.robot.num_joints,),
                'dtype': np.float32,
                'low': -10.0,
                'high': 10.0
            },
            'base_pose': {
                'shape': (7,),  # [x, y, z, qw, qx, qy, qz]
                'dtype': np.float32,
                'low': [-np.inf, -np.inf, 0, -1, -1, -1, -1],
                'high': [np.inf, np.inf, np.inf, 1, 1, 1, 1]
            },
            'sensor_data': {
                'shape': (self.sensor_size,),
                'dtype': np.float32,
                'low': -np.inf,
                'high': np.inf
            }
        }
        return observation_spec

    def define_action_space(self):
        # Define action space for humanoid robot
        action_spec = {
            'joint_commands': {
                'shape': (self.robot.num_joints,),
                'dtype': np.float32,
                'low': -np.pi,
                'high': np.pi
            },
            'gains': {
                'shape': (self.robot.num_joints * 2,),  # [position_gains, velocity_gains]
                'dtype': np.float32,
                'low': 0.0,
                'high': 1000.0
            }
        }
        return action_spec

    def define_reward_function(self):
        # Define reward function for humanoid locomotion
        def reward_function(state, action, next_state, info):
            reward = 0.0

            # Progress reward - move forward
            progress = next_state['base_pose'][0] - state['base_pose'][0]
            reward += progress * 10.0

            # Velocity reward - maintain target speed
            current_velocity = self.calculate_base_velocity(next_state)
            target_velocity = self.task_config.target_velocity
            velocity_reward = -abs(current_velocity - target_velocity) * 5.0
            reward += velocity_reward

            # Balance reward - maintain upright posture
            base_orientation = next_state['base_pose'][3:7]  # quaternion
            upright_reward = self.calculate_upright_reward(base_orientation) * 2.0
            reward += upright_reward

            # Smoothness reward - penalize jerky movements
            action_smoothness = -np.sum(np.abs(action)) * 0.1
            reward += action_smoothness

            return reward

        return reward_function

    def reset(self):
        # Reset environment to initial state
        self.simulation.reset()

        # Apply randomization if enabled
        if self.task_config.randomize:
            self.randomize_environment()

        # Get initial observation
        initial_state = self.get_current_state()
        return self.format_observation(initial_state)

    def step(self, action):
        # Execute one step of the environment
        previous_state = self.get_current_state()

        # Apply action to robot
        self.apply_action_to_robot(action)

        # Step simulation
        self.simulation.step()

        # Get new state
        current_state = self.get_current_state()

        # Calculate reward
        reward = self.reward_function(previous_state, action, current_state, {})

        # Check termination conditions
        terminated = self.check_termination(current_state)
        truncated = self.check_truncation(current_state)

        # Get observation
        observation = self.format_observation(current_state)

        # Get info dictionary
        info = self.get_info_dict(current_state, reward)

        return observation, reward, terminated, truncated, info
```

## Learning Outcomes

By the end of this week, students should be able to:

1. **Understand Isaac platform architecture** - Explain the components and capabilities of the NVIDIA Isaac ecosystem for AI-powered robotics.

2. **Implement GPU-accelerated perception** - Create perception pipelines using Isaac ROS packages that leverage GPU acceleration for real-time performance.

3. **Configure Isaac Sim environments** - Set up high-fidelity simulation environments with appropriate physics properties and synthetic data generation capabilities.

4. **Design reinforcement learning environments** - Create RL environments in Isaac Lab with appropriate observation spaces, action spaces, and reward functions for humanoid robot tasks.

5. **Integrate Isaac components** - Connect simulation, perception, and control systems using the Isaac platform for comprehensive humanoid robot development.

---

# Week 9: AI Perception and Control

## Introduction

AI perception and control form the cognitive core of humanoid robots, enabling them to understand their environment, make intelligent decisions, and execute complex behaviors. This week explores the integration of artificial intelligence techniques with robotic perception and control systems, focusing on computer vision, sensor fusion, and intelligent control strategies that enable humanoid robots to operate autonomously in complex environments.

## Computer Vision for Robotics

Computer vision provides humanoid robots with the ability to interpret visual information from cameras and other optical sensors, enabling navigation, object recognition, and interaction with the environment.

### Deep Learning-Based Object Detection

Modern object detection systems use deep neural networks to identify and locate objects in images:

```
Pseudocode: Object Detection System
class ObjectDetectionSystem:
    def __init__(self):
        self.detection_model = self.load_pretrained_model('yolov8')
        self.feature_extractor = FeatureExtractor()
        self.tracker = ObjectTracker()
        self.classifier = ObjectClassifier()

    def detect_objects(self, image):
        # Preprocess image for neural network
        processed_image = self.preprocess_image(image)

        # Run object detection
        detections = self.detection_model.inference(processed_image)

        # Filter detections by confidence threshold
        confident_detections = [
            det for det in detections
            if det.confidence > self.confidence_threshold
        ]

        # Extract features for tracking
        for detection in confident_detections:
            detection.features = self.feature_extractor.extract(
                image, detection.bbox
            )

        # Update object tracker
        tracked_objects = self.tracker.update(confident_detections)

        return tracked_objects

    def preprocess_image(self, image):
        # Resize and normalize image
        resized = cv2.resize(image, (640, 640))
        normalized = resized.astype(np.float32) / 255.0
        normalized = np.transpose(normalized, (2, 0, 1))  # HWC to CHW
        return normalized

    def load_pretrained_model(self, model_name):
        # Load pre-trained model with GPU acceleration
        if model_name == 'yolov8':
            model = YOLOv8Model()
            model.load_weights('yolov8_weights.pt')
            model.to_gpu()
            return model
        elif model_name == 'detectnet':
            return DetectNetModel()
```

### Semantic Segmentation

Semantic segmentation provides pixel-level understanding of the environment:

```
Pseudocode: Semantic Segmentation System
class SemanticSegmentation:
    def __init__(self):
        self.segmentation_model = SegmentationModel('deeplabv3')
        self.color_map = self.create_color_map()
        self.post_processor = SegmentationPostProcessor()

    def segment_image(self, image):
        # Run segmentation inference
        raw_output = self.segmentation_model.inference(image)

        # Apply softmax to get class probabilities
        probabilities = self.softmax(raw_output)

        # Get predicted class for each pixel
        predicted_classes = np.argmax(probabilities, axis=0)

        # Apply post-processing to refine boundaries
        refined_mask = self.post_processor.refine_boundaries(
            predicted_classes, image
        )

        # Convert to colored segmentation map
        colored_map = self.colorize_segmentation(refined_mask)

        return {
            'segmentation_map': refined_mask,
            'colored_map': colored_map,
            'class_probabilities': probabilities
        }

    def colorize_segmentation(self, segmentation_map):
        # Map class indices to RGB colors
        height, width = segmentation_map.shape
        colored_map = np.zeros((height, width, 3), dtype=np.uint8)

        for class_idx in np.unique(segmentation_map):
            mask = segmentation_map == class_idx
            colored_map[mask] = self.color_map[class_idx]

        return colored_map

    def extract_traversable_regions(self, segmentation_result):
        # Identify walkable areas from segmentation
        walkable_classes = ['floor', 'grass', 'carpet', 'road']
        walkable_mask = np.zeros_like(segmentation_result['segmentation_map'])

        for class_name in walkable_classes:
            class_idx = self.get_class_index(class_name)
            walkable_mask[segmentation_result['segmentation_map'] == class_idx] = 1

        return walkable_mask
```

### 3D Perception and Depth Estimation

Understanding 3D structure is crucial for humanoid robot navigation and manipulation:

```
Pseudocode: 3D Perception System
class ThreeDPerception:
    def __init__(self):
        self.depth_estimator = DepthEstimator('monodepth2')
        self.pointcloud_generator = PointCloudGenerator()
        self.surface_analyzer = SurfaceAnalyzer()
        self.obstacle_detector = ObstacleDetector()

    def process_3d_data(self, stereo_images=None, depth_image=None, rgb_image=None):
        if depth_image is not None:
            # Use provided depth image
            depth_map = depth_image
        elif stereo_images is not None:
            # Estimate depth from stereo images
            depth_map = self.depth_estimator.from_stereo(stereo_images)
        elif rgb_image is not None:
            # Estimate depth from single RGB image
            depth_map = self.depth_estimator.from_monocular(rgb_image)

        # Generate point cloud
        pointcloud = self.pointcloud_generator.from_depth(
            depth_map, self.camera_intrinsics
        )

        # Analyze surfaces for navigation
        surfaces = self.surface_analyzer.analyze(pointcloud)

        # Detect obstacles
        obstacles = self.obstacle_detector.detect(pointcloud, surfaces)

        return {
            'depth_map': depth_map,
            'pointcloud': pointcloud,
            'surfaces': surfaces,
            'obstacles': obstacles
        }

    def generate_occupancy_grid(self, pointcloud, resolution=0.1):
        # Create 2D occupancy grid from 3D point cloud
        min_x, min_y = np.min(pointcloud[:, :2], axis=0)
        max_x, max_y = np.max(pointcloud[:, :2], axis=0)

        grid_width = int((max_x - min_x) / resolution)
        grid_height = int((max_y - min_y) / resolution)

        occupancy_grid = np.zeros((grid_width, grid_height), dtype=np.float32)

        for point in pointcloud:
            x_idx = int((point[0] - min_x) / resolution)
            y_idx = int((point[1] - min_y) / resolution)

            if 0 <= x_idx < grid_width and 0 <= y_idx < grid_height:
                # Mark as occupied if point is below robot height threshold
                if point[2] < self.robot_height_threshold:
                    occupancy_grid[x_idx, y_idx] = 1.0

        return occupancy_grid
```

## Sensor Fusion and State Estimation

Integrating data from multiple sensors provides a more complete and accurate understanding of the robot's state and environment.

### Multi-Sensor Data Integration

```
Pseudocode: Sensor Fusion System
class SensorFusion:
    def __init__(self):
        self.kalman_filter = ExtendedKalmanFilter()
        self.particle_filter = ParticleFilter()
        self.imu_processor = IMUProcessor()
        self.odometry_processor = OdometryProcessor()
        self.vision_processor = VisionProcessor()

    def initialize_state_estimator(self, initial_pose, initial_covariance):
        # Initialize Kalman filter state
        self.kalman_filter.initialize(
            state=initial_pose,
            covariance=initial_covariance
        )

        # Initialize particle filter for multimodal distributions
        self.particle_filter.initialize(
            num_particles=1000,
            initial_distribution=initial_pose
        )

    def fuse_sensor_data(self, imu_data, odometry_data, vision_data, dt):
        # Process IMU data (high frequency, relative measurements)
        imu_prediction = self.imu_processor.process(imu_data, dt)

        # Process odometry data (medium frequency, relative measurements)
        odometry_correction = self.odometry_processor.process(odometry_data)

        # Process vision data (low frequency, absolute measurements)
        vision_correction = self.vision_processor.process(vision_data)

        # Fuse all sensor data using Kalman filter
        prediction = self.kalman_filter.predict(imu_prediction, dt)
        corrected_state = self.kalman_filter.update(
            prediction,
            [odometry_correction, vision_correction]
        )

        # Update particle filter for non-linear estimation
        self.particle_filter.update(
            odometry_correction,
            vision_correction,
            imu_prediction
        )

        return {
            'estimated_pose': corrected_state,
            'uncertainty': self.kalman_filter.covariance,
            'particles': self.particle_filter.particles
        }

    def handle_sensor_failures(self, sensor_data):
        # Implement sensor failure detection and graceful degradation
        for sensor_name, data in sensor_data.items():
            if not self.is_sensor_valid(data):
                # Switch to alternative sensor or prediction-only mode
                self.enable_sensor_backup(sensor_name)
                self.log_sensor_failure(sensor_name)
```

### Visual-Inertial Odometry (VIO)

Combining visual and inertial measurements for robust pose estimation:

```
Pseudocode: Visual-Inertial Odometry
class VisualInertialOdometry:
    def __init__(self):
        self.feature_detector = FeatureDetector('orb')
        self.feature_tracker = FeatureTracker()
        self.imu_integrator = IMUIntegrator()
        self.optimization_backend = OptimizationBackend()
        self.keyframe_manager = KeyframeManager()

    def estimate_pose(self, current_image, imu_measurements, previous_pose):
        # Track features from previous frame
        tracked_features = self.feature_tracker.track(
            previous_image=self.previous_image,
            current_image=current_image
        )

        # Integrate IMU measurements for prediction
        imu_prediction = self.imu_integrator.integrate(
            imu_measurements, self.dt
        )

        # Estimate pose from feature correspondences
        visual_pose_estimate = self.estimate_pose_from_features(
            tracked_features, self.camera_intrinsics
        )

        # Fuse visual and inertial estimates
        fused_pose = self.fuse_visual_inertial(
            visual_estimate=visual_pose_estimate,
            inertial_estimate=imu_prediction,
            previous_pose=previous_pose
        )

        # Optimize pose graph for consistency
        optimized_pose = self.optimize_pose_graph(fused_pose)

        # Manage keyframes for map building
        if self.should_add_keyframe(optimized_pose):
            self.keyframe_manager.add_keyframe(
                image=current_image,
                pose=optimized_pose
            )

        self.previous_image = current_image
        return optimized_pose

    def estimate_pose_from_features(self, features, intrinsics):
        # Use PnP (Perspective-n-Point) algorithm
        object_points = self.get_3d_points(features)
        image_points = self.get_2d_points(features)

        success, rvec, tvec = cv2.solvePnP(
            object_points, image_points, intrinsics, None
        )

        if success:
            # Convert rotation vector to rotation matrix
            rotation_matrix, _ = cv2.Rodrigues(rvec)

            # Create transformation matrix
            transform = np.eye(4)
            transform[:3, :3] = rotation_matrix
            transform[:3, 3] = tvec.flatten()

            return transform
        else:
            return None
```

## Intelligent Control Systems

AI-based control systems enable humanoid robots to execute complex behaviors and adapt to changing conditions.

### Model Predictive Control (MPC) with Learning

```
Pseudocode: Learning-Based MPC
class LearningBasedMPC:
    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.dynamics_predictor = DynamicsPredictor()
        self.trajectory_optimizer = TrajectoryOptimizer()
        self.learning_module = LearningModule()
        self.safety_checker = SafetyChecker()

    def compute_control_command(self, current_state, reference_trajectory, horizon=10):
        # Use learned dynamics model to predict future states
        predicted_trajectories = []

        for control_sequence in self.generate_control_candidates(horizon):
            predicted_states = []
            state = current_state.copy()

            for control in control_sequence:
                # Predict next state using learned dynamics
                next_state = self.dynamics_predictor.predict(
                    state, control, self.dt
                )

                # Check safety constraints
                if not self.safety_checker.is_safe(next_state):
                    break

                predicted_states.append(next_state)
                state = next_state

            if len(predicted_states) == len(control_sequence):
                cost = self.evaluate_trajectory_cost(
                    predicted_states, reference_trajectory
                )
                predicted_trajectories.append({
                    'states': predicted_states,
                    'controls': control_sequence,
                    'cost': cost
                })

        # Select optimal trajectory
        optimal_trajectory = min(
            predicted_trajectories,
            key=lambda x: x['cost']
        )

        # Apply learning to improve future predictions
        self.learning_module.update(
            current_state,
            optimal_trajectory['controls'][0]
        )

        return optimal_trajectory['controls'][0]

    def evaluate_trajectory_cost(self, predicted_states, reference_trajectory):
        total_cost = 0.0

        for i, (pred_state, ref_state) in enumerate(zip(predicted_states, reference_trajectory)):
            # Tracking cost
            tracking_error = np.linalg.norm(pred_state - ref_state)
            total_cost += tracking_error ** 2

            # Control effort cost
            if i < len(predicted_states) - 1:
                control_diff = predicted_states[i+1]['control'] - pred_state['control']
                total_cost += 0.1 * np.sum(control_diff ** 2)

            # Safety cost
            if not self.safety_checker.is_safe(pred_state):
                total_cost += 1000.0  # High penalty for unsafe states

        return total_cost
```

### Adaptive Control with Neural Networks

```
Pseudocode: Neural Adaptive Controller
class NeuralAdaptiveController:
    def __init__(self, robot_dof):
        self.robot_dof = robot_dof
        self.adaptive_network = self.build_adaptive_network()
        self.feedback_controller = PIDController()
        self.reference_model = ReferenceModel()
        self.parameter_estimator = ParameterEstimator()

    def build_adaptive_network(self):
        # Build neural network for adaptive control
        network = Sequential([
            Dense(128, activation='relu', input_shape=(self.robot_dof * 4,)),  # [pos, vel, ref_pos, ref_vel]
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(self.robot_dof, activation='linear')  # Adaptive control terms
        ])
        return network

    def compute_adaptive_control(self, current_state, desired_state, dt):
        # Extract relevant state information
        state_error = current_state['position'] - desired_state['position']
        velocity_error = current_state['velocity'] - desired_state['velocity']

        # Prepare network input
        network_input = np.concatenate([
            current_state['position'],
            current_state['velocity'],
            desired_state['position'],
            desired_state['velocity']
        ])

        # Compute adaptive control terms
        adaptive_terms = self.adaptive_network.predict(network_input)

        # Compute feedback control
        feedback_control = self.feedback_controller.compute(
            state_error, velocity_error, dt
        )

        # Combine adaptive and feedback control
        total_control = feedback_control + adaptive_terms

        # Update network based on tracking performance
        self.update_adaptive_network(
            network_input, total_control, state_error
        )

        return total_control

    def update_adaptive_network(self, state_input, control_output, tracking_error):
        # Define target adaptive terms to minimize tracking error
        target_adaptive = self.compute_target_adaptive(
            tracking_error, control_output
        )

        # Train network to predict required adaptive terms
        self.adaptive_network.fit(
            x=state_input.reshape(1, -1),
            y=target_adaptive.reshape(1, -1),
            epochs=1,
            verbose=0
        )
```

## Learning and Adaptation

Enabling robots to learn from experience and adapt to new situations is crucial for autonomous operation.

### Online Learning Systems

```
Pseudocode: Online Learning System
class OnlineLearningSystem:
    def __init__(self):
        self.behavior_models = {}
        self.experience_buffer = ExperienceBuffer(max_size=10000)
        self.learning_algorithm = IncrementalLearner()
        self.performance_monitor = PerformanceMonitor()

    def update_behavior_model(self, task, observation, action, reward, next_observation):
        # Store experience in buffer
        experience = {
            'task': task,
            'observation': observation,
            'action': action,
            'reward': reward,
            'next_observation': next_observation,
            'timestamp': time.time()
        }
        self.experience_buffer.add(experience)

        # Update behavior model incrementally
        if self.should_update_model(task):
            self.learning_algorithm.incremental_update(
                task,
                self.experience_buffer.get_recent_experiences(task, 100)
            )

        # Monitor performance and trigger retraining if needed
        performance = self.performance_monitor.evaluate(task)
        if performance < self.performance_threshold:
            self.trigger_retraining(task)

    def predict_action(self, task, observation):
        # Use learned model to predict best action
        if task in self.behavior_models:
            return self.behavior_models[task].predict(observation)
        else:
            # Use default controller for unknown tasks
            return self.default_controller(observation)

    def transfer_learning(self, source_task, target_task):
        # Transfer knowledge from source task to target task
        source_model = self.behavior_models[source_task]
        target_model = self.initialize_model(target_task)

        # Fine-tune target model using source model weights
        target_model.transfer_weights(
            source_model,
            learning_rate=0.001
        )

        # Adapt to target task using few examples
        for experience in self.get_target_task_experiences(target_task, 50):
            target_model.update(
                experience['observation'],
                experience['action']
            )

        self.behavior_models[target_task] = target_model
```

## Learning Outcomes

By the end of this week, students should be able to:

1. **Implement computer vision systems** - Design and implement object detection, semantic segmentation, and 3D perception systems for robotic applications.

2. **Fuse multi-sensor data** - Integrate data from cameras, IMUs, odometry, and other sensors using Kalman filters and other fusion techniques.

3. **Design intelligent control systems** - Create adaptive and learning-based controllers that enable robots to improve their performance over time.

4. **Apply model predictive control** - Implement MPC systems that use learned dynamics models for optimal trajectory planning and control.

5. **Develop online learning capabilities** - Create systems that enable robots to learn from experience and adapt their behavior in real-time.

---

# Week 10: Reinforcement Learning for Robot Control

## Introduction

Reinforcement Learning (RL) has emerged as a powerful paradigm for developing adaptive and intelligent robot control systems. This week explores how RL algorithms can be applied to teach humanoid robots complex behaviors, from basic locomotion to sophisticated manipulation tasks. We examine various RL approaches, their implementation in robotic systems, and the challenges of applying these techniques to real-world robot control problems.

## Foundations of Reinforcement Learning for Robotics

Reinforcement learning provides a framework for learning optimal behaviors through interaction with the environment, making it particularly well-suited for robotic applications where explicit programming of all possible scenarios is infeasible.

### RL Framework for Robotics

The RL framework in robotics consists of:

- **Agent**: The robot learning to perform tasks
- **Environment**: The physical or simulated world where the robot operates
- **State**: Robot's current configuration and environmental information
- **Action**: Control commands sent to the robot's actuators
- **Reward**: Feedback signal indicating task success or failure
- **Policy**: Strategy that maps states to actions

```
Pseudocode: Basic RL Framework for Robotics
class RobotRLAgent:
    def __init__(self, robot_env, policy_network, learning_rate=0.001):
        self.env = robot_env
        self.policy_network = policy_network
        self.learning_rate = learning_rate
        self.optimizer = AdamOptimizer(learning_rate)
        self.replay_buffer = ReplayBuffer(max_size=100000)
        self.exploration_noise = OrnsteinUhlenbeckProcess()

    def train_step(self, state, action, reward, next_state, done):
        # Store experience in replay buffer
        self.replay_buffer.add(state, action, reward, next_state, done)

        # Sample batch from replay buffer
        batch = self.replay_buffer.sample(batch_size=32)

        # Update policy network
        with tf.GradientTape() as tape:
            # Compute predicted actions
            predicted_actions = self.policy_network(batch.states)

            # Compute loss (negative expected return)
            loss = self.compute_policy_loss(batch, predicted_actions)

        # Apply gradients
        gradients = tape.gradient(loss, self.policy_network.trainable_variables)
        self.optimizer.apply_gradients(
            zip(gradients, self.policy_network.trainable_variables)
        )

        return loss

    def select_action(self, state, explore=True):
        # Get action from policy network
        action = self.policy_network.predict(state)

        if explore:
            # Add exploration noise
            noise = self.exploration_noise.sample()
            action = action + noise

        # Ensure action is within bounds
        action = np.clip(action, self.env.action_space.low, self.env.action_space.high)

        return action

    def compute_policy_loss(self, batch, predicted_actions):
        # Compute policy gradient loss
        # This is a simplified version - actual implementation depends on specific algorithm
        advantages = self.compute_advantages(batch.rewards, batch.values)
        log_probs = self.compute_log_probs(predicted_actions, batch.actions)

        policy_loss = -tf.reduce_mean(advantages * log_probs)
        return policy_loss
```

### Reward Function Design

Designing effective reward functions is critical for successful RL in robotics:

```
Pseudocode: Reward Function Design
class RewardFunctionDesigner:
    def __init__(self):
        self.components = {}
        self.weights = {}
        self.normalization_factors = {}

    def design_locomotion_reward(self):
        # Design reward function for bipedal locomotion
        def reward_function(state, action, next_state, info):
            reward = 0.0

            # Forward progress reward
            forward_velocity = next_state['base_linear_velocity'][0]  # x-direction
            target_velocity = 1.0  # m/s
            velocity_reward = max(0, forward_velocity)  # Only reward forward motion
            reward += velocity_reward * 2.0

            # Balance reward - maintain upright posture
            base_orientation = next_state['base_orientation']  # quaternion
            upright_reward = self.calculate_upright_reward(base_orientation)
            reward += upright_reward * 3.0

            # Energy efficiency reward - penalize excessive joint torques
            joint_torques = next_state['joint_torques']
            energy_penalty = -np.mean(np.abs(joint_torques)) * 0.1
            reward += energy_penalty

            # Smoothness reward - penalize jerky movements
            action_smoothness = -np.sum(np.abs(action)) * 0.05
            reward += action_smoothness

            # Safety reward - penalize dangerous configurations
            if self.is_unsafe_configuration(next_state):
                reward += -10.0  # Large penalty for unsafe states

            # Normalize reward
            reward = np.clip(reward, -10.0, 10.0)

            return reward

        return reward_function

    def design_manipulation_reward(self):
        # Design reward function for manipulation tasks
        def reward_function(state, action, next_state, info):
            reward = 0.0

            # Distance to target reward
            target_pos = info['target_position']
            end_effector_pos = next_state['end_effector_position']
            distance = np.linalg.norm(target_pos - end_effector_pos)
            distance_reward = -distance  # Negative distance (closer is better)
            reward += distance_reward * 5.0

            # Grasping reward
            if self.is_grasping_object(next_state):
                reward += 10.0
                # Bonus for stable grasp
                grasp_stability = self.calculate_grasp_stability(next_state)
                reward += grasp_stability * 2.0

            # Avoid collisions
            if self.is_in_collision(next_state):
                reward += -5.0

            # Joint limit penalty
            joint_angles = next_state['joint_positions']
            joint_limit_penalty = self.calculate_joint_limit_penalty(joint_angles)
            reward += joint_limit_penalty * -1.0

            return reward

        return reward_function

    def calculate_upright_reward(self, orientation_quat):
        # Calculate how upright the robot is (1.0 = perfectly upright, -1.0 = upside down)
        # Convert quaternion to rotation matrix and extract z-axis
        rotation_matrix = self.quaternion_to_rotation_matrix(orientation_quat)
        world_up = np.array([0, 0, 1])
        robot_up = rotation_matrix[:, 2]  # z-axis of robot frame

        dot_product = np.dot(world_up, robot_up)
        return max(-1.0, min(1.0, dot_product))  # Clamp between -1 and 1
```

## Deep Reinforcement Learning Algorithms

Deep RL algorithms combine neural networks with reinforcement learning to handle high-dimensional state and action spaces common in robotics.

### Deep Deterministic Policy Gradient (DDPG)

DDPG is suitable for continuous control tasks like robot joint control:

```
Pseudocode: DDPG Implementation
class DDPGAgent:
    def __init__(self, state_dim, action_dim, action_bound):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.action_bound = action_bound

        # Actor network (policy)
        self.actor = self.create_actor_network()
        self.target_actor = self.create_actor_network()

        # Critic network (value function)
        self.critic = self.create_critic_network()
        self.target_critic = self.create_critic_network()

        # Initialize target networks with same weights as main networks
        self.target_actor.set_weights(self.actor.get_weights())
        self.target_critic.set_weights(self.critic.get_weights())

        self.replay_buffer = ReplayBuffer(max_size=100000)
        self.noise_process = OrnsteinUhlenbeckProcess(size=action_dim)

        # Hyperparameters
        self.gamma = 0.99  # Discount factor
        self.tau = 0.005   # Target network update rate
        self.learning_rate = 0.001

    def create_actor_network(self):
        # Actor network: state -> action
        model = Sequential([
            Dense(400, activation='relu', input_shape=(self.state_dim,)),
            Dense(300, activation='relu'),
            Dense(self.action_dim, activation='tanh')  # Output in [-1, 1]
        ])

        # Scale output to action bounds
        def scale_action(action):
            return action * self.action_bound

        model.add(Lambda(scale_action))
        model.compile(optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def create_critic_network(self):
        # Critic network: (state, action) -> Q-value
        state_input = Input(shape=(self.state_dim,))
        action_input = Input(shape=(self.action_dim,))

        # Process state
        state_hidden = Dense(400, activation='relu')(state_input)
        state_hidden = Dense(300)(state_hidden)

        # Process action
        action_hidden = Dense(300)(action_input)

        # Combine state and action
        combined = Add()([state_hidden, action_hidden])
        combined = Activation('relu')(combined)

        # Output Q-value
        q_value = Dense(1)(combined)

        model = Model(inputs=[state_input, action_input], outputs=q_value)
        model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss='mse')
        return model

    def update_networks(self):
        if len(self.replay_buffer) < 64:  # Batch size
            return

        # Sample batch from replay buffer
        batch = self.replay_buffer.sample(64)
        states, actions, rewards, next_states, dones = batch

        # Update critic network
        with tf.GradientTape() as tape:
            # Get target Q-values from target networks
            next_actions = self.target_actor(next_states)
            target_q_values = self.target_critic([next_states, next_actions])
            target_q_values = rewards + (1 - dones) * self.gamma * target_q_values

            # Current Q-values
            current_q_values = self.critic([states, actions])

            # Critic loss
            critic_loss = tf.reduce_mean(tf.square(target_q_values - current_q_values))

        # Apply critic gradients
        critic_gradients = tape.gradient(critic_loss, self.critic.trainable_variables)
        self.critic.optimizer.apply_gradients(
            zip(critic_gradients, self.critic.trainable_variables)
        )

        # Update actor network (policy gradient)
        with tf.GradientTape() as tape:
            # Get actions from current policy
            current_actions = self.actor(states)

            # Get Q-values for these actions
            q_values = self.critic([states, current_actions])

            # Actor loss (maximize Q-values)
            actor_loss = -tf.reduce_mean(q_values)

        # Apply actor gradients
        actor_gradients = tape.gradient(actor_loss, self.actor.trainable_variables)
        self.actor.optimizer.apply_gradients(
            zip(actor_gradients, self.actor.trainable_variables)
        )

        # Update target networks (soft update)
        self.update_target_networks()

    def update_target_networks(self):
        # Soft update target networks
        actor_weights = self.actor.get_weights()
        target_actor_weights = self.target_actor.get_weights()
        for i in range(len(actor_weights)):
            target_actor_weights[i] = (
                self.tau * actor_weights[i] + (1 - self.tau) * target_actor_weights[i]
            )
        self.target_actor.set_weights(target_actor_weights)

        critic_weights = self.critic.get_weights()
        target_critic_weights = self.target_critic.get_weights()
        for i in range(len(critic_weights)):
            target_critic_weights[i] = (
                self.tau * critic_weights[i] + (1 - self.tau) * target_critic_weights[i]
            )
        self.target_critic.set_weights(target_critic_weights)
```

### Twin Delayed DDPG (TD3)

TD3 addresses overestimation bias in DDPG:

```
Pseudocode: TD3 Implementation
class TD3Agent:
    def __init__(self, state_dim, action_dim, action_bound):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.action_bound = action_bound

        # Actor network (single)
        self.actor = self.create_actor_network()
        self.target_actor = self.create_actor_network()

        # Two critic networks (twin critics)
        self.critic1 = self.create_critic_network()
        self.critic2 = self.create_critic_network()
        self.target_critic1 = self.create_critic_network()
        self.target_critic2 = self.create_critic_network()

        # Initialize target networks
        self.target_actor.set_weights(self.actor.get_weights())
        self.target_critic1.set_weights(self.critic1.get_weights())
        self.target_critic2.set_weights(self.critic2.get_weights())

        self.replay_buffer = ReplayBuffer(max_size=100000)
        self.noise_std = 0.1
        self.target_policy_noise_std = 0.2
        self.target_policy_noise_clip = 0.5

        self.gamma = 0.99
        self.tau = 0.005
        self.policy_delay = 2  # Update policy every 2 critic updates
        self.update_counter = 0

    def update_networks(self):
        if len(self.replay_buffer) < 100:  # Minimum batch size
            return

        # Sample batch from replay buffer
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(100)

        # Add noise to target actions for smoothing
        target_actions = self.target_actor(next_states)
        noise = tf.random.normal(shape=target_actions.shape, stddev=self.target_policy_noise_std)
        noise = tf.clip_by_value(noise, -self.target_policy_noise_clip, self.target_policy_noise_clip)
        noisy_target_actions = tf.clip_by_value(
            target_actions + noise,
            -self.action_bound,
            self.action_bound
        )

        # Compute target Q-values using minimum of twin critics
        target_q1 = self.target_critic1([next_states, noisy_target_actions])
        target_q2 = self.target_critic2([next_states, noisy_target_actions])
        target_q = rewards + (1 - dones) * self.gamma * tf.minimum(target_q1, target_q2)

        # Update critics
        with tf.GradientTape(persistent=True) as tape:
            current_q1 = self.critic1([states, actions])
            current_q2 = self.critic2([states, actions])

            critic1_loss = tf.reduce_mean(tf.square(target_q - current_q1))
            critic2_loss = tf.reduce_mean(tf.square(target_q - current_q2))

        # Apply critic gradients
        critic1_grads = tape.gradient(critic1_loss, self.critic1.trainable_variables)
        critic2_grads = tape.gradient(critic2_loss, self.critic2.trainable_variables)

        self.critic1.optimizer.apply_gradients(
            zip(critic1_grads, self.critic1.trainable_variables)
        )
        self.critic2.optimizer.apply_gradients(
            zip(critic2_grads, self.critic2.trainable_variables)
        )

        # Update actor (delayed)
        self.update_counter += 1
        if self.update_counter % self.policy_delay == 0:
            with tf.GradientTape() as tape:
                current_actions = self.actor(states)
                actor_q = self.critic1([states, current_actions])
                actor_loss = -tf.reduce_mean(actor_q)

            actor_grads = tape.gradient(actor_loss, self.actor.trainable_variables)
            self.actor.optimizer.apply_gradients(
                zip(actor_grads, self.actor.trainable_variables)
            )

        # Update target networks
        self.update_target_networks()
```

### Soft Actor-Critic (SAC)

SAC maximizes both expected reward and entropy for better exploration:

```
Pseudocode: SAC Implementation
class SACAgent:
    def __init__(self, state_dim, action_dim, action_bound):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.action_bound = action_bound

        # Actor network (stochastic policy)
        self.actor = self.create_actor_network()

        # Two Q-networks (twin Q-learning)
        self.q_network1 = self.create_q_network()
        self.q_network2 = self.create_q_network()
        self.target_q_network1 = self.create_q_network()
        self.target_q_network2 = self.create_q_network()

        # Temperature parameter (entropy regularization)
        self.log_alpha = tf.Variable(0.0, trainable=True)  # log of alpha
        self.alpha_optimizer = Adam(learning_rate=3e-4)

        # Initialize target networks
        self.target_q_network1.set_weights(self.q_network1.get_weights())
        self.target_q_network2.set_weights(self.q_network2.get_weights())

        self.replay_buffer = ReplayBuffer(max_size=100000)
        self.target_entropy = -action_dim  # Target entropy for automatic alpha tuning

        self.gamma = 0.99
        self.tau = 0.005

    def create_actor_network(self):
        # Stochastic actor that outputs mean and std of Gaussian policy
        state_input = Input(shape=(self.state_dim,))

        hidden = Dense(256, activation='relu')(state_input)
        hidden = Dense(256, activation='relu')(hidden)

        # Output mean and log_std for each action dimension
        mean_output = Dense(self.action_dim, activation='tanh')(hidden)
        log_std_output = Dense(self.action_dim, activation='tanh')(hidden)

        # Scale log_std to reasonable range
        log_std_output = tf.clip_by_value(log_std_output, -20, 2)

        # Reparameterization trick for sampling
        def sample_action(inputs):
            mean, log_std = inputs
            std = tf.exp(log_std)
            noise = tf.random.normal(shape=tf.shape(mean))
            raw_action = mean + std * noise
            # Apply tanh to bound actions
            bounded_action = tf.tanh(raw_action)
            return bounded_action

        action_output = Lambda(sample_action)([mean_output, log_std_output])

        model = Model(inputs=state_input, outputs=[mean_output, log_std_output, action_output])
        return model

    def update_networks(self):
        if len(self.replay_buffer) < 256:  # Batch size
            return

        # Sample batch from replay buffer
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(256)

        # Update Q-networks
        with tf.GradientTape(persistent=True) as tape:
            # Get next state actions and log probabilities
            next_means, next_log_stds, next_actions = self.actor(next_states)
            next_log_probs = self.gaussian_log_prob(next_means, next_log_stds, next_actions)

            # Compute target Q-values
            next_q1 = self.target_q_network1(next_states)
            next_q2 = self.target_q_network2(next_states)
            next_q_min = tf.minimum(next_q1, next_q2)
            target_q = rewards + (1 - dones) * self.gamma * (
                next_q_min - tf.exp(self.log_alpha) * next_log_probs
            )

            # Current Q-values
            current_q1 = self.q_network1(states)
            current_q2 = self.q_network2(states)

            # Q-network losses
            q1_loss = tf.reduce_mean(tf.square(target_q - current_q1))
            q2_loss = tf.reduce_mean(tf.square(target_q - current_q2))

        # Apply Q-network gradients
        q1_grads = tape.gradient(q1_loss, self.q_network1.trainable_variables)
        q2_grads = tape.gradient(q2_loss, self.q_network2.trainable_variables)

        self.q_network1.optimizer.apply_gradients(
            zip(q1_grads, self.q_network1.trainable_variables)
        )
        self.q_network2.optimizer.apply_gradients(
            zip(q2_grads, self.q_network2.trainable_variables)
        )

        # Update actor network
        with tf.GradientTape() as tape:
            means, log_stds, sampled_actions = self.actor(states)
            log_probs = self.gaussian_log_prob(means, log_stds, sampled_actions)

            # Q-values for current actions
            q1_values = self.q_network1(states)
            q2_values = self.q_network2(states)
            min_q_values = tf.minimum(q1_values, q2_values)

            # Actor loss (maximize Q-value and entropy)
            actor_loss = tf.reduce_mean(
                tf.exp(self.log_alpha) * log_probs - min_q_values
            )

        actor_grads = tape.gradient(actor_loss, self.actor.trainable_variables)
        self.actor.optimizer.apply_gradients(
            zip(actor_grads, self.actor.trainable_variables)
        )

        # Update temperature parameter (alpha)
        with tf.GradientTape() as tape:
            means, log_stds, sampled_actions = self.actor(states)
            log_probs = self.gaussian_log_prob(means, log_stds, sampled_actions)

            # Temperature loss (match target entropy)
            alpha_loss = -tf.reduce_mean(
                self.log_alpha * (log_probs + self.target_entropy)
            )

        alpha_grads = tape.gradient(alpha_loss, [self.log_alpha])
        self.alpha_optimizer.apply_gradients(
            zip(alpha_grads, [self.log_alpha])
        )

        # Update target networks
        self.update_target_networks()

    def gaussian_log_prob(self, mean, log_std, action):
        # Compute log probability of action under Gaussian distribution
        std = tf.exp(log_std)
        var = std ** 2
        log_prob = -0.5 * ((action - mean) ** 2) / var - 0.5 * tf.math.log(2 * np.pi * var)
        return tf.reduce_sum(log_prob, axis=1, keepdims=True)
```

## Simulation-to-Real Transfer

Transferring policies learned in simulation to real robots is a major challenge in robotics RL.

### Domain Randomization

Domain randomization helps policies generalize across different environments:

```
Pseudocode: Domain Randomization System
class DomainRandomization:
    def __init__(self):
        self.randomization_ranges = {
            'robot_dynamics': {
                'mass_multiplier': (0.8, 1.2),
                'friction_coefficient': (0.1, 0.9),
                'joint_damping': (0.01, 0.1),
                'actuator_delay': (0.0, 0.02)
            },
            'environment': {
                'gravity': (9.5, 10.1),
                'ground_friction': (0.4, 0.8),
                'lighting_intensity': (0.5, 2.0),
                'texture_roughness': (0.0, 1.0)
            },
            'sensors': {
                'imu_noise': (0.001, 0.01),
                'camera_noise': (0.001, 0.005),
                'delay': (0.0, 0.01)
            }
        }

    def randomize_environment(self, env):
        # Randomize robot dynamics
        mass_multiplier = np.random.uniform(
            self.randomization_ranges['robot_dynamics']['mass_multiplier'][0],
            self.randomization_ranges['robot_dynamics']['mass_multiplier'][1]
        )
        env.robot.set_mass_multiplier(mass_multiplier)

        friction = np.random.uniform(
            self.randomization_ranges['robot_dynamics']['friction_coefficient'][0],
            self.randomization_ranges['robot_dynamics']['friction_coefficient'][1]
        )
        env.robot.set_friction_coefficient(friction)

        # Randomize environment properties
        gravity = np.random.uniform(
            self.randomization_ranges['environment']['gravity'][0],
            self.randomization_ranges['environment']['gravity'][1]
        )
        env.set_gravity(gravity)

        # Randomize sensor properties
        imu_noise = np.random.uniform(
            self.randomization_ranges['sensors']['imu_noise'][0],
            self.randomization_ranges['sensors']['imu_noise'][1]
        )
        env.robot.set_imu_noise(imu_noise)

    def curriculum_randomization(self, training_step, max_steps):
        # Gradually increase randomization as training progresses
        progress = training_step / max_steps
        randomization_factor = min(progress * 2, 1.0)  # Increase up to 2x range

        for param, (min_val, max_val) in self.randomization_ranges['robot_dynamics'].items():
            range_size = (max_val - min_val) * randomization_factor
            center = (max_val + min_val) / 2
            new_min = center - range_size / 2
            new_max = center + range_size / 2
            self.randomization_ranges['robot_dynamics'][param] = (new_min, new_max)
```

### System Identification and Model Adaptation

Adapting simulation models to better match real robot behavior:

```
Pseudocode: System Identification
class SystemIdentifier:
    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.param_optimizer = ParameterOptimizer()
        self.simulator = PhysicsSimulator()
        self.real_data_buffer = DataBuffer(max_size=10000)

    def identify_robot_parameters(self, excitation_signal):
        # Apply excitation signal to real robot and collect data
        real_responses = self.excite_robot(excitation_signal)

        # Optimize simulation parameters to match real responses
        optimized_params = self.param_optimizer.optimize(
            target_data=real_responses,
            simulation_model=self.simulator,
            initial_params=self.robot_model.get_parameters()
        )

        # Update robot model with identified parameters
        self.robot_model.update_parameters(optimized_params)

        return optimized_params

    def excite_robot(self, signal):
        # Apply known excitation signal to robot joints
        responses = []

        for step, command in enumerate(signal):
            # Send command to robot
            self.robot_model.send_command(command)

            # Record response
            state = self.robot_model.get_state()
            responses.append({
                'time': step * self.dt,
                'position': state['position'],
                'velocity': state['velocity'],
                'torque': state['torque'],
                'command': command
            })

        return responses

    def adaptive_model_learning(self, real_experience):
        # Update simulation model based on real-world experience
        for episode in real_experience:
            # Extract system behavior from real data
            real_behavior = self.extract_behavior(episode)

            # Compare with simulation predictions
            sim_behavior = self.simulator.predict(episode.initial_state, episode.actions)

            # Compute behavior mismatch
            mismatch = self.compute_behavior_mismatch(real_behavior, sim_behavior)

            # Update model parameters to reduce mismatch
            updated_params = self.update_model_parameters(mismatch)
            self.simulator.update_parameters(updated_params)
```

## Learning Outcomes

By the end of this week, students should be able to:

1. **Design RL frameworks for robotics** - Create reinforcement learning systems specifically tailored for robotic control tasks with appropriate state, action, and reward definitions.

2. **Implement advanced RL algorithms** - Apply DDPG, TD3, and SAC algorithms to continuous control problems in humanoid robotics.

3. **Create effective reward functions** - Design reward functions that promote desired behaviors while avoiding local optima and unsafe configurations.

4. **Address sim-to-real transfer challenges** - Implement domain randomization and system identification techniques to improve policy transfer from simulation to reality.

5. **Evaluate and improve RL policies** - Assess policy performance, identify failure modes, and implement strategies for continuous improvement.

---