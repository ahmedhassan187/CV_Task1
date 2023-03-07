function toggleClass(div, classname){
    for(i = 0; i < div.length; i++){
        div[i].classList.remove(classname)
    }
}


function json_request(data,route,state){
    var xhr=new XMLHttpRequest();
    xhr.open("POST",route , true);
    xhr.setRequestHeader('Content-Type', 'application/json');    
    xhr.send(JSON.stringify(data));
    xhr.onload = function (e) {
        if (xhr.readyState === 4 && xhr.status === 200) {
                if(state == 'input'){
                send_img('./static/imgs/original_img.jpg','input');
                }
                if(state == 'output'){
                    send_img('./static/imgs/filtered_img.jpg','output');
                    console.log('wowowowo')
                }
                if(state == 'hybrid'){
                    send_img('./static/imgs/hybrid_img.jpg','hybrid');
                }
            } else {
            console.log('err')
        }
    };
}


function send_img(path,state){
    checkIfImageExists(path, (exists) => {
    if (exists) {
        var timestamp = new Date().getTime();
        if(state == 'input'){
            original = document.createElement('img')
            original.src = path +'?t=' + timestamp;
            originalImg.innerHTML = " ";
            originalImg.appendChild(original);   
        }
        if(state == 'hybrid'){
            hybrid = document.createElement('img')
            hybrid.src = path +'?t=' + timestamp;
            hybrid.innerHTML = " ";
            hybridImg.appendChild(hybrid); 
        }
        else{
            filtered = document.createElement('img')
            filtered.src = path +'?t=' + timestamp;
            filteredImg.innerHTML = " ";
            filteredImg.appendChild(filtered);      
            }
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
};

function imgToFlask(name , data ,filename , route){
    var xhr=new XMLHttpRequest();
    var fd=new FormData();
    fd.append(name,data ,filename);
    xhr.onreadystatechange = function() {
        if (xhr.status == 200) {
            console.log("i.ve been sent")
        }
        }; 
    xhr.open("POST",route,true);
    xhr.send(fd);
    console.log(fd)
};
