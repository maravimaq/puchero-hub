function test_fakenodo_connection() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/fakenodo/test', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (!response.success) {
                document.getElementById("test_fakenodo_connection_error").style.display = "block";
                console.log(response);
                console.log(response.success);
                console.log(response.message);
            }
        } else if (xhr.readyState === 4 && xhr.status !== 200) {
            document.getElementById("test_fakenodo_connection_error").style.display = "block";
            console.error('Error:', xhr.status);
        }
    };
    xhr.send();
}