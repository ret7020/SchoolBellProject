function auto_grow(element) {
    element.style.height = '5px';
    element.style.height = `${element.scrollHeight}px`;
}

function upload_melody(){
    document.getElementById('uploadMelodyInput').click();
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
        document.getElementById('melodySelect').innerHTML = resp['all_melodies'];
    });
});

melodiesModal.addEventListener('show.bs.modal', function(e){
    getReqApi(`/api/get_melodies`).then(function(resp){
        if (resp["status"]){
            document.getElementById("melodies_container_ul").innerHTML = "";
            resp["melodies"].forEach(melody => {
                document.getElementById("melodies_container_ul").insertAdjacentHTML('beforeend', `
                    <li class="list-group-item melody_collaps_open_btn" data-bs-toggle="collapse" href="#melody_collapse_${melody[0]}">${melody[1]}</li>
                    <div class="collapse" id="melody_collapse_${melody[0]}">
                        <div style="margin-top: 10px">
                            <audio controls>
                                <source src="/melodies/${melody[2]}" type="audio/mpeg">
                            </audio>
                                
                        </div>
                    </div>
                `);
            });
        }
        
    })
});
settingsModal.addEventListener('show.bs.modal', event => {});


document.getElementById("update_timetable_form").addEventListener('submit', function(e){
    e.preventDefault();
    let api_endpoint = this.getAttribute("action");
    var formData = new FormData(document.getElementById("update_timetable_form"));
    document.getElementById("timetable_area").innerHTML = `<div class="d-flex justify-content-center">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
</div>`;
    sendForm(api_endpoint, formData).then(function(resp){
        document.getElementById("timetable_area").innerHTML = resp["new_time_table"];
    });
});

document.getElementById("update_lesson_form").addEventListener('submit', function(e){
    e.preventDefault();
    let api_endpoint = this.getAttribute("action");
    var formData = new FormData(document.getElementById("update_lesson_form"));
    document.getElementById("timetable_area").innerHTML = `<div class="d-flex justify-content-center">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
</div>`;
    sendForm(api_endpoint, formData).then(function(resp){
        bootstrap.Modal.getInstance(lessonModal).hide();
        document.getElementById("timetable_area").innerHTML = resp["new_time_table"];
    });
});

document.getElementById("uploadMelodyInput").addEventListener('input', function(e){
    let form = document.getElementById("upload_melody_form");
    let status_text = document.getElementById("melody_upload_status");
    let api_endpoint = form.getAttribute("action");
    var formData = new FormData(form);
    status_text.innerText = "Uploading...";
    sendForm(api_endpoint, formData).then(function(resp){
        console.log(resp);
        document.getElementById("uploadMelodyInput").value = "";
    });
});