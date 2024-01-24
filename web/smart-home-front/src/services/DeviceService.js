class DeviceService {

    async getDevices(PI) {
      try {
        console.log(PI);
        const response = await fetch(`http://localhost:8000/api/devices/${PI}`);
        const data = await response.json();
        return data;
      } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
      }
    }

    async updateRGBLight(color) {
      try {
        const response = await fetch(`http://localhost:8000/api/updateRGB/${color}`);
        const data = await response.json();
        return data;
      } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
      }
    }

    async getAlarmTime() {
      try {
        const response = await fetch(`http://localhost:8000/api/getAlarmClock`);
        const data = await response.json();
        return data;
      } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
      }
    }

    async updateAlarmTime(time) {
      try {
          const response = await fetch('http://localhost:8000/api/setAlarmClock', {
              method: 'PUT',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ time }),
          });
  
          const data = await response.json();
          return data;
      } catch (error) {
          console.error('Error fetching data:', error);
          throw error;
      }
  }
  
}

export default new DeviceService();

