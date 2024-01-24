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
}

export default new DeviceService();

