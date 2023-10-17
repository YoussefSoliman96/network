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
        // Close the pop-up
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');
    
        const modalsBackdrops = document.getElementsByClassName('modal-backdrop');
    
        for(let i=0; i<modalsBackdrops.length; i++) {
            document.body.removeChild(modalsBackdrops[i]);
        }
    })}

function delete_post(id){
    //delete post
    fetch(`delete_post/${id}`, {
        method: "POST",
    })
        post = document.getElementById(`post_${id}`);
        console.log(post)
        post_area = document.querySelector(`#post_${id}`)
        post_area.classList = ''
        post_area.innerHTML = 
        `<div class="alert alert-danger" role="alert"> Post Deleted! 
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
        </button></div>`
}

function delete_comment(id){
    //delete comment
    fetch(`delete_comment/${id}`, {
        method: "POST",
    })
        comment = document.getElementById(`comment_${id}`);
        console.log(comment)
        comment_area = document.querySelector(`#comment_${id}`)
        comment_area.classList = ''
        comment_area.innerHTML = 
        `<div class="alert alert-danger" role="alert"> Comment Deleted! 
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
        </button></div>`
}

function like(id, liked_posts){
    console.log(liked_posts)
    // Check if post is liked
    if (liked_posts.includes(id) == true){
        var liked = true;
    }
    else {
        var liked = false;
    }


    if (liked == true){
        fetch(`unlike/${id}`)
            var likeBtn = document.getElementById(`like_${id}`)
            var likes = document.getElementById(`post_likes_${id}`)
            likeBtn.innerText = "like"
            var newLikes = parseInt(likes.innerHTML) - 1;
            likes.innerHTML = newLikes;
            liked = false
            liked_posts.pop(id)

    }
    else if (liked == false){
        fetch(`like/${id}`)
            var likeBtn = document.getElementById(`like_${id}`)
            var likes = document.getElementById(`post_likes_${id}`)
            likeBtn.innerText = "Unlike"
            var newLikes = parseInt(likes.innerHTML) + 1;
            likes.innerHTML = newLikes;
            liked = true
            liked_posts.push(id)
    }
    console.log(liked)
    likeBtn = document.getElementById(`like_${id}`)
    likeBtn.onclick = () => {
        like(id, liked_posts)
    }
    }
    

