function generateRandomImage() {
    // Construct the URL for your Python script
    var scriptUrl = "background_generator.py"; // Assuming the script is in the same directory
  
    // Make a request to the Python script
    fetch(scriptUrl)
      .then(response => response.text())
      .then(filename => {
        // Extract the filename from the response
        // (You might need to adjust this based on how your script returns the filename)
        var imageUrl = "images/" + filename.trim();
  
        // Update the background image of the body
        document.body.style.backgroundImage = "url('" + imageUrl + "')";
      })
      .catch(error => {
        console.error("Error generating background image:", error);
      });
  }
  
  // Call the function to generate the initial background image
  generateRandomImage();
  
  // You can also call this function on other events, like a button click or a timer