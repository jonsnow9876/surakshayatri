document.addEventListener('DOMContentLoaded', () => {
  // --- Get references to all necessary DOM elements ---
  const registerForm = document.getElementById('registerForm');
  const submitButton = document.getElementById('submitBtn');
  const messageArea = document.getElementById('messageArea');
  const qrCodeArea = document.getElementById('qrCodeArea');
  const qrCodeImage = document.getElementById('qrCodeImage');

  // --- Safety check: ensure all elements exist before adding listeners ---
  if (!registerForm || !submitButton || !messageArea || !qrCodeArea || !qrCodeImage) {
    console.error('Fatal Error: One or more required HTML elements are missing from the page.');
    return;
  }

  registerForm.addEventListener('submit', async (event) => {
    // Prevent the default form submission which reloads the page
    event.preventDefault();

    // --- 1. Reset the UI for a new submission ---
    messageArea.textContent = '';
    messageArea.className = 'alert'; // Reset any success/danger classes
    qrCodeArea.style.display = 'none';
    qrCodeImage.src = '';

    // --- 2. Provide user feedback during the process ---
    submitButton.disabled = true;
    submitButton.textContent = 'Registering...';

    // --- 3. Prepare the data to be sent to the API ---
    const formData = new FormData(registerForm);
    const payload = {
      name: formData.get('name'),
      email: formData.get('email'),
      phone: formData.get('phone'),
      passport: formData.get('passport'),
      password: formData.get('password'),
      itinerary: formData.get('itinerary') || null // Send null if empty
    };

    try {
      // --- 4. Send the request to the backend ---
      const response = await fetch('/register/new', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      // --- 5. Handle potential errors from the server ---
      if (!response.ok) {
        // Use the server's error message if available, otherwise use a generic one
        const errorMessage = data.detail || `Server returned an error: ${response.status}`;
        throw new Error(errorMessage);
      }

      // --- 6. Handle the success case ---
      messageArea.className = 'alert alert-success';
      messageArea.innerHTML = `
        <strong>Registration Successful!</strong><br>
        Your details are secure. Save this QR to use in the mobile app.<br><br>
        <strong>Tourist ID:</strong> <code>${data.tourist_id}</code><br>
        <strong>Temporary ID:</strong> <code>${data.temp_id}</code>
      `;

      // Display the QR code image received from the server
      qrCodeImage.src = `data:image/png;base64,${data.qr_code_base64}`;
      qrCodeArea.style.display = 'block';

      registerForm.reset(); // Clear the form fields

    } catch (error) {
      // --- 7. Handle network errors or server errors ---
      console.error('Registration failed:', error);
      messageArea.className = 'alert alert-danger';
      messageArea.textContent = `Error: ${error.message}`;

    } finally {
      // --- 8. Always re-enable the button after the process is complete ---
      submitButton.disabled = false;
      submitButton.textContent = 'Register & Generate QR';
    }
  });
});