document.addEventListener("DOMContentLoaded", function(){  

    // Choose the page to print
    document.querySelector("#allposts-btn").addEventListener("click", () => print_some_posts('all', 1));  

    // Events if user is logged in
    if (document.querySelector("#profile-btn")){
        document.querySelector("#following-btn").addEventListener("click", () => print_some_posts('following', 1));
        document.querySelector("#profile-btn").addEventListener("click", () => print_profile(document.querySelector("#profile-btn").textContent)); 
        
        // Authorize submission of a post only if there is an input
        document.querySelector("#textarea-content").addEventListener("input", allowsubmission);

        // Submit a newpost 
        document.querySelector('#submit-post').addEventListener("click", submit_post);
        //print_some_posts('all', 1);
        //return;
    }
    print_some_posts('all', 1);
}); 

// Event handlers

function print_some_posts(whichposts, page_number){
    /* Print a selection of posts :
    Inputs: 
        - whichpost (str): all or following if we want to get the posts of people we follow
        - page_number (int): the page of posts we want to print (posts are printed ten by ten) */

    // Print the block of posts, hide profile block  
    document.querySelector("#allposts-content").style.display = "block";
    document.querySelector("#profile-content").style.display ="none"; 

    // Hide the eventual posts printed before and the next/previous buttons
    if (document.querySelectorAll('.post-element')) document.querySelectorAll('.post-element').forEach(element => element.remove());
    if (document.querySelector('.nav-buttons')) document.querySelector('.nav-buttons').remove(); 
    
    // Request the API to load the appropriate set of posts
    fetch(`/someposts/${whichposts}?param1=${page_number}`)
    .then(response => response.json())
    .then(data => {

        //  Print each post
        data["posts"].forEach(element => {
        // Create the html element containing the post   
        const post = create_a_post_element(element, data["requestuser"]);

        // Add the post to the DOM
        document.querySelector('#allposts-content').append(post);
        post.querySelector('.user-btn').addEventListener('click', () => print_profile(element.username));
        post.querySelector('.heart-btn').addEventListener("click", () => like_post(post));
        })

        // Add buttons next/previous to change the slot of posts
        add_button_to_browse_posts(data, whichposts, page_number);
    })
    .catch(error => console.log(error));
}


function print_profile(username){
    /* Print the profile of a user given by its username */

    document.querySelector("#allposts-content").style.display = "none";
    document.querySelector("#profile-content").style.display = "block"; 
    document.querySelector("#profile-content").innerHTML = "";
 
    // Request to get the user informations
    fetch(`/profile/${username}`)
    .then(response => response.json())
    .then(data => {

        // Recover profile infos and create element html 
        const user_infos = document.createElement('div');
        user_infos.className = 'user-infos'
        user_infos.innerHTML = `<p>Number of followers: ${data.user_stats.followers_number}</p>
                                <p>Following: ${data.user_stats.following_number} people</p>`
        
        // Add a follow/unfollow button and an eventListener if it is not owner profile
        if (!data.userisowner){
            if (data.userisfollower) user_infos.innerHTML += `<button class="follow-${data.user_stats.username}">Unfollow</button>`
            else user_infos.innerHTML += `<button class="follow-${data.user_stats.username}">Follow</button>` 
        }
        document.querySelector("#profile-content").append(user_infos);
        if (document.querySelector(`.follow-${data.user_stats.username}`)) document.querySelector(`.follow-${data.user_stats.username}`).addEventListener('click', follow_or_unfollow);

        // Recover user posts and create elements
        data.posts.forEach(element => { 
            const user_post = create_a_post_element(element, data['requestuser']); 
            document.querySelector('#profile-content').append(user_post);
            user_post.querySelector('.heart-btn').addEventListener("click", () => like_post(user_post));
        })
    })
}


function allowsubmission(event){ 
    /* Function to authorize to submit a post */
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
        document.querySelector('#submit-post').hidden = true;

        // Do not print posts already present on the page
        document.querySelectorAll('.post-element').forEach(element => element.style.display = 'none');

        // Print all posts 
        print_some_posts('all', 1);
    })
    .catch(error => console.log(error));
}   

