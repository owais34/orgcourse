
const handleSubmit =() =>{
    //console.log(document.getElementById("fullPath"))
    let path = document.getElementById("fullPath").value

    if (path.length === 0) {
        return
    }

    if (path.charAt(0)==="\"") {
        path = path.substring(1)
    }
    if (path.charAt(path.length-1)==="\"") {
        path = path.substring(0, path.length-1)
    }

    document.getElementById("cardForm").setAttribute("hidden","true")
    document.getElementById("success-spinner").removeAttribute("hidden")
    
    fetch(`${baseUrl}/add`, {
        method: 'POST',
        body: JSON.stringify({
            path
        })
    })
    .then(response => {

    })
    .catch(err => {

    })
}

document.getElementById("submitButton").addEventListener("click", handleSubmit);

const baseUrl = "http://127.0.0.1:5000"

