document.addEventListener("DOMContentLoaded", function(){
    document.querySelector("#allposts-content").addEventListener("click", print_all_posts);
    document.querySelector("#profile-content").addEventListener("click", print_profile);
    document.querySelector("#following-content").addEventListener("click", print_following_posts);
}); 


function print_all_posts(){
    document.querySelector("#allposts-content")
}


function print_profile(){
    document.querySelector("#profile-content")
}


function print_following_posts(){
    document.querySelector("#following-content")
}