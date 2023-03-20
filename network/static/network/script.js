document.addEventListener('DOMContentLoaded', function() {

    // Listen for follow and unfollow buttons
    if (document.querySelector('#followbtn')){
        document.querySelector('#followbtn').addEventListener('click', () => follow());
    }else if (document.querySelector('#unfollowbtn')){
        document.querySelector('#unfollowbtn').addEventListener('click', () => unfollow());
    }
    

    // Listen for edit buttons
    if (document.querySelectorAll('.editbtn')){
        editbtns = document.querySelectorAll('.editbtn');

        editbtns.forEach((editbtn)=>{
            editbtn.addEventListener('click', (event) =>{

                // Catch the necessary elements of the post
                const element = event.target;
                let postcontent = element.parentElement.querySelector('.postcontent');
                postcontent.innerHTML = '<textarea></textarea>';

                // Add save button
                const savebtn = document.createElement('button');
                savebtn.setAttribute("class", "savebtn btn btn-primary allbuttons");
                savebtn.innerHTML='Save';

                let editbtn = element;

                // Add event listener for save button
                savebtn.addEventListener('click', (event) =>{
                    const element = event.target;

                    // Get post id and new edited content
                    let post_id = element.parentElement.querySelector('.post_id').value;
                    let content = element.parentElement.querySelector('.postcontent').children[0].value;

                    // Edit the content using the edit fetch function
                    edit(post_id, content);

                    // Remove the save button and add the newly edited content
                    let contentdiv = element.parentElement.querySelector('.postcontent');
                    contentdiv.innerHTML = content;
                    element.parentElement.appendChild(editbtn);
                    element.remove();
                })

                // Append button
                element.parentElement.appendChild(savebtn);

                // Remove edit button
                element.parentElement.querySelector('.editbtn').remove();
            });
        })
    }


    // Listen for like buttons
    if (document.querySelectorAll('.likebtn')){
        likebtns = document.querySelectorAll('.likebtn');

        likebtns.forEach((likebtn)=>{
            likebtn.addEventListener('click', (event) =>{

                // Catch the necessary elements of the post
                const element = event.target;
                let post_id = element.parentElement.querySelector('.post_id').value;
                let likecount = element.parentElement.querySelector('.likecount');
                let parent_button_element = element.parentElement.parentElement.querySelector('.postdiv');
                console.log(element);
                console.log(likecount.innerHTML);
                console.log(`Postdiv is: ${parent_button_element.innerHTML}`);
                console.log(`Post id is: ${post_id}`);

                // Like the post using the like fetch function depending on the icon class, and update the like count using the .then()

                if (element.classList.contains('fa-regular')){
                    like(post_id, likecount);
                } else if(element.classList.contains('fa-solid')){
                    unlike(post_id, likecount);
                }

                // Toggle the heart class to liked or unliked!
                if (element.classList.contains('fa-regular')){
                    element.setAttribute("class", "fa-solid fa-heart");
                } else if(element.classList.contains('fa-solid')){
                    element.setAttribute("class", "fa-regular fa-heart");

                }
            });
        })
    }



});




function follow() {
    //Get the profile id from the HTML hidden input
    let user_id = document.querySelector('#user_id').value;

    // Use python to follow
    fetch('/follow/'+user_id)
    .then( () =>{
        // Delete follow button and replace it with unfollow
        document.querySelector('#followbtndiv').innerHTML='';
        const unfollowbtn = document.createElement('button');
        unfollowbtn.setAttribute("id", "unfollowbtn");
        unfollowbtn.setAttribute("class", "btn btn-primary allbuttons");
        unfollowbtn.innerHTML='Unfollow';

        // Append button
        document.querySelector('#followbtndiv').appendChild(unfollowbtn);
    })
}

function unfollow() {
    //Get the profile id from the HTML hidden input
    let user_id = document.querySelector('#user_id').value;

    // Use python to unfollow
    fetch('/unfollow/'+user_id)
    .then( () =>{
        // Delete unfollow button and replace it with follow
        document.querySelector('#followbtndiv').innerHTML='';
        const followbtn = document.createElement('button');
        followbtn.setAttribute("id", "followbtn");
        followbtn.setAttribute("class", "btn btn-primary allbuttons");
        followbtn.innerHTML='Follow';

        // Append button
        document.querySelector('#followbtndiv').appendChild(followbtn);
    })
}

function edit(post_id, content){
    fetch('/edit/'+post_id, {
        method: 'POST',
        body: JSON.stringify({
            content: content,
        })
    })
    .then(response => response.json())
    .then( (message) =>{
        alert(message.message)
    })
}

function like(post_id, element){

    fetch('/like', {
        method: 'POST',
        body: JSON.stringify({
            postid: post_id,
        })
    })
    .then( likecount => likecount.json())
    .then( jsonobject =>{
        element.innerHTML = `Likes: ${jsonobject.likecount}`;
    })
    
}

function unlike(post_id, element){
    fetch('/unlike', {
        method: 'POST',
        body: JSON.stringify({
            postid: post_id,
        })
    })
    .then( likecount => likecount.json())
    .then( jsonobject =>{
        element.innerHTML = `Likes: ${jsonobject.likecount}`;
    })
}