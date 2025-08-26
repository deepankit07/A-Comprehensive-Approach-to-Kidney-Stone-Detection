function uploadReport() {
  
  var fileInput = document.getElementById("report-file");

  
  if (fileInput.files.length === 0) {
    alert("Please select a file to upload.");
    return;
  }

  
  var file = fileInput.files[0];

  
  var formData = new FormData();
  formData.append("report", file);

  
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "http://localhost:5000/upload", true);
  xhr.withCredentials = false;
  //   xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
  xhr.onload = function () {
    if (xhr.status === 200) {
      
      document.getElementById("prediction-result").textContent =
        xhr.responseText;
    } else {
      alert("Error uploading file. Please try again.");
    }
  };
  xhr.send(formData);
}
