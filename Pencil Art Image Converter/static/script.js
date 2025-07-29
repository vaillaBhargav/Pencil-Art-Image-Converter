const imageUpload = document.getElementById('imageUpload');
const originalImage = document.getElementById('originalImage');
const sketchImage = document.getElementById('sketchImage');
const uploadLabel = document.querySelector('.upload-label');

imageUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Show original image
    const reader = new FileReader();
    reader.onload = function(evt) {
        originalImage.src = evt.target.result;
        originalImage.classList.add('visible');
    };
    reader.readAsDataURL(file);

    // Prepare form data for upload
    const formData = new FormData();
    formData.append("image", file);

    // Show loading text while processing
    uploadLabel.textContent = "Processing...";

    // Send to Flask backend
    try {
        const response = await fetch('/upload', { method: 'POST', body: formData });
        if (!response.ok) throw new Error("Image processing failed.");
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        sketchImage.src = url;
        sketchImage.classList.add('visible');
    } catch (error) {
        alert(error.message);
    } finally {
        uploadLabel.textContent = "Choose an Image";
    }
});
