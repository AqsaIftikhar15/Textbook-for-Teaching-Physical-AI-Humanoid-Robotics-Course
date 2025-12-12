---
title: ROS 2 Fundamentals
sidebar_position: 2
description: Overview of ROS 2 middleware architecture
---

# Week 3: ROS 2 Fundamentals

## Introduction

ROS 2 (Robot Operating System 2) serves as the middleware layer that enables communication between different components of a robotic system, functioning as the "nervous system" of the robot. This week explores the fundamental concepts of ROS 2, including its architecture, communication patterns, and core components. Understanding ROS 2 is essential for developing modular, scalable, and maintainable robotic applications that can coordinate sensors, actuators, and computational processes effectively.

## ROS 2 Architecture and Middleware Design

ROS 2 implements a distributed computing framework that allows different software components to communicate seamlessly across multiple processes and machines. The architecture is built on the Data Distribution Service (DDS) standard, which provides a publish-subscribe communication model with quality-of-service (QoS) controls.

### Client Library Architecture

ROS 2 provides client libraries that wrap DDS functionality:

- **rclcpp**: C++ client library for performance-critical applications
- **rclpy**: Python client library for rapid prototyping and scripting
- **rclc**: C client library for embedded systems
- **rclnodejs**: JavaScript client library for web integration

The client libraries provide a consistent API across programming languages while maintaining the underlying DDS communication infrastructure.

### Node-Based Architecture

The fundamental unit of computation in ROS 2 is the node:

```
Pseudocode: Basic ROS 2 Node Structure
class RobotNode:
    def __init__(self, node_name):
        self.node = rclpy.create_node(node_name)
        self.publishers = {}
        self.subscribers = {}
        self.services = {}
        self.actions = {}

    def create_publisher(self, msg_type, topic_name, qos_profile):
        publisher = self.node.create_publisher(msg_type, topic_name, qos_profile)
        self.publishers[topic_name] = publisher
        return publisher

    def create_subscription(self, msg_type, topic_name, callback, qos_profile):
        subscriber = self.node.create_subscription(msg_type, topic_name, callback, qos_profile)
        self.subscribers[topic_name] = subscriber
        return subscriber

    def spin(self):
        rclpy.spin(self.node)

    def destroy_node(self):
        self.node.destroy_node()
```

### Communication Patterns

ROS 2 supports multiple communication patterns:

- **Publish-Subscribe**: Asynchronous one-to-many communication
- **Request-Response**: Synchronous client-server communication
- **Action-Based**: Asynchronous request-response with feedback and goal management

## Topics and Message Passing

Topics form the backbone of ROS 2's publish-subscribe communication model, enabling asynchronous data exchange between nodes.

### Topic Architecture

Topics are named channels through which nodes publish and subscribe to messages:

- **Publishers**: Nodes that send messages to topics
- **Subscribers**: Nodes that receive messages from topics
- **Message Types**: Strongly typed data structures defined in .msg files

```
Pseudocode: Topic Publisher Implementation
class SensorPublisher:
    def __init__(self):
        self.node = rclpy.create_node('sensor_publisher')
        self.publisher = self.node.create_publisher(
            sensor_msgs.msg.LaserScan,
            'laser_scan',
            10  // Queue size
        )
        self.timer = self.node.create_timer(0.1, self.publish_scan)

    def publish_scan(self):
        scan_msg = sensor_msgs.msg.LaserScan()
        scan_msg.header.stamp = self.node.get_clock().now().to_msg()
        scan_msg.header.frame_id = 'laser_frame'
        scan_msg.angle_min = -1.57  // -90 degrees
        scan_msg.angle_max = 1.57   // 90 degrees
        scan_msg.angle_increment = 0.01
        scan_msg.ranges = self.get_laser_data()

        self.publisher.publish(scan_msg)
```

### Quality of Service (QoS) Profiles

QoS profiles control the reliability and performance characteristics of topic communication:

