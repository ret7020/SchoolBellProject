function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}


// Bindings
const timetableModal = document.getElementById('timetableModal');
const melodiesModal = document.getElementById('melodiesModal');
const settingsModal = document.getElementById('settingsModal');

timetableModal.addEventListener('show.bs.modal', event => {
    getReqApi('/api/get_timetable').then(function(resp){
        if (resp["status"]){
            let txarea = document.getElementById("timetable-raw-times");
            txarea.value = resp["timetable"];
            txarea.style.height = `${resp['heights_px']}px`;
        }
    });
});
melodiesModal.addEventListener('show.bs.modal', event => {});
settingsModal.addEventListener('show.bs.modal', event => {});

document.getElementById("update_timetable_form").addEventListener('submit', function(e){
    e.preventDefault();
    let api_endpoint = this.getAttribute("action");
    var formData = new FormData(document.getElementById("update_timetable_form"));
    sendForm(api_endpoint, formData);
});