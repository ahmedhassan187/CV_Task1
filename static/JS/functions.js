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
                //console.log(JSON.stringify(data))
                send_img();
                console.log('body the king')
            } else {
            console.log('err')
        }
    };
}



function send_img(){
    checkIfImageExists('./static/imgs/filtered_img.jpg', (exists) => {
    if (exists) {
        console.log('Image exists.')
        var timestamp = new Date().getTime();
        filtered = document.createElement('img')
        filtered.src = './static/imgs/filtered_img.jpg?t=' + timestamp;
        filteredImg.innerHTML = " ";
        filteredImg.appendChild(filtered)         
        console.log("sucessfully send"); 
    } else {
        console.log('Image does not exists.')
    }
});
}
function checkIfImageExists(url, callback) {
    const img = new Image();
    img.src = url;
    
    if (img.complete) {
        callback(true);
    } else {
        img.onload = () => {
        callback(true);
    };
        img.onerror = () => {
        callback(false);
        };
    }
}