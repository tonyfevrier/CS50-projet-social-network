document.addEventListener("DOMContentLoaded", function(){  

    // Choose the page to print
    document.querySelector("#allposts-btn").addEventListener("click", print_some_posts);

    if (document.querySelector("#profile-btn")) document.querySelector("#profile-btn").addEventListener("click", print_profile); 

    // Authorize submission of a post only if there is an input
    document.querySelector("#textarea-content").addEventListener("input", allowsubmission);

    // Submit a newpost
    document.querySelector('#submit-post').addEventListener("click", submit_post);

    print_some_posts('all');
}); 

function print_some_posts(whichposts){
    // Print the block of posts, hide profile block  
    document.querySelector("#allposts-content").style.display = "block";
    document.querySelector("#profile-content").style.display ="none"; 

    // Request the API to load the appropriate set of posts
    fetch(`/someposts/${whichposts}`)
    .then(response => response.json())
    .then(data => data.forEach(element => {
        //create the html element containing the post 
        const post = document.createElement('div');
        post.className = "post-element";
        post.innerHTML = `<button class="user-btn">${element.username}</button> 
                          <p><span>le ${element.date}</span><p>
                          <p class="post-text">${element.text}</p> 
                          <p>${element.likes} likes</p>`;
        document.querySelector('#allposts-content').append(post);
        post.querySelector('.user-btn').addEventListener('click', print_profile);
    }))
}


function print_profile(event){
    document.querySelector("#allposts-content").style.display = "none";
    document.querySelector("#profile-content").style.display = "block"; 
    document.querySelector("#profile-content").innerHTML = "";
 
    // Request to get the user informations
    fetch(`/profile/${event.target.textContent}`)
    .then(response => response.json())
    .then(data => {

        // Recover profile infos and create element html 
        const user_infos = document.createElement('div');
        user_infos.className = 'user-infos'
        user_infos.innerHTML = `<p>Number of followers: ${data.user_stats.followers_number}</p>
                                <p>Following: ${data.user_stats.following_number} people</p>`
        
        // Add a follow/unfollow button and an eventListener
        if (!data.userisowner){
            if (data.userisfollower) user_infos.innerHTML += `<button class="follow-${data.user_stats.username}">Unfollow</button>`
            else user_infos.innerHTML += `<button class="follow-${data.user_stats.username}">Follow</button>` 
        }

        // Add the html element to the DOM
        document.querySelector("#profile-content").append(user_infos);
        if (document.querySelector(`.follow-${data.user_stats.username}`)) document.querySelector(`.follow-${data.user_stats.username}`).addEventListener('click', follow_or_unfollow);

        // Recover user posts and create elements
        data.posts.forEach(element => {
            const user_post = document.createElement('div');
            user_post.className = "post-element";
            user_post.innerHTML = `<p>${element.username}</p> <p><span> le ${element.date}</span><p>
                              <p class="post-text">${element.text}</p> 
                              <p>${element.likes} likes</p>`;
            document.querySelector('#profile-content').append(user_post);
        })
    })
}


function allowsubmission(event){ 
    if (!event.target.value){
        document.querySelector('#submit-post').hidden = true;
        return;
    }
    document.querySelector('#submit-post').hidden = false;
}


function submit_post(){
    // Récupérer le token
    const csrf_token = document.querySelector('meta[name="csrf-token"]').content;

    // Make a request to the API 
    fetch('/post', { 
        method: "POST",
        headers:{
            'X-CSRFToken':csrf_token,
        },
        body: JSON.stringify({
            post_content: document.querySelector('#textarea-content').value,
        })
    })
    .then(response => { 
        document.querySelector('#textarea-content').value = ''; 

        // Do not print posts already present on the page
        document.querySelectorAll('.post-element').forEach(element => element.style.display = 'none');

        // Print all posts 
        print_some_posts('all');
    })
    .catch(error => console.log(error));
}   

function follow_or_unfollow(event){

    // Recover the profile user 
    const username = event.target.className.split('-')[1]; 
    
    // Make a request to toggle this user from following
    fetch(`/follow/${username}`)
    .catch(error => console.log(error));
}