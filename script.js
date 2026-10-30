const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const fileName = document.getElementById("fileName");

if (fileInput && preview) {
fileInput.addEventListener("change", function () {
const file = this.files[0];

    if (!file) {
        preview.src = "";
        preview.style.display = "none";

        if (fileName) {
            fileName.textContent = "";
        }
        return;
    }

    if (!file.type.startsWith("image/")) {
        alert("Please select an image file.");
        this.value = "";
        preview.src = "";
        preview.style.display = "none";

        if (fileName) {
            fileName.textContent = "";
        }
        return;
    }

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";

    if (fileName) {
        fileName.textContent = file.name;
    }
});
}
