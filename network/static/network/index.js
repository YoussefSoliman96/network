function getCookie(name){
    const value = `: ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}


function editPost(id){
    const editedText = document.getElementById(`edit_content_${id}`).value;
    const text = document.getElementById(`content_${id}`);
    const modal = document.getElementById(`edit_${id}`);
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            content: editedText
        })
    })
    .then(response => response.json())
    .then(result => {
        text.innerHTML = result.edited_text;

        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');
    
        const modalsBackdrops = document.getElementsByClassName('modal-backdrop');
    
        for(let i=0; i<modalsBackdrops.length; i++) {
            document.body.removeChild(modalsBackdrops[i]);
        }
    })}