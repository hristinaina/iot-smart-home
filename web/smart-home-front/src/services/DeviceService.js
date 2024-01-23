const devices = [
    {
      id: 2,
      name: 'Bakina lampa',
      type: 'Lamp',
      status: 'Offline',
    },
    {
      id: 3,
      name: 'Masina Sladja',
      type: 'Washing Machine',
      status: 'Online',
    },
    {
      id: 4,
      name: 'Prsk prsk',
      type: 'Sprinkler',
      status: 'Online',
    },
    {
      id: 5,
      name: 'Samo kes',
      type: 'Solar Panel',
      status: 'Offline',
    },
    {
      id: 6,
      name: 'Masina Masa',
      type: 'Washing machine',
      status: 'Online',
    },
    {
      id: 7,
      name: 'Curaljka',
      type: 'Sprinkler',
      status: 'Online',
    },
    {
      id: 8,
      name: 'Zvezda Severnjaca',
      type: 'Lamp',
      status: 'Offline',
    },
    {
      id: 1,
      name: 'Panelcici',
      type: 'Solar Panel',
      status: 'Online',
    }
  ];

class DeviceService {

    async getDevices(realEstateId) {
        // try {
        //     const response = await fetch('http://localhost:8081/api/devices/' + realEstateId);
        //     const data = await response.json();
        //     return data;
        //   } catch (error) {
        //     console.error('Error fetching data:', error);
        //     throw error;
        //   }
        return devices;
    }
}

export default new DeviceService();

