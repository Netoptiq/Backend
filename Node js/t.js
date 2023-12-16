const WebSocket = require('ws');

const socket = new WebSocket('ws://localhost:8000/ws/log/');

socket.on('open', (event) => {
    console.log('WebSocket connection opened:', event);
});

socket.on('message', (message) => {
    console.log('WebSocket message received:', message);
});

socket.on('close', (event) => {
    console.log('WebSocket connection closed:', event);
});
