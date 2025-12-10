# Data Model: Physical AI & Humanoid Robotics Book

**Feature**: Physical AI & Humanoid Robotics Book
**Date**: 2025-12-08
**Model Version**: 1.0

## Overview

This data model represents the conceptual structure of the Physical AI & Humanoid Robotics Book. Since this is an educational book rather than a software application, the "data model" represents the conceptual entities and their relationships that will be taught throughout the four modules.

## Core Entities

### 1. Module
Represents a major section of the book with focused learning objectives.

**Attributes**:
- moduleId: String (e.g., "module-1-ros2", "module-2-digital-twin")
- title: String (e.g., "The Robotic Nervous System")
- description: String (brief overview of module focus)
- learningObjectives: Array[String] (specific outcomes students should achieve)
- duration: Number (in weeks)
- prerequisites: Array[String] (required knowledge from previous modules)

**Validation Rules**:
- moduleId must follow the format "module-[number]-[topic]"
- learningObjectives must be specific and measurable
- duration must be between 1-3 weeks
- prerequisites must reference valid previous modules

### 2. Week
Represents a weekly section within a module with specific learning content.

**Attributes**:
- weekId: String (e.g., "module-1-week-3")
- title: String (e.g., "ROS 2 Fundamentals")
- content: String (detailed content description)
- learningGoals: Array[String] (what students should learn this week)
- moduleRef: String (reference to parent module)
- weekNumber: Number (position within the module)

**Validation Rules**:
- weekId must be unique within the module
- weekNumber must be sequential starting from 1
- content must align with module's overall objectives

### 3. Concept
Represents a fundamental idea or principle taught in the book.

**Attributes**:
- conceptId: String (e.g., "ros2-node", "vla-system", "sim2real-transfer")
- name: String (e.g., "ROS 2 Node", "Vision-Language-Action System")
- definition: String (clear definition of the concept)
- category: String (e.g., "middleware", "perception", "control", "ai")
- relatedConcepts: Array[String] (other concepts this concept connects to)
- moduleOrigin: String (which module first introduces this concept)

**Validation Rules**:
- conceptId must be unique across the book
- category must be one of the predefined categories
- relatedConcepts must reference valid concepts

### 4. Diagram
Represents a visual element used to explain concepts.

**Attributes**:
- diagramId: String (e.g., "ros2-architecture-diagram")
- title: String (e.g., "ROS 2 Architecture Overview")
- type: String (e.g., "flowchart", "system-diagram", "sequence-diagram")
- description: String (what the diagram illustrates)
- conceptsIllustrated: Array[String] (which concepts this diagram helps explain)
- filePath: String (path to the diagram file in the repository)

**Validation Rules**:
- diagramId must be unique
- type must be one of the predefined types
- conceptsIllustrated must reference valid concepts

### 5. PseudoCodeExample
Represents a conceptual code example using pseudo-code.

**Attributes**:
- exampleId: String (e.g., "ros2-publisher-example")
- title: String (e.g., "Simple ROS 2 Publisher")
- languageStyle: String (e.g., "python-like", "algorithmic")
- purpose: String (what concept this example illustrates)
- code: String (the actual pseudo-code)
- relatedConcepts: Array[String] (concepts this example demonstrates)
- moduleRef: String (which module contains this example)

**Validation Rules**:
- exampleId must be unique
- code must be in proper pseudo-code format (not executable)
- relatedConcepts must reference valid concepts

### 6. Assessment
Represents an evaluation component to validate student understanding.

**Attributes**:
- assessmentId: String (e.g., "module-1-quiz", "capstone-project")
- title: String (e.g., "ROS 2 Communication Patterns Quiz")
- type: String (e.g., "quiz", "project", "conceptual-exercise")
- difficulty: String (e.g., "beginner", "intermediate", "advanced")
- objectives: Array[String] (what learning objectives this assesses)
- moduleRef: String (which module this assessment belongs to)

**Validation Rules**:
- assessmentId must be unique
- type must be one of the predefined types
- objectives must align with module's learning objectives

### 7. ReferenceSource
Represents an academic or technical source cited in the book.

**Attributes**:
- sourceId: String (e.g., "nvidia-isaac-paper-2023")
- type: String (e.g., "academic-paper", "documentation", "industry-report")
- title: String (full title of the source)
- authors: Array[String] (author names)
- publication: String (journal, conference, or publisher)
- publicationDate: String (YYYY-MM-DD format)
- url: String (URL if available)
- apaCitation: String (proper APA format citation)
- topicsCovered: Array[String] (which concepts/topics this source covers)

**Validation Rules**:
- sourceId must be unique
- type must be one of the predefined types
- apaCitation must follow APA format
- at least 60% of sources must be peer-reviewed (as per constitution)

## Entity Relationships

### Module ↔ Week
- One-to-Many: One module contains multiple weeks
- Module (1) → Week (0..n)
- Week must belong to exactly one module

### Module ↔ Concept
- Many-to-Many: A module can introduce multiple concepts; a concept can appear in multiple modules (for reinforcement)
- Module (0..n) ↔ Concept (0..n)
- Concepts are introduced in a specific module but may be referenced in later modules

### Week ↔ Concept
- Many-to-Many: A week covers multiple concepts; a concept may span multiple weeks
- Week (0..n) ↔ Concept (0..n)

### Concept ↔ Diagram
- Many-to-Many: A concept may be illustrated by multiple diagrams; a diagram may illustrate multiple concepts
- Concept (0..n) ↔ Diagram (0..n)

### Concept ↔ PseudoCodeExample
- Many-to-Many: A concept may be demonstrated by multiple examples; an example may demonstrate multiple concepts
- Concept (0..n) ↔ PseudoCodeExample (0..n)

### Module ↔ Assessment
- One-to-Many: One module contains multiple assessments
- Module (1) → Assessment (0..n)

### Assessment ↔ Concept
- Many-to-Many: An assessment may test multiple concepts; a concept may be tested by multiple assessments
- Assessment (0..n) ↔ Concept (0..n)

### Concept ↔ ReferenceSource
- Many-to-Many: A concept may be supported by multiple sources; a source may cover multiple concepts
- Concept (0..n) ↔ ReferenceSource (0..n)

## State Transitions (where applicable)

### Content Development State
- Concept states: [proposed, approved, in-development, reviewed, published]
- Module states: [planned, in-development, reviewed, published]
- Week states: [planned, in-development, reviewed, published]

### Review State
- All content items follow: [draft, peer-review, approved, published]

## Constraints

1. **Four-Module Limit**: Total modules must equal exactly 4 (as per constitution)
2. **Conceptual Focus**: All examples must be pseudo-code, not executable implementations
3. **Prerequisite Chain**: Later modules must build on concepts from earlier modules
4. **Citation Standard**: Minimum 60% peer-reviewed sources required
5. **Academic Rigor**: All content must follow Flesch-Kincaid Grade 10-12 standard
6. **No Duplication**: Content must not duplicate concepts from other modules unnecessarily
7. **Embodied Intelligence Focus**: All content must connect to physical robot systems

## Indexes

### Primary Indexes
- Module by moduleId
- Concept by conceptId
- Week by weekId
- ReferenceSource by sourceId

### Secondary Indexes
- Concepts by category
- Diagrams by type
- Assessments by type and difficulty
- ReferenceSources by type and publication date