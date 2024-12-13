document.addEventListener('DOMContentLoaded', function() {
    const pageContainer = document.getElementById('page-container');
    const links = document.querySelectorAll('a'); // Select all links

    links.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior
        const href = this.href; // Get the link's destination

        pageContainer.classList.add('fade-out'); // Start fade-out

        setTimeout(function() {
          window.location.href = href; // Go to the new page after fade-out
        }, 500); // Adjust delay to match transition duration
    });
    });
});