
const handleSubmit =() =>{
    //console.log(document.getElementById("fullfullPath"))
    let fullPath = document.getElementById("fullPath").value
    console.log(fullPath)
    if (fullPath.length === 0) {
        return
    }

    if (fullPath.charAt(0)==="\"") {
        fullPath = fullPath.substring(1)
    }
    if (fullPath.charAt(fullPath.length-1)==="\"") {
        fullPath = fullPath.substring(0, fullPath.length-1)
    }

    document.getElementById("cardForm").setAttribute("hidden","true")
    document.getElementById("success-spinner").removeAttribute("hidden")
    
    fetch(`${baseUrl}/add`, {
        method: 'POST',
        body: JSON.stringify({
            fullPath
        })
    })
    .then(response => {
        console.log(response)
        window.location.href = `${baseUrl}/`
    })
    .catch(err => {
        console.log(err)
    })
}

document.getElementById("submitButton").addEventListener("click", handleSubmit);

document.getElementById("success-spinner").setAttribute("hidden","true")
document.getElementById("cardForm").removeAttribute("hidden")

const baseUrl = "http://127.0.0.1:5000"

