// Base URL logic: If hosted on Heroku, format differently
var host = window.location.hostname;
if (host.includes("heroku")) {
    var base_url = "https://" + host;
} else {
    var base_url = "http://127.0.0.1:5000";
}

function init() {
    endpoint = base_url + "/api";
    Plotly.d3.json(endpoint, function(error, response) {
        if (error) return console.warn(error);
        // Fill the x and y arrays as a function of the selected dataset
        var datas = response[0]["What size and which brand are more profitable"];
        var max_price = [];
        var count_sneakers = [];
        var category_max = [];
        var size_max = [];
        var category_max = [];
        var size_max = [];
        var jordan_count = [];
        var yeezy_count = [];
        var jordan_max = [];
        var yeezy_max = [];
        datas['max_price'].forEach(dict => {
            max_price.push(Number(Object.keys(dict)[0]));
            category_max.push(Object.values(dict)[0][0]);
            size_max.push(Object.values(dict)[0][1]);
        });
        datas['count_sneakers'].forEach(dict => {
            count_sneakers.push(Number(Object.keys(dict)[0]));
        });
        for (var i = 0; i < max_price.length/2; i++) {
            jordan_max.push(max_price[i]);
        }
        for (var i = max_price.length/2; i < max_price.length; i++) {
            yeezy_max.push(max_price[i]);
        }
        for (var i = 0; i < count_sneakers.length/2; i++) {
            jordan_count.push(count_sneakers[i]);
        }
        for (var i = count_sneakers.length/2; i < count_sneakers.length; i++) {
            yeezy_count.push(count_sneakers[i]);
        }
        var trace1 = {
            x: size_max,
            y: jordan_max,
            type: 'scatter',
            mode: 'lines',
            line: {color: 'rgb(222,45,38)'},
            name : 'Max Prices of Jordan',
            marker:{
                color: 'rgb(222,45,38)'
            }
        };
        var trace2 = {
            x: size_max,
            y: yeezy_max,
            type: 'scatter',
            mode: 'lines',
            line: {color: 'rgb(55, 83, 109)'},
            name : 'Max Prices of Yeezy',
            marker:{
                color: 'rgb(55, 83, 109)'
            }
        };
        var trace3 = {
            x: size_max,
            y: jordan_count,
            type: 'scatter',
            mode: 'lines',
            line: {color: 'rgba(222,45,38, 0.5)', dash: 'dot', width: 4},
            name : '# of Jordan Sales'
        };
        var trace4 = {
            x: size_max,
            y: yeezy_count,
            type: 'scatter',
            mode: 'lines',
            line: {color: 'rgba(55, 83, 109, 0.5)', dash: 'dot', width: 4},
            name : '# of Yeezy Sales'
        };
        var trace5 = {
            x: size_max,
            y: count_sneakers,
            type: 'bar',
            name : 'Total Sales',
            marker:{color: 'rgba(204,204,204,1)'}
        };
        data = [trace1, trace2, trace3, trace4, trace5];
        var layout = {
            title: "What size and which brand are more profitable",
            xaxis: {
                title: {text: 'Size'},
            }
        };
        var PLOT = document.getElementById("plot");
        Plotly.plot(PLOT, data, layout);
    })
};

function updatePlotly(data, layout) {
  var PLOT = document.getElementById("plot");
  // Note the extra brackets around 'newx' and 'newy'
  Plotly.newPlot(PLOT, data, layout);
}

