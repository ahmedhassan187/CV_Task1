function toggleClass(div, classname){
    for(i = 0; i < div.length; i++){
        div[i].classList.remove(classname)
    }
}
function json_request(data,route){
    var xhr=new XMLHttpRequest();
    xhr.open("POST",route , true);
    xhr.setRequestHeader('Content-Type', 'application/json');    
    xhr.send(JSON.stringify(data));
    xhr.onload = function (e) {
        if (xhr.readyState === 4 && xhr.status === 200) {
                console.log(JSON.stringify(data))
                //filteredImg.src = '/static/imgs/filtered_img.jpg';
        } else {
            console.log('err')
        }
    };
}