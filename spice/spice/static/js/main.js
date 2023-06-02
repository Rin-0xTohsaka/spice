// Wait until the document has fully loaded
$(document).ready(function() {
    // Get the 2d drawing context of the canvas with id 'chart'
    var ctx = document.getElementById('chart').getContext('2d');
    
    // Declare a variable to hold our chart instance
    var chart;

    // Declare a placeholder address to fetch data for on page load
    var address = 'bc1p2xmduzppdyw05xj9zk2v0fqwwhga84kvnzg3fue27646rmqlverqd9lxf6';

    // Helper function to truncate fields
    function truncateField(field) {
        if (!field) return "";
        return field.length > 10 ? field.slice(0, 6) + "..." + field.slice(-4) : field;
    }

    // Helper function to format Unix time to DateTime
    function formatTime(unixTime) {
        var date = new Date(Number(unixTime));
        return date.toLocaleString();
    }
    
    // Define a function to fetch data for a given address
    function fetchData(address) {
        // Fetch the token data from the backend
        $.getJSON('/api/fetch_data?address=' + address, function(data) {
            // Clear the table first
            $('#data-table').empty();

            // Then for each item in the data
            data.forEach(function(item) {
                // Create a new table row
                var row = $('<tr>');
                // Add a cell with the token name
                row.append($('<td>').text(item.token));
                // Add a cell with the token balance
                row.append($('<td>').text(item.balance));
                // Add a cell with the token type
                row.append($('<td>').text(item.tokenType));
                // Add the row to the table
                $('#data-table').append(row);
            });
        });

        // Fetch data for chart
        $.getJSON('/api/fetch_chart_data?address=' + address, function(data) {
            // If a chart already exists, destroy it before creating a new one
            if (chart) {
                chart.destroy();
            }
            // Create a new chart
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(function(item) { return item.token; }),  // Use the token names as labels
                    datasets: [{
                        label: 'Balance',  // Set the label for the dataset
                        data: data.map(function(item) { return item.balance; }),  // Use the token balances as data
                        backgroundColor: 'rgba(0, 123, 255, 0.5)',  // Set the background color of the bars
                        borderColor: 'rgba(0, 123, 255, 1)',  // Set the border color of the bars
                        borderWidth: 1  // Set the border width of the bars
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true  // Start the y-axis at 0
                        }
                    }
                }
            });
        });
    }

    // Declare a variable to hold the total page count
    var totalPageCount = 0;

    // Modify fetchTransactionHistory to format and truncate fields
    function fetchTransactionHistory(address, page = 1) {
        // Fetch the transaction history data from the backend
        $.getJSON('/api/fetch_transaction_history?address=' + address + '&page=' + page, function(data) {
            // Set the total page count
            totalPageCount = data.total_count;
            // Clear the table first
            $('#transaction-history-table').empty();

            // Then for each item in the data
            data.transactions.forEach(function(item) {
                // Create a new table row
                var row = $('<tr>');
                // Add cells with the data, using truncateField where necessary, and formatTime for the time
                row.append($('<td>').text(formatTime(item.time)));
                row.append($('<td>').text(item.token));
                row.append($('<td>').text(truncateField(item.txId)));
                row.append($('<td>').text(item.blockHeight));
                row.append($('<td>').text(item.state));
                row.append($('<td>').text(item.actionType));
                row.append($('<td>').text(item.amount));
                row.append($('<td>').text(truncateField(item.fromAddress)));
                row.append($('<td>').text(truncateField(item.toAddress)));
                // Add the row to the table
                $('#transaction-history-table').append(row);
            });
            
            // Generate the pagination buttons
            generatePaginationButtons();
        });
    }

    // Modify generatePaginationButtons to only create as many buttons as there are pages of data
    function generatePaginationButtons() {
        // Clear the pagination buttons first
        $('#pagination-buttons').empty();
        
        // Calculate how many pages there will be
        var numPages = Math.ceil(totalPageCount / 10);

        // Then for each page
        for (let i = 1; i <= numPages; i++) {
            // Create a new button
            var button = $('<button>').text('Page ' + i);
            // Set the onclick function to fetch data for the corresponding page
            button.on('click', function() { fetchTransactionHistory(address, i); });
            // Add the button to the pagination buttons
            $('#pagination-buttons').append(button);
        }
    }

        // Fetch data on page load for the placeholder address
        fetchData(address);

        // Fetch transaction history on page load for the placeholder address
        fetchTransactionHistory(address);

        // Then fetch data again when the form is submitted
        $('#address-form').on('submit', function(event) {
            event.preventDefault();  // prevent the form from being submitted normally
            var newAddress = $('#address').val();  // Get the address entered by the user
            fetchData(newAddress);  // Fetch data for the new address
            fetchTransactionHistory(newAddress);  // Fetch transaction history for the new address
        });
    });

/*
How to add to the code
This JavaScript code primarily deals with handling user input, fetching data from the backend, 
and updating the frontend with the fetched data. Here are a few ways you could extend it:

- Add more user inputs: Right now, the only input is the Bitcoin address. You could add more 
  inputs for the user to control, such as the type of chart to display or the time period 
  of data to fetch.

- Improve error handling: Right now, if the backend returns an error (for example, if the 
  entered address is invalid), the frontend doesn't do anything special. You could add code 
  to handle these errors and display a helpful message to the user.

- Add more interactivity: For example, you could add buttons to sort the table by different 
  columns, or you could add a dropdown to filter the table by token type.

Remember, when adding new features, it's important to consider both the frontend and the backend. 
For example, if you want to add a feature to filter the table by token type, you would need to 
add a user input on the frontend, send that input to the backend, and then modify the backend to 
return filtered data.
*/
