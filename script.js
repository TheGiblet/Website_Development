document.addEventListener('DOMContentLoaded', function() {
  const pageContainer = document.getElementById('page-container');
  const nav = document.querySelector('nav');
  const transitionSettings = {
    class: 'fade-out',
    duration: 500 // In milliseconds
  };

  function handleLinkClick(event) {
    if (event.target.tagName === 'A') {
      event.preventDefault();
      const link = event.target;
      const href = link.href;

      pageContainer.classList.add(transitionSettings.class);

      const transitionEndHandler = function() {
        window.location.href = href;
        pageContainer.removeEventListener('transitionend', transitionEndHandler); // Remove the listener after redirecting
      };

      pageContainer.addEventListener('transitionend', transitionEndHandler);

      // Fallback for browsers that don't support transitionend
      setTimeout(transitionEndHandler, transitionSettings.duration); 
    }
  }

  nav.addEventListener('click', handleLinkClick);
});