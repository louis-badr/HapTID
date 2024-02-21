var port;
var data_array = [];

async function readFromMCU() {
    try {
        const reader = port.readable.getReader();
        while (true) {
            const { value, done } = await reader.read();
            if (done) {
                console.log("Reader done");
                reader.releaseLock();
                break;
            }
            console.log("Received from MCU:", new TextDecoder().decode(value));
        }
    } catch (error) {
        console.error("Error reading data from MCU:", error);
    }
}

async function getReader() {
    port = await navigator.serial.requestPort({});
    await port.open({ baudRate: 115200 });
    document.getElementById("serial_connect_button").innerHTML="CONNECTED";	
    readFromMCU();
}

function listSerial(){
    if (port) {
        console.log("Closing port: " + port);
        port.close();
        port = undefined;
        document.getElementById("serial_connect_button").innerHTML="CONNECT";
    }
    else {
        console.log("Look for Serial Ports")
        getReader();
    }
}

async function sendToMCU(valueToSend) {
    try {
        if (port && valueToSend !== "") {
            const writer = port.writable.getWriter();
            await writer.write(new TextEncoder().encode(valueToSend));
            console.log("Sent: " + valueToSend);
            writer.releaseLock();
        } else {
            console.log("Port not open or value to send is empty");
        }
    } catch (error) {
        console.error("Error sending data to MCU:", error);
    }
}

async function sendArrayToMCU() {
    try {
        if (port && data_array.length > 0) {
            for (let i = 0; i < data_array.length; i++) {
                await sendToMCU(data_array[i].toString());
                await new Promise(resolve => setTimeout(resolve, 10)); // Wait for a short time between sending each value
            }
        } else {
            console.log("Port not open or data array is empty");
        }
    } catch (error) {
        console.error("Error sending array to MCU:", error);
    }
}


