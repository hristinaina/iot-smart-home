
import { Component } from 'react';
import './Devices.css';
import { Navigation } from './Navigation';
import DeviceService from '../services/DeviceService'
import mqtt from 'mqtt';

export class Devices extends Component {
    connected = false;

    constructor(props) {
        super(props);
        this.state = {
            data: [],
        };
        this.mqttClient = null;
        this.connecting = false; //change to true if you want to use this
        this.pi =this.extractPIFromUrl();
    }

    async fetchData(){
        try {
            const result = await DeviceService.getDevices(this.pi);
            this.setState({ data: result });
        } catch (error) {
            console.log("Error fetching data from the server");
            console.log(error);
        }
    }

    async componentDidMount() {
        this.fetchData();

        try {
            if (!this.connected) {  // to avoid reconnecting because this renders 2 times !!!
                this.connected = true;
                this.mqttClient = mqtt.connect('ws://localhost:9001/mqtt', {
                    clientId: "react-front-iot-devices",
                    clean: false,
                    keepalive: 60
                });
                console.log("Connected to mqtt broker");
                // Subscribe to the MQTT topic for device status
                this.mqttClient.on('connect', () => {
                    this.mqttClient.subscribe('data/+');
                });

                // Handle incoming MQTT messages
                this.mqttClient.on('message', (topic, message) => {
                    this.handleMqttMessage(topic, message);
                });
            }
        } catch (error) {
            console.log("Error trying to connect to broker");
            console.log(error);
        }
    }

    componentWillUnmount() {
        // Disconnect MQTT client on component unmount
        if (this.mqttClient) {
            this.mqttClient.end();
        }
    }

    extractPIFromUrl() {
        const parts = window.location.href.split('/');
        return parts[parts.length - 1];
    }

    // Handle incoming MQTT messages
    handleMqttMessage(topic, message) {
        console.log("handle message");
        this.setState((prevState) => {
            const { data } = prevState;
            const deviceId = parseInt(this.extractDeviceNameFromTopic(topic));
            const status = message.toString();

            // // Update the IsOnline status based on the received MQTT message
            // const updatedData = data.map((device) =>
            //     device.Id == deviceId
            //         ? {
            //             ...device,
            //             Status: status === 'online',
            //         }
            //         : device
            // );

            // return {
            //     data: updatedData,
            // };
        });
    }

    //todo navigate to appropriate page
    handleClick(device) {
        if (device.Type === 'Ambient Sensor')
            window.location.assign("/ambient-sensor/" + device.Id)
        else if (device.Type === 'Air conditioner')
            window.location.assign("/air-conditioner/" + device.Id)
        else if (device.Type === 'Washing machine')
            window.location.assign("/lamp/" + device.Id)
        else if (device.Type === 'Lamp')
            window.location.assign("/lamp/" + device.Id)
        else if (device.Type === 'Vehicle gate')
            window.location.assign("/lamp/" + device.Id)
        else if (device.Type === 'Sprinkler')
            window.location.assign("/lamp/" + device.Id)
        else if (device.Type === 'Solar panel')
            window.location.assign("/sp/" + device.Id)
        else if (device.Type === 'Battery storage')
            window.location.assign("/hb/" + device.Id)
        else if (device.Type === 'Electric vehicle charger')
            window.location.assign("/lamp/" + device.Id)
    }

    extractDeviceNameFromTopic(topic) {
        const parts = topic.split('/');
        return parts[parts.length - 1];
    }

    render() {
        const { data } = this.state;
        const connecting = this.connecting;
        return (
            <div>
                <Navigation />
                <div id="tools">
                </div>
                <DevicesList devices={data}  onClick={this.handleClick} connecting={connecting}/>
            </div>
        )
    }
}

const DevicesList = ({ devices, onClick, connecting }) => {
    const chunkSize = 5; // Number of items per row

    const chunkArray = (arr, size) => {
        return Array.from({ length: Math.ceil(arr.length / size) }, (v, i) =>
            arr.slice(i * size, i * size + size)
        );
    };

    const rows = chunkArray(devices, chunkSize);

    return (
        <div id='devices-container'>
            {rows.map((row, rowIndex) => (
                <div key={rowIndex} className='device-row'>
                    {row.map((device, index) => (
                        <div key={index} className='device-card' onClick={() => onClick(device)}>
                            <div className='device-info'>
                                <p className='device-title'>{device.name}</p>
                                <p className='device-text'>{device.type}</p>
                                {device.simulated && (<p className='device-text'><b>Simulation:</b> True</p>)}
                                {!device.simulated && (<p className='device-text'><b>Simulation:</b> False</p>)}
                            </div>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};
