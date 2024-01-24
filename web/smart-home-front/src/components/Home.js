import React, {useEffect, useState} from 'react';
import './Devices.css';
import { Navigation } from './Navigation';
import io from "socket.io-client";

export function Home() {
    const [showAlarm, setShowAlarm] = useState(false);

    useEffect(() => {
        const socket = io('http://localhost:8000');

        socket.on('connect', () => {
            console.log('Connected to server');
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });

        socket.on('alarm', (msg) => {
            const message = msg.message
            console.log(message);
            setShowAlarm(message);
        });
        return () => {
            socket.disconnect();
        };
    }, []);


    return (
    <div>
        <Navigation  showAlarm={showAlarm}></Navigation>
    </div>
  );
}
