var numPoints = 7;
var updateDelayMs = 2000;
var transitionDuration = 500;
var lastDateTime = null;

document.body.insertAdjacentHTML('afterbegin', '<div class="c3" style="display: none;"><div class="c3-axis-y-label"/><div class="c3-axis-y2-label"/></div>');
var elem,
    style;
elem = document.querySelector('.c3-axis-y-label');
style = getComputedStyle(elem);
var axisYLabelColor = style.fill;
elem = document.querySelector('.c3-axis-y2-label');
style = getComputedStyle(elem);
var axisY2LabelColor = style.fill;
document.querySelector('.c3').remove();

var initialJson = {};
var xmlHttp = new XMLHttpRequest();
xmlHttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200)
    {
        initialJson = JSON.parse(this.responseText);
        lastDateTime = initialJson.graph.data.x.sort()[initialJson.graph.data.x.length - 1];
    }
}
xmlHttp.open("GET", "/hydrometer_chart?pageload=1", false);
xmlHttp.send(null);

var chart = c3.generate({
    bindto: '#hydrometer-chart',
    data: {
        x: 'x',
        json: initialJson.graph.data,
        xFormat: '%Y-%m-%d %H:%M:%S',
        axes: {
            Humidity: 'y2'
        },
        colors: {
            Temperature: axisYLabelColor,
            Humidity: axisY2LabelColor
        }
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%H:%M:%S'
            }
        },
        y: {
            label: '°C'
        },
        y2: {
            show: true,
            label: '% Humidity'
        }
    },
    grid: initialJson.graph.grid
});

setInterval(function () {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200)
        {
            var jsonResponse = JSON.parse(this.responseText);
            if (jsonResponse.graph.data.x.length > 0) {
                lastDateTime = jsonResponse.graph.data.x.sort()[jsonResponse.graph.data.x.length - 1];
                chart.flow({
                    json: jsonResponse.graph.data,
                    duration: transitionDuration,
                });
		chart.grid = jsonResponse.graph.grid;

                var button = document.querySelector('.power-button button');
                button.className = jsonResponse.status.button.className;
                button.textContent = jsonResponse.status.button.textContent;
                document.querySelector('.temperature-label').textContent = jsonResponse.status.tempLabel;
                document.querySelector('.humidity-label').textContent = jsonResponse.status.humLabel;
            }
        }
    }
    if (lastDateTime != null) {
        xmlHttp.open("GET", "/hydrometer_chart?last=" + lastDateTime, true); // true for asynchronous
    }
    else {
        xmlHttp.open("GET", "/hydrometer_chart", false);
    }
    xmlHttp.send(null);
}, updateDelayMs);