function follow_or_unfollow(event){

    // Recover the profile user 
    const username = event.target.className.split('-')[1];  
    
    // Make a request to toggle this user from following
    fetch(`/follow/${username}`)
    .then(response => {
        // Update the actuel profile page
        print_profile(username)
    })
    .catch(error => console.log(error));
}

function pass_in_edition_mode(event){
    /* Get a textarea to edit a given post */

    // Prevent multiple textarea from opening before saving one 
    if (document.querySelector('.save-btn')) return;

    // Recover the corresponding post and hide its content
    const post = event.target.closest('.post-element');
    
    const content = post.querySelector('.post-text');
    content.hidden = true;

    // Create a textarea and a save button
    const form = document.createElement('div');
    form.id = "post-form";
    form.innerHTML = `<textarea class='edit-content'>${content.textContent}</textarea><button class="save-btn">Save</button>`
    content.after(form);

    // Recover the post id and create an eventListener to save the post
    document.querySelector('.save-btn').addEventListener('click', () => edit_post(post));//,post.querySelector('.post-id').textContent));    
}

function edit_post(post){
    const csrf_token = document.querySelector('meta[name="csrf-token"]').content;

    fetch(`/editpost/${post.querySelector('.post-id').textContent}`,{
        method: "POST",
        headers: {
            'X-CSRFToken':csrf_token,
        },
        body: JSON.stringify({
            content: document.querySelector('.edit-content').value,
        })
    })
    .then(response => {
        post.querySelector('.post-text').textContent = document.querySelector('.edit-content').value;
        post.querySelector('.post-text').hidden = false;
        document.querySelector('#post-form').remove();
    })
    .catch(error => console.log(error));
}

function like_post(post){
    if (document.querySelector('.error-like')) document.querySelector('.error-like').remove();

    // Make a request to be a liker or to remove from likers
    fetch(`/likepost/${post.querySelector('.post-id').textContent}`)
    .then(response => response.json())
    .then(data => {  
        // Change the number of likes in the page
        if (data.post){ 
            post.querySelector(".update-post p").innerHTML = data.post["likes"];
        } else {
            post.insertAdjacentHTML('beforeend', `<p class="error-like">${data.error}</p>`);
        }
    })
    .catch(error => console.log(error))
}

// Utils for refactoring

function create_a_post_element(element, request_user){ 
    // Create the html element containing the post  
    const post = document.createElement('div');
    post.className = "post-element";
    post.innerHTML = `<div class="user-date"> 
                        <button class="user-btn">${element.username}</button> 
                        <span class="post-date">le ${element.date}</span>
                      </div>
                      <p class="post-text">${element.text}</p> 
                      <div class="update-post">
                        <button class="heart-btn" id="post-${element.id}"><img src="/static/network/heart.png" alt="like"></button>
                        <p class="post-likes">${element.likes}</p>
                      </div>
                      <p class='post-id' hidden=true>${element.id}</p>`;

    // Add an edition button for request user posts
    if (request_user === element.username){
        const edit_button = document.createElement("button");
        edit_button.className = "edit"
        edit_button.innerHTML = "Edit";
        post.querySelector(".update-post").append(edit_button); 
        edit_button.addEventListener('click', pass_in_edition_mode);
    }
    return post;
}

function add_button_to_browse_posts(data, whichposts, page_number){
    /* Since posts are printed ten by ten, add buttons to see previous or next posts 
    Inputs : 
        - data: returned by the fetch request
        - whichposts: all or following
        - page_number: the number of the page */

    const nav_buttons = document.createElement('div');
    nav_buttons.className = "nav-buttons";
    document.querySelector('#allposts-content').append(nav_buttons);        

    if (data['previous']){
        const previous = document.createElement('button');
        previous.className = "previous";
        previous.innerHTML = "Previous";
        nav_buttons.append(previous);
        previous.addEventListener('click', () => print_some_posts(whichposts, page_number - 1));
    } 
    if (data['next']){
        const next = document.createElement('button');
        next.className = "next";
        next.innerHTML = "Next";
        nav_buttons.append(next);
        next.addEventListener('click', () => print_some_posts(whichposts, page_number + 1));
    } 
}
