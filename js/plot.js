// Define Data
const data = [{
    y: [],
    // sample rate is 16kHz, show in ms
    x: [],
    mode: 'lines',
    name: 'hv',
    line: {shape: 'hv',
    color: '#F4EFDC'},
    type: 'scatter',
}];

// Define Layout
const layout = {
    
    // add padding to the left and right of the plot
    margin: {
        l: 100,
        r: 100,
        b: 50,
        t: 50,
        pad: 20
    },
    yaxis: {
        title: 'Amplitude',
        autorange: true,
        titlefont: {color: '#F4EFDC'},
        tickfont: {color: '#2E45ED'},
        range: [0, pwm_max],
        // visible: false,
        showgrid: false,
        zeroline: false,
    },
    xaxis: {
        title: 'Time (ms)',
        autorange: true,
        titlefont: {color: '#F4EFDC'},
        tickfont: {color: '#2E45ED'},
        zeroline: false,
        showgrid: false,
        // linecolor: '#2E45ED',
        // visible: false,
    },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
};

// Display using Plotly
Plotly.newPlot("myPlot", data, layout);