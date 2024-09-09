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
        post.innerHTML = `<p><strong>${element.username}</strong> <span> le ${element.date}</span><p>
                          <p class="post-text">${element.text}</p> 
                          <p>${element.likes} likes</p>`;
        document.querySelector('#allposts-content').append(post);
        }))
}


function print_profile(){
    document.querySelector("#allposts-content").style.display = "none";
    document.querySelector("#profile-content").style.display = "block"; 
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