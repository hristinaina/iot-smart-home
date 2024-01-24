
import { Component } from 'react';
import './Devices.css';
import { Navigation } from './Navigation';
import DeviceService from '../services/DeviceService'
import io from 'socket.io-client';

export class Devices extends Component {
    connected = false;

    constructor(props) {
        super(props);
        this.state = {
            data: [],
        };
        this.connecting = false; //change to true if you want to use this
        this.pi =this.extractPIFromUrl();
        this.socket = null;
        this.showAlarm = true;
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

        this.socket = io('http://localhost:8000');

        this.socket.on('connect', () => {
            console.log('Connected to server');
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });        

        // Listen for messages from the server
        this.socket.on('data/'+this.pi, (msg) => {
            const message = msg.message
            console.log(message);
            let updated = this.updateDHT(message);
            if (updated) return;
            updated = this.updateGyro(message);
            if (updated) return;
            // other
            this.setState((prevState) => {
                const { data } = prevState;
                const deviceName = message.name;
                const value = message.value;
                
                const updatedData = data.map((device) =>
                    device.name == deviceName
                        ? {
                            ...device,
                            value: value,
                            measurement: message.measurement
                        }
                        : device
                );
                return {
                    data: updatedData,
                };
            });
        });
    }

    updateDHT(message){
        let updated = false;
        this.setState((prevState) => {
            const { data } = prevState;
            const deviceName = message.name;
            const value = message.value;

            if(message.measurement == "Temperature"){
                updated = true;
                const updatedData = data.map((device) =>
                    device.name == deviceName || (device.name == "GLCD" && deviceName == "GDHT")
                        ? {
                            ...device,
                            valueT: value,
                        }
                        : device
                );
                return {
                    data: updatedData,
                };
            }
            else if(message.measurement == "Humidity"){
                updated = true;
                const updatedData = data.map((device) =>
                    device.name == deviceName || (device.name == "GLCD" && deviceName == "GDHT")
                        ? {
                            ...device,
                            valueH: value,
                        }
                        : device
                );
                return {
                    data: updatedData,
                };
            }
        })
        return updated;
    }

    updateGyro(message){
        let updated = false;
        this.setState((prevState) => {
            const { data } = prevState;
            const deviceName = message.name;
            const value = message.value;
            if(message.measurement == "Acceleration" && message.axis == "x"){
                updated = true;
                const updatedData = data.map((device) =>
                    device.name == deviceName
                        ? {
                            ...device,
                            valueAX: value,
                        }
                        : device
                );
                return {
                    data: updatedData,
                };
            }
            else if(message.measurement == "Acceleration" && message.axis == "y"){
                updated = true;
                const updatedData = data.map((device) =>
                    device.name == deviceName
                        ? {
                            ...device,
                            valueAY: value,
                        }
                        : device
                );
                return {
                    data: updatedData,
                };
            }
            else if(message.measurement == "Acceleration" && message.axis == "z"){
                updated = true;
                const updatedData = data.map((device) =>
                    device.name == deviceName
                        ? {
                            ...device,
                            valueAZ: value,
                        }
                        : device
                );
                return {
                    data: updatedData,
                };
            }
            else if(message.measurement == "Gyroscope"  && message.axis == "x"){
                updated = true;
                const updatedData = data.map((device) =>
                    device.name == deviceName
                        ? {
                            ...device,
                            valueGX: value,
                        }
                        : device
                );
                return {
                    data: updatedData,
                };
            } else if(message.measurement == "Gyroscope"  && message.axis == "y"){
                updated = true;
                const updatedData = data.map((device) =>
                    device.name == deviceName
                        ? {
                            ...device,
                            valueGY: value,
                        }
                        : device
                );
                return {
                    data: updatedData,
                };
            } else if(message.measurement == "Gyroscope"  && message.axis == "z"){
                updated = true;
                const updatedData = data.map((device) =>
                    device.name == deviceName
                        ? {
                            ...device,
                            valueGZ: value,
                        }
                        : device
                );
                return {
                    data: updatedData,
                };
            }
        })
        return updated;
    }

    componentWillUnmount() {
        this.socket.disconnect();
    }

    extractPIFromUrl() {
        const parts = window.location.href.split('/');
        return parts[parts.length - 1];
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

    render() {
        const { data } = this.state;
        const connecting = this.connecting;
        const showAlarm = this.showAlarm;
        return (
            <div>
                <Navigation showAlarm={showAlarm}/>
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
                                {device.type.slice(-3) == "DHT" && (<p className='device-text'><b>Temperature: </b>{device.valueT}°C</p>)}
                                {device.type.slice(-3) == "DHT" && (<p className='device-text'><b>Humidity: </b>{device.valueH}%</p>)}
                                {device.name == "GLCD" && (<p className='device-text'><b>Temperature: </b>{device.valueT}°C</p>)}
                                {device.name == "GLCD" && (<p className='device-text'><b>Humidity: </b>{device.valueH}%</p>)}
                                {device.name == "GSG" && (<p className='device-text'><b>Acceleration: </b>{device.valueAX}, {device.valueAY}, {device.valueAZ}</p>)}
                                {device.name == "GSG" && (<p className='device-text'><b>Gyroscope: </b>{device.valueGX}, {device.valueGY}, {device.valueGZ}</p>)}
                                {device.type.slice(-3) != "DHT" && device.name != "GSG" && device.name != "GLCD" && (<p className='device-text'><b>{device.measurement}: </b>{device.value}</p>)}
                                {device.name == "BRGB" && (<p className='device-text'><button className='card-button'>Change Light</button></p>)}
                                {device.name == "DMS" && (<p className='device-text'><button className='card-button'>Enter pin</button></p>)}
                            </div>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};
