var numPoints = 7;
var updateDelayMs = 2000;
var transitionDuration = 500;

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
    }
}
xmlHttp.open("GET", "/hydrometer_chart?last=" + numPoints, false);
xmlHttp.send(null);

var chart = c3.generate({
    bindto: '#hydrometer-chart',
    data: {
        x: 'x',
        json: initialJson,
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
                format: '%Y-%m-%d %H:%M:%S'
            }
        },
        y: {
            label: '°C'
        },
        y2: {
            show: true,
            label: '% Humidity'
        }
    }
});

setInterval(function () {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200)
        {
            var jsonResponse = JSON.parse(this.responseText);
            chart.flow({
                json: JSON.parse(this.responseText),
                duration: transitionDuration,
            });
        }
    }
    xmlHttp.open("GET", "/hydrometer_chart", true); // true for asynchronous
    xmlHttp.send(null);
}, updateDelayMs);
