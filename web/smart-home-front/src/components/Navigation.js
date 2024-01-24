import React, { useEffect, useRef, useState } from 'react';
import { Navbar, NavItem, NavLink } from 'reactstrap';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

export function Navigation({ showAlarm }) {
  const location = useLocation();
  const [blink, setBlink] = useState(false);
  const prevPathnameRef = useRef(location.pathname);

  useEffect(() => {
    // Check if the route has changed before triggering a reload
    if (prevPathnameRef.current !== location.pathname) {
      console.log('Route changed:', location.pathname);
      window.location.reload();
    }

    // Update the previous pathname for the next render
    prevPathnameRef.current = location.pathname;
  }, [location.pathname]);

  useEffect(() => {
    // Toggle the blink effect based on showAlarm prop
    if (showAlarm) {
      const intervalId = setInterval(() => {
        setBlink((prevBlink) => !prevBlink);
      }, 500); // Toggle every 500 milliseconds

      return () => clearInterval(intervalId);
    } else {
      setBlink(false);
    }
  }, [showAlarm]);

  return (
    <header>
      <Navbar className="navbar">
        <ul>
          <span className="logo">Smart Home</span>
          <NavItem>
            <NavLink
              tag={Link}
              className={`text-light ${location.pathname === '/home' ? 'active' : ''}`}
              to="/home"
            >
              Home
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink
              tag={Link}
              className={`text-light ${location.pathname === '/devices/PI1' ? 'active' : ''}`}
              to="/devices/PI1"
            >
              PI1
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink
              tag={Link}
              className={`text-light ${location.pathname === '/devices/PI2' ? 'active' : ''}`}
              to="/devices/PI2"
            >
              PI2
            </NavLink>
          </NavItem>
          <NavItem>
            <NavLink
              tag={Link}
              className={`text-light ${location.pathname === '/devices/PI3' ? 'active' : ''}`}
              to="/devices/PI3"
            >
              PI3
            </NavLink>
          </NavItem>
          {showAlarm && (
            <>
              <span id="alarm">
                ALARM
              </span>
              <img src='/images/alarm.png' id='alarmImg' className={blink ? 'blink' : ''} />
            </>
          )}

        </ul>
      </Navbar>
    </header>
  );
}
