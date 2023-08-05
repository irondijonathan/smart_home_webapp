function displayNotification(device, action) {
  var notificationDiv = document.getElementById("notification");
  var messageElement = document.getElementById("notification-message");
  var onButton = document.getElementById("notification-on-button");
  var offButton = document.getElementById("notification-off-button");

  // Set the notification message
  messageElement.textContent = "Turn " + action + " " + device + "?";

  // Show the notification pop-up
  notificationDiv.style.display = "block";

  // Add event listeners to the buttons
  onButton.addEventListener("click", function () {
    sendAction(device, "on");
    notificationDiv.style.display = "none"; // Hide the notification after user action
  });

  offButton.addEventListener("click", function () {
    sendAction(device, "off");
    notificationDiv.style.display = "none"; // Hide the notification after user action
  });

  console.log("Notification displayed:", device, action);
  console.log("XXXXXXXXXXXX");
}
