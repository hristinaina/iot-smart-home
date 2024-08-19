# Smart Home
Project for course Internet of things (IOT).

## Team members
- [Uroš Stanić](https://github.com/ili0n)
- [Hristina Adamović](https://github.com/hristinaina)
  
## Project Description

This project involves the use of sensors installed on three Raspberry Pis (or simulations if physical devices are unavailable) to monitor a smart home system.
The application provides real-time status updates for each component in the house. It also triggers an alert/alarm if any component detects suspicious behavior.
The photo below illustrates the house plan and the and the system implemented in this project:

![image](https://github.com/user-attachments/assets/f5ba61fd-b2b6-4940-aad2-764315164a64)

## Technologies Used

The sensors send data to a backend server using MQTT, and the data is stored in an InfluxDB database.
The backend is built with Python Flask, and the frontend is developed using React and Grafana for data visualization.

- [InfluxDB](https://www.influxdata.com/): Time-series database for handling metrics and events.
- [Docker](https://www.docker.com/): Platform for developing, shipping, and running applications in containers.
- [Grafana](https://grafana.com/) Tool used for data visualization.
- [React](https://reactjs.org/): JavaScript library for building user interfaces.
- [Material Design](https://material.io/): Design system for creating visually appealing and consistent UIs.

## Project Structure

- `backend/`: Contains the Python Flask application.
- `frontend/`: Contains the React application.
- the rest of the root folder is related to the work with sensors
- `sensors/`: Contains scripts for the sensors on the Raspberry Pis.
- `simulation/`: Contains scripts for the simulated sensors if there are no Raspberry Pis.
- `settings#.json`: Configuration files for sensors where you can specify whether simulation is required.

## Setup Instructions

### Sensors

1. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```
2. Navigate to the `infrastructure/` directory and build docker containers:
   ```sh
   docker-compose up
   ```
3. Run the PI#.py scripts:
   ```sh
   python PI#.py
   ```
   
### Backend

4. Run the Flask server by navigating to the 'backend' directory and running the next command:
   ```sh
   python server.py
   ```
### Frontend

5. Navigate to the `frontend/` directory. Install the required npm packages:
   ```sh
   npm install
   ```
6. Start the React application:
   ```sh
   npm start
   ```
   
### Keep your home safe and stay informed with our intelligent monitoring system! 🏠
