var activeMotor = "1";
var currentTab = "sine";

var sineVolumeSlider = document.getElementById("sineVolumeSlider");
var sineFrequencySlider = document.getElementById("sineFrequencySlider");
var noiseVolumeSlider = document.getElementById("noiseVolumeSlider");
var clicksVolumeSlider = document.getElementById("clicksVolumeSlider");
var clicksNumberSlider = document.getElementById("clicksNumberSlider");
var clicksSpacingSlider = document.getElementById("clicksSpacingSlider");

var sineVolumeOutput = document.getElementById("sineVolumeOutput");
var sineFrequencyOutput = document.getElementById("sineFrequencyOutput");
var noiseVolumeOutput = document.getElementById("noiseVolumeOutput");
var clicksVolumeOutput = document.getElementById("clicksVolumeOutput");
var clicksNumberOutput = document.getElementById("clicksNumberOutput");
var clicksSpacingOutput = document.getElementById("clicksSpacingOutput");

sineVolumeOutput.innerHTML = sineVolumeSlider.value;
sineFrequencyOutput.innerHTML = sineFrequencySlider.value;
noiseVolumeOutput.innerHTML = noiseVolumeSlider.value;
clicksVolumeOutput.innerHTML = clicksVolumeSlider.value;
clicksNumberOutput.innerHTML = clicksNumberSlider.value;
clicksSpacingOutput.innerHTML = clicksSpacingSlider.value;

sineVolumeSlider.oninput = function() {
    sineVolumeOutput.innerHTML = this.value;
}

sineFrequencySlider.oninput = function() {
    sineFrequencyOutput.innerHTML = this.value;
}

noiseVolumeSlider.oninput = function() {
    noiseVolumeOutput.innerHTML = this.value;
}

clicksVolumeSlider.oninput = function() {
    clicksVolumeOutput.innerHTML = this.value;
}

clicksNumberSlider.oninput = function() {
    clicksNumberOutput.innerHTML = this.value;
}

clicksSpacingSlider.oninput = function() {
    clicksSpacingOutput.innerHTML = this.value;
}

var array_input_field = document.getElementById("array_input_field");

function openTab(evt, tabName) {
    currentTab = tabName;
    var i, x, tablinks;
    x = document.getElementsByClassName("tab");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function selectMotor(evt, motorNo) {
    var i, motortabs;
    motortabs = document.getElementsByClassName("motortab");
    for (i = 0; i < motortabs.length; i++) {
        motortabs[i].className = motortabs[i].className.replace(" active", "");
    }
    evt.currentTarget.className += " active";
    activeMotor = motorNo;
}

async function loadArray() {
    // generate the array
    data_array = [];
    if (currentTab == "sine"){
        var frequency = sineFrequencySlider.value;
        var samples_per_period = sample_rate/frequency;
        for (var i = 0; i < samples_per_period; i++){
            data_array[i] = Math.round((Math.sin(2*Math.PI*i/samples_per_period) * pwm_max / 2 + pwm_max / 2) * sineVolumeSlider.value / 100);
        }
    }
    else if (currentTab == "noise"){
        data_array = whitenoise_data.slice();
        // multiply by volume
        for (var i = 0; i < data_array.length; i++){
            data_array[i] = Math.round(data_array[i] * noiseVolumeSlider.value / 100);
        }
    }
    else if (currentTab == "clicks"){
        var clicks_spacing_length = Math.round(clicksSpacingSlider.value * sample_rate / 1000);
        for (var i = 0; i < clicksNumberSlider.value - 1; i++){
            for (var j = 0; j < click_length; j++){
                data_array.push(pwm_max * clicksVolumeSlider.value / 100);
            }
            for (var j = 0; j < clicks_spacing_length; j++){
                data_array.push(0);
            }
        }
        for (var j = 0; j < click_length; j++){
            data_array.push(pwm_max * clicksVolumeSlider.value / 100);
        }
        // add one second of silence
        for (var j = 0; j < sample_rate; j++){
            data_array.push(0);
        }
    }
    else if (currentTab == "custom"){
        data_array = array_input_field.value.split(",").map(Number);
    }

    // send the array to the microcontroller
    await sendToMCU("L");
    await sendArrayToMCU();
    await sendToMCU(-1);

    // update plotly data (only x and y)
    Plotly.restyle("myPlot", "y", [data_array]);
    Plotly.restyle("myPlot", "x", [Array.from({length: data_array.length}, (v, k) => k*1000/16000)]);
    // auto resize plotly
    Plotly.Plots.resize("myPlot");
}

document.getElementById("load_button").addEventListener("click", async function() {
    await loadArray();
    console.log("Loaded array of length " + data_array.length);
    console.log("Loaded array: " + data_array);
});
document.getElementById("start_button").addEventListener("click", async function() {
    await sendToMCU(activeMotor);
    console.log("Started motor " + activeMotor);
});
document.getElementById("stop_button").addEventListener("click", async function() {
    await sendToMCU("S");
    console.log("Stopped all motors");
});