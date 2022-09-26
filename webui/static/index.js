
// Bindings
const timetableModal = document.getElementById('timetableModal');
const melodiesModal = document.getElementById('melodiesModal');
const settingsModal = document.getElementById('settingsModal');

timetableModal.addEventListener('show.bs.modal', event => {
    console.log("Send AJAX");
});
melodiesModal.addEventListener('show.bs.modal', event => {});
settingsModal.addEventListener('show.bs.modal', event => {});