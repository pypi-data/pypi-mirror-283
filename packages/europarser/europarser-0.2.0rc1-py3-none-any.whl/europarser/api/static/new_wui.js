document.getElementsByClassName('myInput').forEach(function (item) {
    item.style.margin = 'auto 1vh 1vh' + document.getElementById('myDropzone').offsetHeight + 'px' + ' 50vh';
});


function saveBlob(blob, fileName) {
    var download = document.getElementById('download');
    download.href = window.URL.createObjectURL(blob);
    download.download = fileName;
}

function createUrl(files, dataBlock) {
    // let url = "{{host + '/upload?'}}"
    let url = "/upload?"
        // + "filter_keywords=" + document.getElementById('filter_keywords').checked.toString()
        // + "&minimal_support=" + (document.getElementById('minimal_support').value || 1)
        // + "&minimal_support_kw=" + (document.getElementById('minimal_support_kw').value || 1)
        // + "&minimal_support_journals=" + (document.getElementById('minimal_support_journals').value || 1)
        // + "&minimal_support_authors=" + (document.getElementById('minimal_support_authors').value || 1)
        // + "&minimal_support_dates=" + (document.getElementById('minimal_support_dates').value || 1)

    console.log(url)
    return (url)
}

function submitForm() {
    //send all the form data along with the files:
    var xhr = new XMLHttpRequest();
    var formData = new FormData();

    let checkboxes = document.getElementsByTagName('input');
    checkboxes = Array.from(checkboxes);

    for (let checkbox of checkboxes) {
        if (checkbox.type === 'checkbox' && checkbox.checked) {
            formData.append("output", checkbox.id.toString().toLowerCase());
        }
    }

    // TODO add the rest of the form data (files)
    1/0

    console.log(formData.get("output"))
    xhr.open("POST", createUrl());

    let len_ = checkboxes.length
    for (let i = 0; i < len_; i++) {
        checkboxes[i].disabled = true;
        checkboxes[i].cursor = "not-allowed";
        checkboxes[i].style.opacity = "0.5";
    }
    xhr.responseType = 'blob';
    xhr.onload = function (e) {
        if (e.currentTarget.status > 300) {
            document.getElementById('loader').style.display = "none";
            document.getElementById('error').innerHTML = e.currentTarget.statusText;
            document.getElementById('error').style.display = "block";
        }
        var blob = e.currentTarget.response;
        var contentDispo = e.currentTarget.getResponseHeader('Content-Disposition');
        // https://stackoverflow.com/a/23054920/
        var fileName = contentDispo.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)[1];
        document.getElementById('download').style.display = "block";
        document.getElementById('loader').style.display = "none";
        saveBlob(blob, fileName);
    }
    xhr.send(formData);
}

let data = Dropzone.options.myDropzone = {
    paramName: 'files',
    url: createUrl,
    autoProcessQueue: false,
    uploadMultiple: true,
    parallelUploads: 100,
    maxFiles: 100,
    acceptedFiles: '.html',
}


