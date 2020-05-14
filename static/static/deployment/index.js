// MIT Aleksi Pirttimaa 2019

function deveuiutility(eui) {
	// input AABBCCDDEEFF
	// return aa-bb-ff-cc-dd-ee-ff
	return eui.toLowerCase().replace(/(.{2})/g,"$1-").slice(0, -1);
}
// const examplesensoreui = 'a8-17-58-ff-fe-03-0f-53';

document.addEventListener("DOMContentLoaded", function() {
	var sdb = new sensordb();
	sdb.connect('pan0153.panoulu.net', '8888');

	var sensors = [];
	// sensors is an array of all known sensors with the last values from the server
	//const examplesensor = {
	//	battery: 3.663,
	//	co2: 432,
	//	humidity: 27,
	//	id: "a8-17-58-ff-fe-03-0f-da",
	//	lastSeen: "2019-07-12T11:57:04.781158392Z",
	//	light: 95,
	//	location: "SM-1602",
	//	pir: "na",
	//	serial: "1",
	//	temperature: 22.2
	//}

	var options = {
	  valueNames: ['serial', 'location', 'id', 'battery', 'lastSeen', 'temperature', 'humidity', 'light', 'pir', 'co2']
	};

	var sensorsList = new List('sensors-list', options, sensors);

	// remove example sensor
	document.getElementsByClassName('sensor')[0].style.display = 'none';


	sensorDeployment.getSensors().then(function(res) {
		const installedSensors = res.data;
		installedSensors.forEach(function(sensor) {
			const id = deveuiutility(sensor.id);
			sdb.getValues(id).then(function(res) {
				delete sensor.lat;
				delete sensor.lon;
				sensor.id = id;
				const combined = {...sensor, ...res};
				sensors.push(combined);
				sensorsList.add(combined);
				if (sensors.length == installedSensors.length) {
					document.getElementById('spinner').style.display = 'none';
				}
			});
		});
		console.log("sensor data is at window.sensors for your convenience");
	});
});
