const formToggler = document.querySelector("#formToggler");
console.log(formToggler)
let formHidden = true;

formToggler.addEventListener("click", formToggle)

function formToggle(){
    if(formHidden){
        document.querySelector("form").style.display = "flex";
        formToggler.textContent = "Hide Form";
        formHidden = false;
    }
    else{
        document.querySelector("form").style.display = "none";
        formToggler.textContent = "Show Form";
        formHidden = true;
    }
}