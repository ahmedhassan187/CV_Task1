let tabs = document.getElementsByClassName("tab")
let tabsBodies = document.getElementsByClassName("tab-body")
let fTabFilters = document.getElementsByClassName("filter")
let fTabNoiseTypes = document.getElementsByClassName("noise-type")
let kernalSizeBox = document.querySelector(".kernal-size")
let radiusBox = document.querySelector(".radius")
let originalImg = document.querySelector(".original-img")
let filteredImg = document.querySelector('.filtered-img')
upload = document.getElementById("upload");

document.addEventListener("click", (e)=>{

    if(e.target.classList.contains("tab")){
        toggleClass(tabs, "active-tab")
        e.target.classList.add("active-tab")
        for(i = 0; i < tabsBodies.length; i++){
            tabsBodies[i].style.display = "none"
            if(tabsBodies[i].classList[1][2] == e.target.classList[1][3]){
                tabsBodies[i].style.display = "flex"
            }
        }
    }

// ################################################################################ //

    if(e.target.classList.contains("filter")){
        toggleClass(fTabFilters, "active-filter")
        e.target.classList.add("active-filter")
        filterType =e.target.classList[1]
        json_request(filterType,'/filter')
        filteredImg.src = '/static/imgs/filtered_img.jpg';
        console.log(filteredImg.src)
        if(e.target.classList.contains("kernal")){
            kernalSizeBox.style.display = "flex"
            radiusBox.style.display = "none"
        }else if(e.target.classList.contains("radius-filter")){
            kernalSizeBox.style.display = "none"
            radiusBox.style.display = "flex"
        }

    }

    // ################################################################################ //

    if(e.target.classList.contains("noise-type")){
        toggleClass(fTabNoiseTypes, "active-noise-type")
        e.target.classList.add("active-noise-type")
        noisetype = e.target.classList[1]
        json_request(noisetype,'/noise')
    }
})

// ################################################################################ //
// ################################################################################ //

let snrSlider = document.getElementById("snr-slider")
let snrSliderValue = document.querySelector(".snr-slider-value")

snrSlider.addEventListener("input", (e) =>{
    snrSliderValue.innerHTML = snrSlider.value

})

//############################################## upload img ############### //

upload.addEventListener('change' , (e) => {
    console.log(e)
    const reader1 = new FileReader();
    reader1.onload = (e) => {
    if (e.target){
        //upload first image
        let img = document.createElement("img");
        img.id = "img";
        img.src = e.target.result;
        //clean 1st image
        originalImg.innerHTML = " ";
        //add 1st image 
        originalImg.appendChild(img);
    }
    };
    //read the  1st img & send it >_<
    img1_send =  e.target.files[0];
    reader1.readAsDataURL(img1_send);
    var xhr=new XMLHttpRequest();
    var fd=new FormData();
    fd.append("original_img",img1_send , "original_img");
    xhr.onreadystatechange = function() {
        if (xhr.status == 200) {
            // filteredImg.src = './static/imgs/filtered_img.jpg';
            console.log('ya booooody');
        }
        }; 
    xhr.open("POST","/",true);
    xhr.send(fd);
    console.log(fd)
    });

