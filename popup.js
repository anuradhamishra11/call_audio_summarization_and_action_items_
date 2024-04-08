chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message.summary) {
    document.getElementById("summary").textContent = message.summary;
  }
});
