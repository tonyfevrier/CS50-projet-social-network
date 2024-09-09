document.addEventListener("DOMContentLoaded", function(){ 

    // Choose the page to print
    document.querySelector("#allposts-btn").addEventListener("click", print_all_posts);
    document.querySelector("#profile-btn").addEventListener("click", print_profile);
    document.querySelector("#following-btn").addEventListener("click", print_following_posts);

    // Authorize submission of a post only if there is an input
    document.querySelector("#textarea-content").addEventListener("input", allowsubmission);

    // Submit a newpost
    document.querySelector('#submit-post').addEventListener("click", submit_post);
}); 


function print_all_posts(event){
    document.querySelector("#allposts-content").style.display = "block";
    document.querySelector("#profile-content").style.display ="none";
    document.querySelector("#following-content").style.display = "none";
}


function print_profile(){
    document.querySelector("#allposts-content").style.display = "none";
    document.querySelector("#profile-content").style.display = "block";
    document.querySelector("#following-content").style.display = "none";
}


function print_following_posts(){
    document.querySelector("#allposts-content").style.display = "none";
    document.querySelector("#profile-content").style.display ="none";
    document.querySelector("#following-content").style.display = "block";
}


function allowsubmission(event){ 
    if (!event.target.value){
        document.querySelector('#submit-post').hidden = true;
        return;
    }
    document.querySelector('#submit-post').hidden = false;
}


function submit_post(){
    // 
}   