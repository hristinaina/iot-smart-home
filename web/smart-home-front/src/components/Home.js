import React from 'react';
import './Devices.css';
import { Navigation } from './Navigation';

export function Home() {
  const showAlarm = true;


  return (
    <div>
        <Navigation  showAlarm={showAlarm}></Navigation>
    </div>
  );
}
