# Docker CPU Resource Management Demo

This project demonstrates Docker container CPU resource management and limitations using a simple Flask application. It includes a CPU stress test feature that allows you to observe how Docker enforces CPU constraints on containers.

## Features

- Docker container with configurable CPU limits
- Flask REST API for controlling CPU stress tests
- Real-time monitoring capabilities
- Resource usage constraints (50% CPU limit, 25% CPU reservation)
- Simple web interface for interaction

## Prerequisites

- Docker
- Docker Compose
- Git (for cloning the repository)

## Project Structure

```
docker-cpu-demo/
|
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile           # Docker image definition
├── requirements.txt     # Python dependencies
├── app.py              # Flask application
├── README.md           # Documentation
├── .gitignore         # Git ignore rules
└── LICENSE            # MIT License
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DevOpsHandbook/docker-cpu-demo.git
cd docker-cpu-demo
```

2. Build and start the container:
```bash
docker-compose up --build
```

## Usage

The application exposes several HTTP endpoints for controlling the CPU stress test:

### API Endpoints

1. Check Server Status
```bash
curl http://localhost:5000/
```

2. Start CPU Stress Test
```bash
curl http://localhost:5000/start
```

3. Check Current Status
```bash
curl http://localhost:5000/status
```

4. Stop CPU Stress Test
```bash
curl http://localhost:5000/stop
```

### Monitoring Resource Usage

To monitor the container's CPU usage:
```bash
docker stats
```

You should observe that the CPU usage never exceeds 50% of a single core, demonstrating Docker's resource constraints in action.

## Configuration

### CPU Limits

The CPU limits are configured in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '0.50'    # Maximum CPU usage (50%)
    reservations:
      cpus: '0.25'    # Reserved CPU (25%)
```

You can modify these values to experiment with different CPU limitations.

## Technical Details

### Resource Management

- The container is limited to using 50% of a CPU core
- A minimum of 25% CPU is reserved for the container
- Docker enforces these limits using cgroups

### Implementation

- Built with Python 3.9 and Flask
- Uses threading for CPU stress simulation
- RESTful API design
- JSON responses for all endpoints

## Response Examples

### Server Status
```json
{
    "status": "Server is running",
    "instructions": {
        "start_test": "GET /start",
        "stop_test": "GET /stop",
        "check_status": "GET /status"
    }
}
```

### Start CPU Test
```json
{
    "message": "CPU stress test started",
    "status": "running",
    "start_time": "2024-11-25 10:30:00"
}
```

### Status Check
```json
{
    "stress_test_active": true,
    "current_time": "2024-11-25 10:30:15",
    "running_duration_seconds": 15.5,
    "start_time": "2024-11-25 10:30:00"
}
```

## Troubleshooting

1. If the container fails to start, ensure no other services are using port 5000
2. If CPU limits aren't working, ensure your Docker version supports resource constraints
3. For Windows users, ensure Docker Desktop is properly configured with WSL 2

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation
- Docker resource management documentation
- Python threading library documentation

## Future Improvements

- [ ] Add graphical CPU usage visualization
- [ ] Include memory stress testing
- [ ] Add more detailed monitoring metrics
- [ ] Implement WebSocket for real-time updates
- [ ] Add configuration file for easy parameter adjustment

## Contact

Gautam Makwana- [@Gautam0210](https://github.com/Gautam0210)

Project Link: [docker-cpu-demo](https://github.com/DevOpsHandbook/docker-cpu-demo.git)