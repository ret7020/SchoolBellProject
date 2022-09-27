function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}


// Bindings
const timetableModal = document.getElementById('timetableModal');
const melodiesModal = document.getElementById('melodiesModal');
const settingsModal = document.getElementById('settingsModal');
const lessonModal = document.getElementById('editLessonModal');

timetableModal.addEventListener('show.bs.modal', event => {
    getReqApi('/api/get_timetable').then(function(resp){
        if (resp["status"]){
            let txarea = document.getElementById("timetable-raw-times");
            txarea.value = resp["timetable"];
            txarea.style.height = `${resp['heights_px']}px`;
        }
    });
});
lessonModal.addEventListener('show.bs.modal', function(e){
    document.getElementById('editLessonModalLabel').innerText = `Редактировать урок № ${e.relatedTarget.dataset['lesson_id']}`;
    getReqApi(`/api/get_lesson_data?lesson_id=${e.relatedTarget.dataset['lesson_id']}`).then(function(resp){
        document.getElementById('lessonStartInput').value = resp['lesson_start'];
        document.getElementById('lessonFinishInput').value = resp['lesson_finish'];
        document.getElementById('update_lesson_id_hidden').value = e.relatedTarget.dataset['lesson_id'];
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

document.getElementById("update_lesson_form").addEventListener('submit', function(e){
    e.preventDefault();
    let api_endpoint = this.getAttribute("action");
    var formData = new FormData(document.getElementById("update_lesson_form"));
    sendForm(api_endpoint, formData).then(function(resp){
        bootstrap.Modal.getInstance(lessonModal).hide();
    });
});