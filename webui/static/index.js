// Globals
const MELODY_BLOCK = `<li class="list-group-item melody_collaps_open_btn" data-bs-toggle="collapse" href="#melody_collapse_{0}" id="collapse_togler_melody_{0}">{1}</li>
<div class="collapse" id="melody_collapse_{2}">
    <div style="margin-top: 10px">
        <form action='/api/update_melody_title' method='POST' id='change_melody_title_form_{0}'>
            <div class="input-group" style='margin-bottom: 10px'>
                <span class="input-group-text">Название</span>
                <input type='hidden' name='melody_id' value='{0}'>
                <input type="text" aria-label="Title" class="form-control" name='title' value='{1}' required>
                <button class="btn btn-outline-primary" type="button" onclick='update_melody_title({0})'>OK</button>
            </div>
        </form>
        <audio controls>
            <source src="/melodies/{3}" type="audio/mpeg">
        </audio>
    </div>
    <button class="btn btn-outline-danger delete_melody" type="button" onclick='delete_melody({0})'>Удалить</button>
</div>`

function auto_grow(element) {
    element.style.height = '5px';
    element.style.height = `${element.scrollHeight}px`;
}

function upload_melody() {
    document.getElementById('uploadMelodyInput').click();
}

function update_melody_title(melody_id) {
    let form = document.getElementById(`change_melody_title_form_${melody_id}`);
    let api_endpoint = form.getAttribute("action");
    var formData = new FormData(form);
    sendForm(api_endpoint, formData).then(function (resp) {
        if (resp["status"]) {
            console.log(resp);
            document.getElementById(`collapse_togler_melody_${melody_id}`).innerText = resp["new_title"];
        }
    });
}

function delete_melody(melody_id) {
    getReqApi(`/api/delete_melody?melody_id=${melody_id}`).then(function (resp) {
        if (resp.status){
            document.getElementById(`melody_collapse_${melody_id}`).remove();
            document.getElementById(`collapse_togler_melody_${melody_id}`).remove();
        }
    });
}


function check_password_confirmation(current_password, confirm_password) {
    if (current_password == confirm_password) {
        submitSettingsButton.disabled = false;
        confirmationStatusText.innerText = "пароли совпадают";
        confirmationStatusText.style.color = "green";
    } else {
        submitSettingsButton.disabled = true;
        confirmationStatusText.innerText = "пароли не совпадают";
        confirmationStatusText.style.color = "red";
    }
}


// Bindings
const timetableModal = document.getElementById('timetableModal');
const melodiesModal = document.getElementById('melodiesModal');
const settingsModal = document.getElementById('settingsModal');
const lessonModal = document.getElementById('editLessonModal');
const debugModal = document.getElementById('sysinfoModal');
const muteDayModal = document.getElementById('muteDayModal');

const confirmPasswordBlock = document.getElementById('passwordConfirmationBlock');
const confirmPasswordInput = document.getElementById('newPasswordConfirm');
const newPasswordInput = document.getElementById('newPassword');
const submitSettingsButton = document.getElementById('updateConfigurationButton');
const confirmationStatusText = document.getElementById('passwordConfirmStatus');
const switcher = document.getElementById("sounds_status");


muteDayModal.addEventListener('show.bs.modal', function (e) {
    getReqApi('/api/get_mute_mode').then(function (resp) {
        if (resp["status"]) {
            if (resp["mute_mode"][0] == 1) {
                document.getElementById("mute_mode_status").innerText = `звук выключен c ${resp['mute_mode'][1][0]}.${resp['mute_mode'][1][1]}.${resp['mute_mode'][1][2]}`;
                document.getElementById("mute_mode_status").style.color = "red";
                switcher.checked = true;
            } else {
                document.getElementById("mute_mode_status").innerText = "звук включен";
                document.getElementById("mute_mode_status").style.color = "green";
                switcher.checked = false;
            }
        }
    });
});



debugModal.addEventListener('show.bs.modal', event => {
    let req_time_start = new Date().getTime();
    getReqApi('/api/get_sys').then(function (resp) {
        if (resp["status"]) {
            document.getElementById("server_local_time").innerText = resp["server_time"];
            document.getElementById("real_ntp_time").innerText = resp["ntp_time"];
            document.getElementById("ntp_server_host").innerText = resp["ntp_server"];
            document.getElementById("api_req_time").innerText = `${new Date().getTime() - req_time_start} ms`;
            document.getElementById("cpu_temperature").innerText = `${resp["cpu_temperature"]}°C`;
            document.getElementById("cpu_usage").innerText = `${resp["cpu_load"]}%`;
            document.getElementById("ram_usage").innerText = `${resp["ram_load"]}%`;
        }
    })
})

timetableModal.addEventListener('show.bs.modal', event => {
    getReqApi('/api/get_timetable').then(function (resp) {
        if (resp["status"]) {
            let txarea = document.getElementById("timetable-raw-times");
            txarea.value = resp["timetable"];
            txarea.style.height = `${resp['heights_px']}px`;
        }
    });
});
lessonModal.addEventListener('show.bs.modal', function (e) {
    document.getElementById('editLessonModalLabel').innerText = `Редактировать урок № ${e.relatedTarget.dataset['lesson_id']}`;
    getReqApi(`/api/get_lesson_data?lesson_id=${e.relatedTarget.dataset['lesson_id']}`).then(function (resp) {
        document.getElementById('lessonStartInput').value = resp['lesson_start'];
        document.getElementById('lessonFinishInput').value = resp['lesson_finish'];
        document.getElementById('update_lesson_id_hidden').value = e.relatedTarget.dataset['lesson_id'];
        document.getElementById('melodySelectStart').innerHTML = resp['all_melodies_start'];
        document.getElementById('melodySelectFinish').innerHTML = resp['all_melodies_finish'];
        document.getElementById("work_at_saturday").checked = resp["saturday_work"];
        document.getElementById("work_at_sunday").checked = resp["sunday_work"];
    });
});

