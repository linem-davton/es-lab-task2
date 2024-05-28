# Task Scheduling Backend


This repository contains the backend server for the Task Scheduling front-end. The backend is responsible for processing the logical model, running scheduling algorithms, and communicating with the frontend. It is built with FastAPI and provides a RESTful API for interaction with the [frontend](https://eslab2.pages.dev/).

## Table of Contents
- [Getting Started](#getting-started)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Input and Output Schemas](#input-and-output-formats)
- [Components](#components)
- [Contributing](#contributing)

## Getting Started

1. Clone the repository:
    git clone [https://github.com/linem-davton/graphdraw-eslab-backend.git

2. Navigate to the project directory:
    cd graphdraw-eslab-backend

3. Install dependencies:
    pip install -r requirements.txt

4. Start the development server:
   python3 src/backend.py

5. Access the API:
   The backend server will be running at http://localhost:8000.
  If everything is set up correctly, you should see the following message: {"Hello": "World"}

6. To access the API documentation, go to http://localhost:8000/docs.

7. Visit the frontend at [eslab2.pages.dev](https://eslab2.pages.dev/), and input the logical and platform model as defined in input schema to schedule tasks.

## Technologies Used

- [Python 3](https://www.python.org/about/gettingstarted/)
- [FastAPI](https://fastapi.tiangolo.com/learn/)
- [NetworkX](https://networkx.org/documentation/stable/tutorial.html)
- [Uvicorn](https://www.uvicorn.org/)

## Features
- **[RESTful](https://en.wikipedia.org/wiki/REST) API**: Provides endpoints for scheduling tasks and retrieving schedules.
- **Multiple Scheduling Algorithms**: Implements LDF and EDF scheduling algorithms for task scheduling.
- **Input Validation**: Ensures valid data format for processing.
- **[Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) (CORS)**: Enabled for specified origins.

## API Endpoints

- **POST /schedule_jobs**: Accepts a task graph in JSON format and returns the scheduled tasks using four different algorithms.
- **GET /get_jobs**: Endpoint for retrieving job schedules.
- **GET /**: Root endpoint to verify if the server is running.

Learn more about [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

## Input and Output Schemas

### API Input Schema for /schedule_jobs

The backend expects input in the following [JSON](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON) schema:


This JSON Schema defines the structure for the input JSON model used by the scheduling algorithms. It ensures the correct format and validation of the input data.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "application": {
      "type": "object",
      "properties": {
        "jobs": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "integer"
              },
              "wcet": {
                "type": "integer"
              },
              "mcet": {
                "type": "integer"
              },
              "deadline": {
                "type": "integer"
              }
            },
            "required": ["id", "wcet", "mcet", "deadline"]
          }
        },
        "messages": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "integer"
              },
              "sender": {
                "type": "integer"
              },
              "receiver": {
                "type": "integer"
              },
              "size": {
                "type": "integer"
              },
              "timetriggered": {
                "type": "integer"
              }
            },
            "required": ["id", "sender", "receiver", "size", "timetriggered"]
          }
        }
      },
      "required": ["jobs", "messages"]
    },
    "platform": {
      "type": "object",
      "properties": {
        "nodes": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "integer"
              },
              "type": {
                "type": "string"
              }
            },
            "required": ["id", "type"]
          }
        }
      },
      "required": ["nodes"]
    },
    "links": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer"
          },
          "start_node": {
            "type": "integer"
          },
          "end_node": {
            "type": "integer"
          },
          "link_delay": {
            "type": "integer"
          },
          "bandwidth": {
            "type": "integer"
          },
          "type": {
            "type": "string"
          }
        },
        "required": ["id", "start_node", "end_node", "link_delay", "bandwidth", "type"]
      }
    }
  },
  "required": ["application", "platform", "links"]
}
```
This schema defines the structure for the application and platform objects required by the scheduling algorithms. It ensures that:

- Jobs: Each job has an id, wcet (worst case execution time), mcet (mean case execution time), and deadline (all integers).
- Messages: Each message has an id, sender, receiver, size (all integers), and timetriggered (integer).
- Nodes: Each node has an id (integer) and type (string).
- Links: Each link has an id, start_node, end_node, link_delay, bandwidth (all integers), and type (string).
By adhering to this schema, you can validate the input JSON model before processing it with the scheduling algorithms.

### Output Schema for /schedule_jobs
This JSON Schema defines the structure for the output schedule generated by the scheduling algorithms. It ensures the correct format and validation of the output data.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "schedule": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "job_id": {
            "type": "integer"
          },
          "node_id": {
            "type": "integer"
          },
          "start_time": {
            "type": "integer"
          },
          "end_time": {
            "type": "integer"
          },
          "deadline": {
            "type": "integer"
          }
        },
        "required": ["job_id", "node_id", "start_time", "end_time", "deadline"]
      }
    }
  },
  "required": ["schedule"]
}
```
This schema defines the structure for the schedule object produced by the scheduling algorithms. It ensures that each scheduled item has:

- job_id: The identifier of the job, which can be a string or integer.
- node_id: The identifier of the node where the job is scheduled, which can be a string or integer.
- start_time: The time when the job starts execution.
- end_time: The time when the job finishes execution.
- deadline: The deadline by which the job must be completed.


## Components

- **backend.py**: Main entry point for the FastAPI backend server.
    - Handles API endpoints and routing.
    - Configures CORS middleware.
- **algorithms.py**: Contains the implementation of the scheduling algorithms (LDF, EDF).
    - ldf_algorithm: Implementation of the LDF scheduling algorithm.
    - edf_schedule: Implementation of the EDF scheduling algorithm.
    - ldf_singlecore: Implementation of the single-core LDF scheduling algorithm.
    - edf_singlecore: Implementation of the single-core EDF scheduling algorithm.
- **config.json**: Configuration file for backend settings.
- **requirements.txt**: File listing all the dependencies required for the project.

## Contributing
Contributions are welcome! Please follow these steps to contribute:

- Fork the repository.
- Create a new branch (git checkout -b feature/your-feature-name).
- Make your changes.
- Commit your changes (git commit -m 'Add some feature').
- Push to the branch (git push origin feature/your-feature-name).
- Create a new Pull Request.

## Resources and References
1. Github Backend Repository: [Task Scheduling Backend](https://github.com/linem-davton/es-lab-task2)
2. Github Frontend Repository: [Task Scheduling Frontend](https://github.com/linem-davton/graphdraw-frontend)