- **Reliability**: Reliable (all messages delivered) vs Best Effort (no guarantee)
- **Durability**: Volatile (new subscribers don't receive old messages) vs Transient Local
- **History**: Keep All vs Keep Last N messages
- **Deadline**: Maximum time between message publications
- **Liveliness**: How to detect if a publisher is still active

```
Pseudocode: QoS Configuration
def configure_qos_profiles():
    # High-priority control commands
    control_qos = rclpy.qos.QoSProfile(
        reliability=rclpy.qos.ReliabilityPolicy.RELIABLE,
        durability=rclpy.qos.DurabilityPolicy.VOLATILE,
        history=rclpy.qos.HistoryPolicy.KEEP_LAST,
        depth=1  // Only keep the most recent command
    )

    # Sensor data (can tolerate some loss)
    sensor_qos = rclpy.qos.QoSProfile(
        reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
        durability=rclpy.qos.DurabilityPolicy.VOLATILE,
        history=rclpy.qos.HistoryPolicy.KEEP_ALL,
        depth=100  // Keep many sensor readings
    )

    return control_qos, sensor_qos
```

## Services and Request-Response Communication

Services provide synchronous request-response communication for operations that require immediate responses or acknowledgments.

### Service Architecture

Services follow a client-server pattern:

- **Service Server**: Provides functionality and responds to requests
- **Service Client**: Makes requests and waits for responses
- **Service Types**: Defined in .srv files with request and response structures

```
Pseudocode: Service Implementation
class NavigationService:
    def __init__(self):
        self.node = rclpy.create_node('navigation_service')
        self.service = self.node.create_service(
            nav_msgs.srv.NavigateToPose,
            'navigate_to_pose',
            self.handle_navigation_request
        )

    def handle_navigation_request(self, request, response):
        # Extract target pose from request
        target_pose = request.pose
        navigation_result = self.execute_navigation(target_pose)

        # Set response fields
        response.success = navigation_result.success
        response.message = navigation_result.message
        response.execution_time = navigation_result.execution_time

        return response

class NavigationClient:
    def __init__(self):
        self.node = rclpy.create_node('navigation_client')
        self.client = self.node.create_client(
            nav_msgs.srv.NavigateToPose,
            'navigate_to_pose'
        )

    def navigate_to_pose(self, target_pose):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.node.get_logger().info('Service not available, waiting...')

        request = nav_msgs.srv.NavigateToPose.Request()
        request.pose = target_pose

        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self.node, future)

        return future.result()
```

## Actions for Complex Task Management

Actions extend the request-response pattern to handle long-running operations with feedback and goal management.

### Action Architecture

Actions support complex operations that may take significant time to complete:

- **Goal**: Request to perform a specific task
- **Feedback**: Continuous updates during task execution
- **Result**: Final outcome when task completes
- **Goal States**: Active, Succeeded, Aborted, Canceled

```
Pseudocode: Action Server Implementation
class MoveRobotAction:
    def __init__(self):
        self.node = rclpy.create_node('move_robot_action')
        self.action_server = ActionServer(
            self.node,
            MoveRobot,
            'move_robot',
            self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

    def goal_callback(self, goal_request):
        # Validate goal request
        if self.is_goal_valid(goal_request):
            return GoalResponse.ACCEPT
        else:
            return GoalResponse.REJECT

    def execute_callback(self, goal_handle):
        feedback_msg = MoveRobot.Feedback()
        result = MoveRobot.Result()

        # Execute the movement
        for step in self.generate_movement_steps(goal_handle.request):
            # Check if goal was canceled
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.success = False
                return result

            # Execute movement step
            success = self.execute_movement_step(step)

            # Publish feedback
            feedback_msg.current_distance = self.get_current_distance()
            feedback_msg.progress_percentage = self.calculate_progress()
            goal_handle.publish_feedback(feedback_msg)

        # Set final result
        result.success = success
        goal_handle.succeed()
        return result
```

## URDF and Robot Description

URDF (Unified Robot Description Format) provides a standardized way to describe robot kinematics, dynamics, and visual properties.

### URDF Structure

URDF files define robot components using XML:

- **Links**: Rigid bodies with mass, inertia, and visual properties
- **Joints**: Connections between links with kinematic constraints
- **Materials**: Visual appearance properties
- **Gazebo Plugins**: Simulation-specific extensions

```
Pseudocode: URDF Processing
class URDFProcessor:
    def __init__(self, urdf_file_path):
        self.urdf_xml = self.load_urdf_file(urdf_file_path)
        self.links = self.parse_links(self.urdf_xml)
        self.joints = self.parse_joints(self.urdf_xml)
        self.materials = self.parse_materials(self.urdf_xml)

    def parse_links(self, urdf_xml):
        links = {}
        for link_element in urdf_xml.findall('link'):
            link = RobotLink()
            link.name = link_element.get('name')
            link.inertial = self.parse_inertial(link_element.find('inertial'))
            link.visual = self.parse_visual(link_element.find('visual'))
            link.collision = self.parse_collision(link_element.find('collision'))
            links[link.name] = link
        return links

    def parse_joints(self, urdf_xml):
        joints = {}
        for joint_element in urdf_xml.findall('joint'):
            joint = RobotJoint()
            joint.name = joint_element.get('name')
            joint.type = joint_element.get('type')
            joint.parent = joint_element.find('parent').get('link')
            joint.child = joint_element.find('child').get('link')
            joint.origin = self.parse_origin(joint_element.find('origin'))
            joint.limit = self.parse_limit(joint_element.find('limit'))
            joints[joint.name] = joint
        return joints

    def compute_forward_kinematics(self, joint_angles):
        # Compute transformation matrices for each joint
        transforms = {}
        for joint_name, joint in self.joints.items():
            joint_angle = joint_angles.get(joint_name, 0.0)
            transform = self.compute_joint_transform(joint, joint_angle)
            transforms[joint_name] = transform

        # Combine transforms to get end-effector pose
        return self.combine_transforms(transforms)
```

## Communication Patterns and Best Practices

Effective ROS 2 development requires understanding appropriate communication patterns for different use cases.

### Topic vs Service vs Action Selection

- **Use Topics for**: Sensor data streams, status updates, broadcast messages
- **Use Services for**: Quick operations that need immediate responses
- **Use Actions for**: Long-running tasks that provide feedback

### Design Patterns

- **Node Specialization**: Each node should have a single, well-defined responsibility
- **Message Standardization**: Use standard message types when possible
- **Namespace Organization**: Organize topics and services using namespaces
- **Error Handling**: Implement robust error handling and recovery mechanisms

```
Pseudocode: Node Design Pattern
class ModularNode:
    def __init__(self, node_name):
        self.node = rclpy.create_node(node_name)

        # Initialize components
        self.parameter_handler = ParameterHandler(self.node)
        self.diagnostics_publisher = self.create_diagnostics_publisher()
        self.heartbeat_timer = self.create_heartbeat_timer()

        # Initialize communication interfaces
        self.setup_publishers()
        self.setup_subscribers()
        self.setup_services()
        self.setup_actions()

    def setup_publishers(self):
        self.status_publisher = self.node.create_publisher(
            std_msgs.msg.String,
            'status',
            10
        )

    def setup_subscribers(self):
        self.command_subscriber = self.node.create_subscription(
            std_msgs.msg.String,
            'commands',
            self.command_callback,
            10
        )

    def command_callback(self, msg):
        try:
            # Process command
            result = self.process_command(msg.data)
            self.status_publisher.publish(std_msgs.msg.String(data=result))
        except Exception as e:
            self.node.get_logger().error(f'Command processing failed: {e}')
```

## Learning Outcomes

By the end of this week, students should be able to:

1. **Explain ROS 2 architecture** - Describe the node-based architecture, client libraries, and DDS middleware that underpin ROS 2 communication.

2. **Implement topic-based communication** - Create publishers and subscribers with appropriate QoS profiles for different types of data streams.

3. **Design service-based interactions** - Implement request-response communication patterns for operations requiring immediate responses.

4. **Create action-based workflows** - Develop long-running operations with feedback and goal management using the action interface.

5. **Parse and utilize URDF specifications** - Understand and process URDF files to extract robot kinematic and dynamic information for humanoid robot applications.

---