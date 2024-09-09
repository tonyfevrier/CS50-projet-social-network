document.addEventListener("DOMContentLoaded", function(){
    console.log( document.querySelector("#allposts-content"))
    document.querySelector("#allposts-btn").addEventListener("click", print_all_posts);
    document.querySelector("#profile-btn").addEventListener("click", print_profile);
    document.querySelector("#following-btn").addEventListener("click", print_following_posts);
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