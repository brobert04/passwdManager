//JAVASCRIPT PENTRU MODALE SI PENTRU AFISAREA ACESTORA CAND APESI PE BUTOANELE
//DIN NAVBAR

const wrapper = document.querySelector(".wrapper")
if (wrapper){
    function displayForm(id){
        const form = document.getElementById(id);
        wrapper.style.display = "flex";
        form.style.display = "flex";

        const close = document.querySelectorAll("#close-button")
        close.forEach(c => {
            c.addEventListener("click", () =>{
                wrapper.style.display = "none";
                form.style.display = "none"; 
            })
        })
    }
}


// SCHIMBARE INTRE CASUTA DE LOGIN SI CEA DE SIGNUP
function switchBetween(id){
    const login = document.getElementById("login-form")
    const signup = document.getElementById("signup-form")

    if(id==="signup-form"){
        login.style.display = "none"
        displayForm(id)
    }
    else if(id === "login-form"){
        signup.style.display = "none"
        displayForm(id)
    }
}



//FUNCTIONALITATEA BUTOANELOR DE COPY DIN CASUTA CU PAROLA SI EMAIL-UL TAU
const copy = document.querySelectorAll(".copy")
copy.forEach(c =>{
    c.onclick = () =>
        {
            let element = c.previousElementSibling;
            element.select();
            document.execCommand("copy");
        }
})

// FUNCTIILE PENTRU FORMA HIDDEN
function logOut(){
    document.getElementById('form-logout').click();
  }

  function deleteCard(){
    let card = document.querySelector('.del-btn{{password.id}}');
    console.log(card);
    card.click();
 }  

// CASUTA DE ADAUGARE PAROLA - VIZUALIZARE PAROLA
const passBtn = document.querySelector('#togglePassword')
const password = document.querySelector('#id_password')

passBtn.addEventListener('click',function(e){
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password'
    password.setAttribute('type', type);
    this.classList.toggle('fa-eye-slash');
})