melodiesModal.addEventListener('show.bs.modal', function (e) {
    getReqApi(`/api/get_melodies`).then(function (resp) {
        if (resp["status"]) {
            document.getElementById("melodies_container_ul").innerHTML = "";
            resp["melodies"].forEach(melody => {
                document.getElementById("melodies_container_ul").insertAdjacentHTML('beforeend', MELODY_BLOCK.format(melody[0], melody[1], melody[0], melody[2]));
            });
        }

    });
});
settingsModal.addEventListener('hide.bs.modal', function (e) {
    newPasswordInput.value = "";
    confirmPasswordInput.value = "";
    confirmPasswordBlock.style.display = "none";
});

timetableModal.addEventListener('hide.bs.modal', function (e) {
    document.getElementById("error_timetable").style.display = 'none';
});



document.getElementById("update_timetable_form").addEventListener('submit', function (e) {
    e.preventDefault();
    let api_endpoint = this.getAttribute("action");
    let formData = new FormData(document.getElementById("update_timetable_form"));
    let old_timetable = document.getElementById("timetable_area").innerHTML;
    document.getElementById("timetable_area").innerHTML = `<div class="d-flex justify-content-center">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
</div>`;
    sendForm(api_endpoint, formData).then(function (resp) {
        if (resp["status"]) {
            document.getElementById("timetable_area").innerHTML = resp["new_time_table"];
            document.getElementById("error_timetable").style.display = 'none';
        } else {
            document.getElementById("timetable_area").innerHTML = old_timetable;
            document.getElementById("error_timetable").innerText = `Ошибка: накладывание звонков между уроками №${resp["lessons"][0]} и №${resp["lessons"][1]}`;
            document.getElementById("error_timetable").style.display = 'block';
        }

    });
});

document.getElementById("update_lesson_form").addEventListener('submit', function (e) {
    e.preventDefault();
    let api_endpoint = this.getAttribute("action");
    var formData = new FormData(document.getElementById("update_lesson_form"));
    let old_timetable = document.getElementById("timetable_area").innerHTML;
    document.getElementById("timetable_area").innerHTML = `<div class="d-flex justify-content-center">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
</div>`;
    sendForm(api_endpoint, formData).then(function (resp) {
        if (resp["status"]) {
            bootstrap.Modal.getInstance(lessonModal).hide();
            document.getElementById("timetable_area").innerHTML = resp["new_time_table"];
        } else { // overlay error handler
            document.getElementById("error_timetable_lesson_modify").innerText = `Ошибка: накладывание звонков между уроками №${resp["lessons"][0]} и №${resp["lessons"][1]}`;;
            document.getElementById("error_timetable_lesson_modify").style.display = 'block';
            document.getElementById("timetable_area").innerHTML = old_timetable;
        }

    });
});

document.getElementById("uploadMelodyInput").addEventListener('input', function (e) {
    let form = document.getElementById("upload_melody_form");
    let status_text = document.getElementById("melody_upload_status");
    let api_endpoint = form.getAttribute("action");
    var formData = new FormData(form);
    status_text.innerText = "Uploading...";
    sendForm(api_endpoint, formData).then(function (resp) {
        if (resp["status"]) {
            status_text.innerText = "";
            document.getElementById("melodies_container_ul").insertAdjacentHTML('beforeend', MELODY_BLOCK.format(resp['melody_id'], resp['melody_name'], resp['melody_id'], resp['melody_name']));
        }
        document.getElementById("uploadMelodyInput").value = "";
    });
});

document.getElementById("update_configuration_form").addEventListener('submit', function (e) {
    e.preventDefault();
    let api_endpoint = this.getAttribute("action");
    var formData = new FormData(document.getElementById("update_configuration_form"));
    sendForm(api_endpoint, formData).then(function (resp) {
        if (resp["status"]) {
            bootstrap.Modal.getInstance(settingsModal).hide();
        }
    })
});


document.getElementById("newPassword").addEventListener('input', function (e) {
    if (this.value) {
        check_password_confirmation(this.value, confirmPasswordInput.value);
        confirmPasswordBlock.style.display = "block";
    } else {
        confirmPasswordBlock.style.display = "none";
    }
});


switcher.addEventListener('input', function (e) {
    getReqApi(`/api/toggle_mute_mode?current_mode=${e.target.checked}`).then(function (resp) {
        if (resp["status"]) {
            if (e.target.checked) {
                document.getElementById("mute_mode_status").innerText = "звук выключен";
                document.getElementById("mute_mode_status").style.color = "red";
            } else {
                document.getElementById("mute_mode_status").innerText = "звук включен";
                document.getElementById("mute_mode_status").style.color = "green";
            }
        }
    })
});

confirmPasswordInput.addEventListener('input', function (e) {
    check_password_confirmation(this.value, newPasswordInput.value)
});