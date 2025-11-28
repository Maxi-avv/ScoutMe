// Custom JavaScript for ScoutMe

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap tooltips are used
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation enhancement
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Video upload preview
    document.getElementById('archivo')?.addEventListener('change', function(e) {
        var file = e.target.files[0];
        if (file) {
            var videoPreview = document.getElementById('video-preview');
            if (videoPreview) {
                videoPreview.src = URL.createObjectURL(file);
                videoPreview.style.display = 'block';
            }
        }
    });

    // Age calculation for date inputs
    document.querySelectorAll('input[type="date"][id*="fecha_nacimiento"]').forEach(function(input) {
        input.addEventListener('change', function() {
            calculateAge(this);
        });
    });

    // Search form enhancements
    var searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            // Show loading spinner
            var submitBtn = this.querySelector('button[type="submit"]');
            var originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Buscando...';
            submitBtn.disabled = true;

            // Re-enable after 2 seconds (in case of slow response)
            setTimeout(function() {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }

    // Message toggle functionality
    window.toggleMessage = function(messageId) {
        var messageElement = document.getElementById('message-' + messageId);
        if (messageElement) {
            messageElement.style.display = messageElement.style.display === 'none' ? 'block' : 'none';
        }
    };

    // Confirm delete actions
    document.querySelectorAll('.delete-confirm').forEach(function(element) {
        element.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar este elemento?')) {
                e.preventDefault();
            }
        });
    });

    // Dynamic form fields
    document.getElementById('tipo')?.addEventListener('change', function() {
        var tipo = this.value;
        var urlField = document.getElementById('url-field');
        var archivoField = document.getElementById('archivo-field');

        if (tipo === 'youtube') {
            urlField.style.display = 'block';
            archivoField.style.display = 'none';
        } else {
            urlField.style.display = 'none';
            archivoField.style.display = 'block';
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Character counter for textareas
    document.querySelectorAll('textarea[maxlength]').forEach(function(textarea) {
        var maxLength = textarea.getAttribute('maxlength');
        var counter = document.createElement('small');
        counter.className = 'text-muted float-end';
        counter.textContent = '0/' + maxLength;
        textarea.parentNode.appendChild(counter);

        textarea.addEventListener('input', function() {
            counter.textContent = this.value.length + '/' + maxLength;
        });
    });

    // Table sorting
    document.querySelectorAll('th[data-sort]').forEach(function(th) {
        th.style.cursor = 'pointer';
        th.addEventListener('click', function() {
            var table = this.closest('table');
            var tbody = table.querySelector('tbody');
            var rows = Array.from(tbody.querySelectorAll('tr'));
            var index = Array.from(this.parentNode.children).indexOf(this);
            var direction = this.getAttribute('data-direction') || 'asc';

            rows.sort(function(a, b) {
                var aVal = a.children[index].textContent.trim();
                var bVal = b.children[index].textContent.trim();

                if (direction === 'asc') {
                    return aVal.localeCompare(bVal);
                } else {
                    return bVal.localeCompare(aVal);
                }
            });

            direction = direction === 'asc' ? 'desc' : 'asc';
            this.setAttribute('data-direction', direction);

            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
        });
    });
});

// Utility functions
function calculateAge(dateInput) {
    var birthDate = new Date(dateInput.value);
    var today = new Date();
    var age = today.getFullYear() - birthDate.getFullYear();
    var monthDiff = today.getMonth() - birthDate.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }

    var ageField = document.getElementById(dateInput.id.replace('fecha_nacimiento', 'edad'));
    if (ageField) {
        ageField.value = age > 0 ? age : '';
    }
}

// AJAX helper function
function ajaxRequest(url, method, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                callback(null, JSON.parse(xhr.responseText));
            } else {
                callback(xhr.status, null);
            }
        }
    };
    xhr.send(JSON.stringify(data));
}

// Export functions for global use
window.calculateAge = calculateAge;
window.ajaxRequest = ajaxRequest;