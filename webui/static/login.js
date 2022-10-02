document.getElementById("login_form").addEventListener('submit', function (e) {
    e.preventDefault();
    let api_endpoint = this.getAttribute("action");
    var formData = new FormData(document.getElementById("login_form"));
    sendForm(api_endpoint, formData).then(function(resp){
        if (resp["status"]){
            window.location.href = '/';
        }else{
            document.getElementById("invalid_password").style.display = "block";
        }
    })
});