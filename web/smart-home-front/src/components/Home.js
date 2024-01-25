import React, {useEffect, useState} from 'react';
import './Devices.css';
import { Navigation } from './Navigation';
import io from "socket.io-client";

export function Home() {
    const [showAlarm, setShowAlarm] = useState(localStorage.getItem('alarm') == "true");

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
            localStorage.setItem("alarm", message);
        });
        return () => {
            socket.disconnect();
        };
    }, []);


    return (
        <div >
            <Navigation showAlarm={showAlarm}></Navigation>

                <iframe width = "100%" height = "900vh"
                    src="http://localhost:3000/public-dashboards/b7417158c7d5433e91984caeb220d594"
                     frameBorder="0"></iframe>

        </div>

    )
        ;
}
