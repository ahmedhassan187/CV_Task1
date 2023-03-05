let tabs = document.getElementsByClassName("tab")
let tabsBodies = document.getElementsByClassName("tab-body")
let fTabFilters = document.getElementsByClassName("filter")

document.addEventListener("click", (e)=>{

    if(e.target.classList.contains("tab")){
        for(i = 0; i < tabs.length; i++){
            tabs[i].classList.remove("active-tab")
        }
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
        for(i = 0; i < fTabFilters.length; i++){
            fTabFilters[i].classList.remove("active-filter")
        }
        e.target.classList.add("active-filter")
    }
})

// ################################################################################ //
// ################################################################################ //

let snrSlider = document.getElementById("snr-slider")
let snrSliderValue = document.querySelector(".snr-slider-value")

snrSlider.addEventListener("input", (e) =>{
    snrSliderValue.innerHTML = snrSlider.value
})