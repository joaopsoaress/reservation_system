fetch("/slots")
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });

