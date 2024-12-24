addEventListener('DOMContentLoaded', function(){
    const newformcontent = document.getElementById('newpost');
    if(newformcontent !== null){
        newformcontent.addEventListener('keyup', togglepostbutton, false);
    }
    const newpostsubmitbutton = document.getElementById('newpostsubmitbutton');
    
    const newpost = document.getElementById('newpost');
    if(newpost !== null){
        newpost.onkeyup = adjustheight(newpost.id);
    }  

    function togglepostbutton(){
        if(newformcontent.value.length === 0){
            newpostsubmitbutton.disabled = true;
        } else{
            newpostsubmitbutton.disabled = false;
        }
    }
})


function togglefollow(followerid, followingid){
    const follow_button = document.getElementById('follow-button');
    const followercount = document.getElementById('numfollower');
    if(follow_button.innerHTML === 'unfollow'){
        console.log(`user[${followerid}] wants to unfollow user[${followingid}]`);
        
        fetch('unfollow', {
            method: 'PUT',
            body: JSON.stringify({
                whowantstounfollow: followerid,
                targetunfollow: followingid
            })
        })
        
        
        fetch('unfollow')
        .then(response => response.json())
        .then(result => {
            console.log(result);
            
        })
        followercount.innerHTML = parseInt(followercount.innerHTML) - 1;
        follow_button.innerHTML = 'follow';
        
    } else{
        console.log(`user[${followerid}] wants to follow user[${followingid}]`);
        
        fetch('follow', {
            method: 'PUT',
            body: JSON.stringify({
                whowantstofollow: followerid,
                targetfollow: followingid
            })
        })
        
        
        fetch('follow')
        .then(response => response.json())
        .then(result => {
            console.log(result);
            
        })
        followercount.innerHTML = parseInt(followercount.innerHTML) + 1;
        follow_button.innerHTML = 'unfollow';
    }
}


async function togglelike(user_id, post_id){
    let likecount = document.getElementById(`like-count-${post_id}`);
    const likebutton = document.getElementById(`like-${post_id}`);
    
    if(likebutton.innerHTML === 'like'){
        console.log(`user[${user_id}] wants to like post[${post_id}]`);
        
        fetch(`like/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                like: true
            })
        })

        likebutton.innerHTML = 'nolike';
        likebutton.style.color = 'orange';

        fetch(`like/${post_id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })
        
        likecount.innerHTML = parseInt(likecount.innerHTML) + 1;
        console.log('updated like count')
        
    } else{
        console.log(`user[${user_id}] wants to remove like for post[${post_id}]`);
        
        fetch(`like/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                like: false
            })
        })
        
        
        likebutton.innerHTML = 'like';
        likebutton.style.color = 'red';
        
        fetch(`like/${post_id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })
        likecount.innerHTML = parseInt(likecount.innerHTML) - 1;
        console.log('updated like count')
    }
}

function editpost(post_id){
    console.log(`user wants to edit post[${post_id}]`)
    const content_div = document.getElementById(`contentdiv-${post_id}`);

    const content_elem = document.getElementById(`content-${post_id}`);
    const content_text = content_elem.innerHTML;
    content_elem.style.display = 'none';

    const editbutton = document.getElementById(`edit-button-${post_id}`);
    editbutton.style.display = 'none';


    let textareaelement = document.createElement('textarea');
    textareaelement.value = content_text;
    textareaelement.style.color = 'blue';
    textareaelement.id = `editpost-${post_id}`;
    textareaelement.rows =  1 + Math.floor(textareaelement.value.length / 80);
    textareaelement.onkeyup = adjustheight(textareaelement.id);

    let savebutton = document.createElement('button');
    savebutton.className = 'btn btn-link p-0 mx-2';
    savebutton.id = `save-button-${post_id}`;
    savebutton.innerHTML = 'save';
    savebutton.onclick = saveedit(post_id);
    
    let cancelbutton = document.createElement('button');
    cancelbutton.className = 'btn btn-link p-0 mx-2';
    cancelbutton.id = `cancel-button-${post_id}`;
    cancelbutton.innerHTML = 'cancel';
    cancelbutton.onclick = cancel(post_id);


    content_div.append(textareaelement);
    content_div.append(cancelbutton);
    content_div.append(savebutton);
}

function saveedit(post_id){
    return function(){
        console.log('user wants to save the post');

        const content_elem = document.getElementById(`content-${post_id}`);
        const content_text = content_elem.innerHTML;
        content_elem.style.display = 'block';

        const editbutton = document.getElementById(`edit-button-${post_id}`);
        editbutton.style.display = 'inline-block';
        
        const savebutton = document.getElementById(`save-button-${post_id}`);
        const textareaelement = document.getElementById(`editpost-${post_id}`);

        
        fetch(`saveeditpost/${post_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: textareaelement.value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })
        
        content_elem.innerHTML = textareaelement.value;
        const cancelbutton = document.getElementById(`cancel-button-${post_id}`);
        textareaelement.remove();
        cancelbutton.remove();
        savebutton.remove();
    }
}

function cancel(post_id){
    return function(){
        console.log(`user want to cancel this edit`);
        
        const content_elem = document.getElementById(`content-${post_id}`);
        const content_text = content_elem.innerHTML;
        content_elem.style.display = 'block';
        
        const editbutton = document.getElementById(`edit-button-${post_id}`);
        editbutton.style.display = 'inline-block';
        
        const cancelbutton = document.getElementById(`cancel-button-${post_id}`);
        const savebutton = document.getElementById(`save-button-${post_id}`);
        const textareaelement = document.getElementById(`editpost-${post_id}`);
        textareaelement.remove();
        cancelbutton.remove();
        savebutton.remove();
    }
}

function adjustheight(textareaid){
    return function(){
        var textareaelement = document.getElementById(textareaid);

        if(textareaelement.value === ''){
            textareaelement.rows = 1;
            console.log(`height adjust to 1 cols`);
        } else if (textareaelement.scrollHeight > textareaelement.clientHeight) {
            const required_height = 1 + textareaelement.rows;
            textareaelement.rows = required_height;
            console.log(`height adjust to ${required_height} cols`);
        }

    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}