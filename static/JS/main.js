let tabs = document.getElementsByClassName("tab")
let tabsBodies = document.getElementsByClassName("tab-body")
let fTabFilters = document.getElementsByClassName("filter")
let fTabNoiseTypes = document.getElementsByClassName("noise-type")
let kernalSizeBox = document.querySelector(".kernal-size")
let radiusBox = document.querySelector(".radius")

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
    }
})

// ################################################################################ //
// ################################################################################ //

let snrSlider = document.getElementById("snr-slider")
let snrSliderValue = document.querySelector(".snr-slider-value")

snrSlider.addEventListener("input", (e) =>{
    snrSliderValue.innerHTML = snrSlider.value
})