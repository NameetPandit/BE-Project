function uploadImage() {
    let input = document.getElementById("imageInput");
    if (input.files.length === 0) {
        alert("Please select an image!");
        return;
    }

    let formData = new FormData();
    formData.append("file", input.files[0]);

    fetch("http://127.0.0.1:8080/upload_image", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.text || "Error in OCR!";
    })
    .catch(error => console.error("Error:", error));
}