function getData(dataset) {
    // Initialize empty arrays to contain our axes
    var x = [];
    var y = [];
    endpoint = base_url + "/api";
    Plotly.d3.json(endpoint, function(error, response) {
        if (error) return console.warn(error);
        switch (dataset) {
        case "dataset2":
            var datas = response[0]["What size and which brand are more profitable"];
            var max_price = [];
            var count_sneakers = [];
            var category_max = [];
            var size_max = [];
            var category_max = [];
            var size_max = [];
            var jordan_count = [];
            var yeezy_count = [];
            var jordan_max = [];
            var yeezy_max = [];
            datas['max_price'].forEach(dict => {
                max_price.push(Number(Object.keys(dict)[0]));
                category_max.push(Object.values(dict)[0][0]);
                size_max.push(Object.values(dict)[0][1]);
            });
            datas['count_sneakers'].forEach(dict => {
                count_sneakers.push(Number(Object.keys(dict)[0]));
            });
            for (var i = 0; i < max_price.length/2; i++) {
                jordan_max.push(max_price[i]);
            }
            for (var i = max_price.length/2; i < max_price.length; i++) {
                yeezy_max.push(max_price[i]);
            }
            for (var i = 0; i < count_sneakers.length/2; i++) {
                jordan_count.push(count_sneakers[i]);
            }
            for (var i = count_sneakers.length/2; i < count_sneakers.length; i++) {
                yeezy_count.push(count_sneakers[i]);
            }
            var trace1 = {
                x: size_max,
                y: jordan_max,
                type: 'scatter',
                mode: 'lines',
                line: {color: 'rgb(222,45,38)'},
                name : 'Max Prices of Jordan',
                marker:{
                    color: 'rgb(222,45,38)'
                }
            };
            var trace2 = {
                x: size_max,
                y: yeezy_max,
                type: 'scatter',
                mode: 'lines',
                line: {color: 'rgb(55, 83, 109)'},
                name : 'Max Prices of Yeezy',
                marker:{
                    color: 'rgb(55, 83, 109)'
                }
            };
            var trace3 = {
                x: size_max,
                y: jordan_count,
                type: 'scatter',
                mode: 'lines',
                line: {color: 'rgba(222,45,38, 0.5)', dash: 'dot', width: 4},
                name : '# of Jordan Sales'
            };
            var trace4 = {
                x: size_max,
                y: yeezy_count,
                type: 'scatter',
                mode: 'lines',
                line: {color: 'rgba(55, 83, 109, 0.5)', dash: 'dot', width: 4},
                name : '# of Yeezy Sales'
            };
            var trace5 = {
                x: size_max,
                y: count_sneakers,
                type: 'bar',
                name : 'Total Sales',
                marker:{color: 'rgba(204,204,204,1)'}
            };
            data = [trace1, trace2, trace3, trace4, trace5];
            var layout = {
                title: "What size and which brand are more profitable",
                xaxis: {
                    title: {text: 'Size'},
                }
            };
            break;
        case "dataset3":
            datas = response[0]["More details on size 7.5"]
            var trace1 = {
                x: ['Yeezy-500', 'Yeezy-350', 'Yeezy-700', 'Jordan-1', 'Jordan-11', 'Jordan-6'],
                y: Object.values(datas["count_sneakers"]),
                type: 'line',
                name: 'Total Sales on size 7.5',
                line:{color: 'rgba(204,204,204,1)', dash: 'dot', width: 4},
            };
            var trace2 = {
                x: ['Yeezy-500', 'Yeezy-350', 'Yeezy-700', 'Jordan-1', 'Jordan-11', 'Jordan-6'],
                y: Object.values(datas["retaile_price"]),
                type: 'line',
                name: 'Retaile Prices',
                line: {color: 'grey', width: 3}
            };
            var trace3 = {
                x: ['Yeezy-500', 'Yeezy-350', 'Yeezy-700', 'Jordan-1', 'Jordan-11', 'Jordan-6'],
                y: Object.values(datas["how_much_earn"]),
                marker:{color: 'rgba(222,45,38,0.8)'},
                type: 'bar',
                name: '% of Profits on size 7.5'
            };
            var data = [trace1, trace2, trace3];
            var layout = {title: "More details on size 7.5"};
            break;
        case "dataset4":
            var datas = response[0]["Best time to buy/sell Sneakers"]
            var key_max_price = [];
            var key_avg_price = [];
            var key_min_price = [];
            var days_all = ['Friday', 'Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday'];
            var max_am = [];
            var max_pm = [];
            var min_am = [];
            var min_pm = [];
            datas['max_price'].forEach(dict => {
                key_max_price.push(Number(Object.keys(dict)[0]));
            });
            datas['min_price'].forEach(dict => {
                key_min_price.push(Number(Object.keys(dict)[0]))
            });
            datas['avg_price'].forEach(dict => {
                key_avg_price.push(Number(Object.keys(dict)[0]))
            });
            for (var i = 0; i < key_max_price.length/2; i++) {
                max_am.push(key_max_price[i]);
            }
            for (var i = key_max_price.length/2; i < key_max_price.length; i++) {
                max_pm.push(key_max_price[i]);
            }
            for (var i = 0; i < key_min_price.length/2; i++) {
                min_am.push(key_min_price[i]);
            }
            for (var i = key_min_price.length/2; i < key_min_price.length; i++) {
                min_pm.push(key_min_price[i]);
            }
            var trace1 = {
                x: days_all,
                y: max_am,
                type: 'bar',
                name : 'Maximum Prices at AM',
                marker:{color: 'rgb(70,130,180)'}
            };
            var trace2 = {
                x: days_all,
                y: max_pm,
                type: 'bar',
                name : 'Maximum Prices at PM',
                marker:{color: 'rgb(55, 83, 109)'}
            };
            var trace3 = {
                x: days_all,
                y: min_am,
                marker:{color: 'rgba(204,204,204,1)'},
                type: 'bar',
                name: 'Minimum Prices at AM'
            };
            var trace4 = {
                x: days_all,
                y: min_pm,
                type: 'bar',
                name : 'Minimum Prices at PM',
                marker:{color: 'grey'}
            };
            data = [trace1, trace2, trace3, trace4];
            var layout = {title: "Best time to buy/sell Sneakers"};
            break;
        default: 
            x = [1, 2, 3, 4, 5];
            y = [0, 0, 0, 0, 0];
            break;
        } 
        updatePlotly(data, layout);
        }).catch(function(error) {
            console.log(error);
        });
};

init();