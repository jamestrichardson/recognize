// Tab functionality
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            const tabId = button.dataset.tab + '-tab';
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Handle form submissions
    setupFormHandler('face-image-form', '/api/detect/face/image', 'face-image-input');
    setupFormHandler('face-video-form', '/api/detect/face/video', 'face-video-input', 'face-frame-skip');
    setupFormHandler('object-image-form', '/api/detect/object/image', 'object-image-input');
    setupFormHandler('object-video-form', '/api/detect/object/video', 'object-video-input', 'object-frame-skip');
});

function setupFormHandler(formId, endpoint, fileInputId, frameSkipId = null) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const fileInput = document.getElementById(fileInputId);
        const file = fileInput.files[0];

        if (!file) {
            showAlert('Please select a file', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        if (frameSkipId) {
            const frameSkip = document.getElementById(frameSkipId).value;
            formData.append('frame_skip', frameSkip);
        }

        // Show progress
        showProgress();

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                displayResults(result.data);
            } else {
                showAlert(result.message || 'An error occurred', 'error');
            }
        } catch (error) {
            showAlert('Failed to process file: ' + error.message, 'error');
        } finally {
            hideProgress();
        }
    });
}

function showProgress() {
    const progress = document.getElementById('progress');
    const results = document.getElementById('results');

    if (progress) progress.style.display = 'block';
    if (results) results.style.display = 'none';
}

function hideProgress() {
    const progress = document.getElementById('progress');
    if (progress) progress.style.display = 'none';
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    if (!resultsDiv) return;

    let html = '<h3>Detection Results</h3>';

    // Display annotated image/video
    if (data.annotated_image) {
        html += `<img src="/api/uploads/${data.annotated_image.split('/').pop()}" alt="Annotated Result">`;
    } else if (data.annotated_video) {
        html += `<video controls style="max-width: 100%;">
                    <source src="/api/uploads/${data.annotated_video.split('/').pop()}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>`;
    }

    // Display detection info
    html += '<div class="result-info">';

    if (data.faces_detected !== undefined) {
        html += `<p><strong>Faces Detected:</strong> ${data.faces_detected}</p>`;

        if (data.faces && data.faces.length > 0) {
            html += '<p><strong>Face Details:</strong></p>';
            html += '<ul class="detection-list">';
            data.faces.forEach(face => {
                html += `<li>Face ${face.face_id}: Position (${face.bbox.x}, ${face.bbox.y}),
                        Size ${face.bbox.width}x${face.bbox.height}</li>`;
            });
            html += '</ul>';
        }

        if (data.total_faces_detected !== undefined) {
            html += `<p><strong>Total Faces in Video:</strong> ${data.total_faces_detected}</p>`;
            html += `<p><strong>Frames Processed:</strong> ${data.processed_frames} / ${data.total_frames}</p>`;
        }
    }

    if (data.objects_detected !== undefined) {
        html += `<p><strong>Objects Detected:</strong> ${data.objects_detected}</p>`;

        if (data.objects && data.objects.length > 0) {
            html += '<p><strong>Object Details:</strong></p>';
            html += '<ul class="detection-list">';
            data.objects.forEach(obj => {
                html += `<li>${obj.class}: ${(obj.confidence * 100).toFixed(1)}% confidence</li>`;
            });
            html += '</ul>';
        }

        if (data.object_summary) {
            html += '<p><strong>Object Summary:</strong></p>';
            html += '<ul class="detection-list">';
            for (const [objClass, count] of Object.entries(data.object_summary)) {
                html += `<li>${objClass}: ${count} occurrences</li>`;
            }
            html += '</ul>';
        }

        if (data.total_frames) {
            html += `<p><strong>Frames Processed:</strong> ${data.processed_frames} / ${data.total_frames}</p>`;
        }
    }

    html += '</div>';

    resultsDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
}

function showAlert(message, type) {
    const resultsDiv = document.getElementById('results');
    if (!resultsDiv) return;

    resultsDiv.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    resultsDiv.style.display = 'block';
}
