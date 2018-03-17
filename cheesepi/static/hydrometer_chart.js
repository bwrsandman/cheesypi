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
        lastDateTime = jsonResponse.x.sort()[jsonResponse.x.length - 1];
    }
}
xmlHttp.open("GET", "/hydrometer_chart?pageload=1", false);
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
    }
});

setInterval(function () {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200)
        {
            var jsonResponse = JSON.parse(this.responseText);
            if (jsonResponse.x.length > 0) {
                lastDateTime = jsonResponse.x.sort()[jsonResponse.x.length - 1];
                chart.flow({
                    json: JSON.parse(this.responseText),
                    duration: transitionDuration,
                });
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
