const btn = document.getElementById("summarise");
btn.addEventListener("click", function () {
  btn.disabled = true;
  (btn.innerHTML = "Summarising..."),
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
      var url = tabs[0].url;
      var xhr = new XMLHttpRequest();
      xhr.open("GET", "http://127.0.0.1:5000/summary?url=" + url, true);
      xhr.onload = function () {
        var text = xhr.responseText;
        const p = document.getElementById("output");
        p.innerHTML = text;
        btn.disabled = false;
        btn.innerHTML = "Summarise";
      };
      xhr.send();
    });
});

var settingsIcon = document.getElementById("settings-icon");
// Add a click event listener to the settings icon
settingsIcon.addEventListener("click", function () {
  // Open a new tab with the settings.html page
  chrome.tabs.create({ url: "settings.html" });
});
