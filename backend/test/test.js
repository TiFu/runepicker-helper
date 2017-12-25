let io = require('socket.io-client');

const socket = io('http://localhost:8765/runeprediction');

let response = (data) => console.log(data);

function errorCB(success, msg) {
	console.log("Success: " + success, msg)
}
socket.on('connect', function(){
	console.log("Connected!");
	socket.emit("startPrediction", {"champion_id": 22, "lane": "MARKSMEN"}, errorCB);
});

socket.on('primaryStyles', function(data){
	console.log(data);
	socket.emit("selectPrimaryStyle", 8400, errorCB)
});

socket.on("subStyles", function(data) {
	console.log(data)
	socket.emit("selectSubStyle", 8100, errorCB)
})

socket.on("primaryRunes", function(data) {
	console.log(data)
	socket.close()
})

socket.on("secondaryRunes", function(data) {
	console.log(data)
})

socket.on('disconnect', function(){
	console.log("disconnected");
});
