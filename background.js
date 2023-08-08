document
  .getElementById("settingsForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const summaryLength = document.getElementById("summaryLength").value;
    const selectedLanguage = document.querySelector(
      'input[name="language"]:checked'
    ).id;
    console.log(selectedLanguage);
    console.log(summaryLength);
    document.getElementById("settingsForm").innerHTML = "Applied";
    sendDataToFlaskServer(summaryLength, selectedLanguage);
  });

function sendDataToFlaskServer(summaryLength, selectedLanguage) {
  // Assuming you have the Flask server URL here, replace it with your actual server URL.
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://127.0.0.1:5000/settings");
  xhr.setRequestHeader("Content-Type", "application/json"); // Set the request header to indicate JSON data.
  xhr.send(
    JSON.stringify({
      summaryLength: summaryLength,
      selectedLanguage: selectedLanguage,
    })
  );
}
