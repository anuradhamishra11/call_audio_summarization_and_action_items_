chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.text) {
      // Call your call summarization function here, passing the message.text
      const summary = summarizeText(message.text);
  
      // Send the summary back to the popup script
      chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { summary: summary });
      });
    }
  });
  