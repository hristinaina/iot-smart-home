
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
            // Handle the received data as needed
            this.setState((prevState) => {
                const { data } = prevState;
                const deviceName = message.name;
                const value = message.value;

                const updatedData = data.map((device) =>
                    device.name == deviceName
                        ? {
                            ...device,
                            value: value,
                        }
                        : device
                );

                return {
                    data: updatedData,
                };
            });
        });
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
                                <p className='device-text'><b>Value: </b>{device.value}</p>
                            </div>
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
};
