document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const uploadStatus = document.getElementById('uploadStatus');
    const resumeInput = document.getElementById('resumes');
    const selectedFiles = document.getElementById('selectedFiles');
    const fileList = document.getElementById('fileList');

    if (uploadForm) {
        // Handle file selection (PDFs only)
        resumeInput.addEventListener('change', function(e) {
            const files = Array.from(e.target.files);

            if (files.length > 0) {
                selectedFiles.classList.remove('hidden');
                fileList.innerHTML = ''; // Clear existing list

                // Add animation class to container
                selectedFiles.classList.add('animate-fade-in');

                files.forEach((file, index) => {
                    if (file.name.toLowerCase().endsWith('.pdf')) {  // Only allow PDFs
                        const li = document.createElement('li');
                        li.className = 'flex justify-between items-center mb-2 animate-fade-in';
                        li.style.animationDelay = `${index * 50}ms`;

                        li.innerHTML = `
                            <div class="flex items-center">
                                <i class="bi bi-file-pdf text-red-500 mr-2"></i>
                                <span class="text-gray-200">${file.name}</span>
                            </div>
                            <span class="badge bg-red-500 rounded-full text-xs">
                                ${(file.size / 1024).toFixed(1)} KB
                            </span>
                        `;
                        fileList.appendChild(li);
                    }
                });
            } else {
                selectedFiles.classList.add('hidden');
            }
        });

        // Handle form submission
        uploadForm.addEventListener('submit', function(e) {
            const requirementsText = document.getElementById('requirements').value;
            const resumeFiles = resumeInput.files;

            if (!requirementsText.trim() || resumeFiles.length === 0) {
                e.preventDefault();
                alert('Please enter job requirements and select at least one PDF file');
                return;
            }

            // Show processing status with animation
            uploadStatus.classList.remove('hidden');
            uploadStatus.classList.add('animate-fade-in');

            // Disable submit button and add loading state
            const submitButton = uploadForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = `
                <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                Processing...
            `;
        });
    }
});
