let EDModes = document.getElementsByClassName("edge-detection-type")

document.addEventListener("click", (e)=>{
    if(e.target.classList.contains("edge-detection-type")){
        toggleClass(EDModes, "active-edge-detection")
        e.target.classList.add("active-edge-detection") }
    })