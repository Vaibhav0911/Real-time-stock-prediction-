document.getElementById('predict-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const ticker = document.getElementById('ticker').value;
    
    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `ticker=${ticker}`
    })
    .then(response => response.json())
    .then(data => {
        if(data.error){
            document.getElementById('result').innerText = data.error;
        } else {
            document.getElementById('result').innerText = `Predicted Price: $${data.predicted_price.toFixed(2)}`;

            // Fetch historical data and plot it
            fetch(`/historical/${ticker}`)
                .then(response => response.json())
                .then(histData => {
                    var trace1 = {
                        x: histData.dates,
                        y: histData.prices,
                        type: 'scatter',
                        mode: 'lines',
                        name: 'Actual Prices',
                        line: { color: '#1f77b4' }
                    };

                    var trace2 = {
                        x: [histData.dates[histData.dates.length - 1]],  // Use the last date for predicted value
                        y: [data.predicted_price],
                        mode: 'markers',
                        name: 'Predicted Price',
                        marker: { color: 'red', size: 10 }
                    };

                    var layout = {
                        title: `${ticker} Stock Prices`,
                        titlefont: {
                            family: 'Arial, sans-serif',
                            size: 24,
                            color: '#333'
                        },
                        xaxis: {
                            title: 'Date',
                            titlefont: { family: 'Arial, sans-serif', size: 18, color: '#333' },
                            tickfont: { size: 14, color: '#666' }
                        },
                        yaxis: {
                            title: 'Price (USD)',
                            titlefont: { family: 'Arial, sans-serif', size: 18, color: '#333' },
                            tickfont: { size: 14, color: '#666' }
                        },
                        legend: {
                            x: 0.1,
                            y: 1.1,
                            bgcolor: 'rgba(255, 255, 255, 0.5)',
                            bordercolor: '#333',
                            borderwidth: 1
                        },
                        paper_bgcolor: '#f9f9f9',
                        plot_bgcolor: '#f9f9f9'
                    };
                    
                    Plotly.newPlot('chart', [trace1, trace2], layout);
                    
                });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'An error occurred. Please try again later.';
    });
});
