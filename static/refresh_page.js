fetch('/api').then(
    function(response) {
        if (response.status !== 200){
            console.log(response.status);
            return;
        }
        response.json().then((data) => {
            $.ajax({
                type : "POST",
                url : '/load_ajax',
                data: JSON.stringify(data),
                contentType: 'application/json;charset=UTF-8',
                success: (result) => {
                    console.log(result)
                } 
            })
        })
    }
).catch((err) => {
    console.log('fetch error');
});