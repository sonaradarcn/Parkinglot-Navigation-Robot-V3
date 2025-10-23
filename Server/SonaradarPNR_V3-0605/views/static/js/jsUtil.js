function post(url, data) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(data));
    return xhr.responseText;
}
function msgBox(messageType, messageTitle, messageText, redirectURL) {
    var encodedTitle = encodeURIComponent(messageTitle);
    var encodedText = encodeURIComponent(messageText);
    var url = "findCar_messageBox.jsp?message_type=" + messageType + "&message_title=" + encodedTitle + "&message_text=" + encodedText + "&message_redierct_url=" + encodeURIComponent(redirectURL);
    window.location.href = url;
}